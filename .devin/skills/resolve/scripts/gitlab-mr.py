#!/usr/bin/env python3

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
from urllib.parse import quote, urlparse

PROVIDER = "gitlab"
DEFAULT_TIMEOUT_S = 60
PER_PAGE = 100


class HelperError(Exception):
    def __init__(self, code, message, details=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details if isinstance(details, dict) else {}


def emit_error(err, host=None, project=None, iid=None):
    payload = {"error": err.code, "message": err.message}
    if host is not None:
        payload["host"] = host
    if project is not None:
        payload["project"] = project
    if iid is not None:
        payload["iid"] = iid
    payload.update(err.details)
    print(json.dumps(payload, indent=2, sort_keys=True), file=sys.stderr)


def check_host(raw):
    host = (raw or "").strip()
    if not host:
        raise HelperError("usage", "host must not be empty")
    if "://" in host or "/" in host or "@" in host:
        raise HelperError("usage", f"host must be a bare hostname, not a URL or path: {raw!r}")
    if any(ch.isspace() for ch in host):
        raise HelperError("usage", f"host must not contain whitespace: {raw!r}")
    return host


def _check_project_segment(segment, raw):
    if not segment:
        raise HelperError("usage", f"project has an empty path segment: {raw!r}")
    for ch in segment:
        if not (ch.isalnum() or ch in "._-"):
            raise HelperError("usage", f"project segment has an illegal character: {segment!r}")


def check_project(raw):
    project = (raw or "").strip()
    if not project or "/" not in project:
        raise HelperError("usage", f"project must look like GROUP/PROJECT: {raw!r}")
    if project.startswith("/") or project.endswith("/"):
        raise HelperError("usage", f"project must not start or end with '/': {raw!r}")
    for segment in project.split("/"):
        _check_project_segment(segment, raw)
    return project


def check_iid(raw):
    if type(raw) is bool:
        raise HelperError("usage", f"mr IID must be a positive integer: {raw!r}")
    try:
        iid = int(raw)
    except (TypeError, ValueError) as err:
        raise HelperError("usage", f"mr IID must be a positive integer: {raw!r}") from err
    if iid <= 0:
        raise HelperError("usage", f"mr IID must be a positive integer: {raw!r}")
    return iid


def check_note_id(raw):
    if type(raw) is bool:
        raise HelperError("usage", f"note id must be a positive integer: {raw!r}")
    try:
        note_id = int(raw)
    except (TypeError, ValueError) as err:
        raise HelperError("usage", f"note id must be a positive integer: {raw!r}") from err
    if note_id <= 0:
        raise HelperError("usage", f"note id must be a positive integer: {raw!r}")
    return note_id


def check_discussion(raw):
    discussion_id = (raw or "").strip()
    if not discussion_id:
        raise HelperError("usage", "discussion id must not be empty")
    if any(ch.isspace() for ch in discussion_id) or "/" in discussion_id:
        raise HelperError("usage", f"discussion id is not a single path segment: {raw!r}")
    return discussion_id


def check_expected_head(raw):
    if type(raw) is bool or not isinstance(raw, str):
        raise HelperError("usage", f"expected head must be a full 40- or 64-character hex SHA: {raw!r}")
    head = raw.strip()
    if not head:
        raise HelperError("usage", "expected head must not be empty")
    if len(head) not in (40, 64) or not all(c in "0123456789abcdefABCDEF" for c in head):
        raise HelperError("usage", f"expected head must be a full 40- or 64-character hex SHA: {raw!r}")
    return head.lower()


def check_timeout(raw):
    try:
        timeout_s = float(raw)
    except (TypeError, ValueError) as err:
        raise HelperError("usage", f"timeout must be a positive number of seconds: {raw!r}") from err
    if not math.isfinite(timeout_s) or timeout_s <= 0:
        raise HelperError("usage", f"timeout must be a positive finite number of seconds: {raw!r}")
    return timeout_s


def _run(argv, timeout_s, label):
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=timeout_s, check=False)
    except subprocess.TimeoutExpired as err:
        raise HelperError(
            "timeout",
            f"glab call timed out after {timeout_s:g}s: {label}",
            {"endpoint": label},
        ) from err
    except UnicodeDecodeError as err:
        raise HelperError(
            "subprocess_failed",
            f"glab output could not be decoded as text for {label}",
            {"endpoint": label},
        ) from err
    except OSError as err:
        raise HelperError(
            "subprocess_failed",
            f"could not execute glab for {label}: {err}",
            {"endpoint": label},
        ) from err


def _parse_json(stdout, label):
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as err:
        raise HelperError(
            "malformed_payload",
            f"glab returned unparseable JSON for {label}: {err}",
            {"endpoint": label},
        ) from err


def _refuse_failed(proc, label):
    if proc.returncode != 0:
        raise HelperError(
            "subprocess_failed",
            f"glab call failed (exit {proc.returncode}): {label}",
            {"endpoint": label, "exit": proc.returncode, "stderr": (proc.stderr or "")[:2000]},
        )


def fetch_single_object(host, endpoint, timeout_s):
    argv = ["glab", "api", "--hostname", host, endpoint, "-X", "GET", "--output", "json"]
    proc = _run(argv, timeout_s, endpoint)
    _refuse_failed(proc, endpoint)
    if not (proc.stdout or "").strip():
        raise HelperError(
            "malformed_payload",
            f"glab returned an empty body for {endpoint}; never an empty success",
            {"endpoint": endpoint},
        )
    payload = _parse_json(proc.stdout, endpoint)
    if not isinstance(payload, dict):
        raise HelperError(
            "malformed_payload",
            f"expected a JSON object for {endpoint}, got {type(payload).__name__}",
            {"endpoint": endpoint},
        )
    return payload


def fetch_complete_list(host, endpoint, timeout_s):
    argv = ["glab", "api", "--hostname", host, endpoint, "-X", "GET",
            "--paginate", "--output", "json"]
    proc = _run(argv, timeout_s, endpoint)
    _refuse_failed(proc, endpoint)
    if not (proc.stdout or "").strip():
        raise HelperError(
            "malformed_payload",
            f"glab returned an empty body for {endpoint}; never an empty success",
            {"endpoint": endpoint},
        )
    payload = _parse_json(proc.stdout, endpoint)
    if not isinstance(payload, list):
        raise HelperError(
            "malformed_payload",
            f"expected a JSON array for {endpoint}, got {type(payload).__name__}",
            {"endpoint": endpoint},
        )
    return payload


def _check_mr_identity(obj, iid, endpoint):
    if type(obj.get("iid")) is not int or obj.get("iid") != iid:
        raise HelperError(
            "wrong_identity",
            f"MR identity mismatch: asked for iid {iid}, got {obj.get('iid')!r}",
            {"endpoint": endpoint, "returned_iid": obj.get("iid")},
        )


def _check_mr_web_url(web_url, host, endpoint, iid):
    if not isinstance(web_url, str) or not web_url.strip():
        raise HelperError(
            "malformed_payload",
            f"MR {iid} response carries no web_url string",
            {"endpoint": endpoint},
        )
    parsed = urlparse(web_url)
    want_host, _, want_port = host.lower().partition(":")
    if not parsed.hostname or parsed.hostname.lower() != want_host:
        raise HelperError(
            "wrong_identity",
            f"MR web_url host {parsed.hostname!r} does not match requested host {host!r}",
            {"endpoint": endpoint, "web_url": web_url},
        )
    try:
        got_port = parsed.port
    except ValueError as err:
        raise HelperError(
            "wrong_identity",
            f"MR web_url {web_url!r} carries an unparsable port",
            {"endpoint": endpoint, "web_url": web_url},
        ) from err
    if want_port and str(got_port or "") != want_port:
        raise HelperError(
            "wrong_identity",
            f"MR web_url port {got_port!r} does not match requested host {host!r}",
            {"endpoint": endpoint, "web_url": web_url},
        )


def _check_mr_references(references, project, iid, endpoint):
    full_ref = references.get("full") if isinstance(references, dict) else None
    if not isinstance(full_ref, str) or not full_ref.strip():
        raise HelperError(
            "malformed_payload",
            f"MR {iid} response carries no references.full string",
            {"endpoint": endpoint, "references": references},
        )
    if full_ref.lower() != f"{project}!{iid}".lower():
        raise HelperError(
            "wrong_identity",
            f"MR full reference {full_ref!r} does not match requested project {project!r}",
            {"endpoint": endpoint, "full_reference": full_ref},
        )


def _check_mr_payload_fields(obj, iid, endpoint):
    if type(obj.get("id")) is not int:
        raise HelperError(
            "malformed_payload",
            f"MR {iid} response carries no integer id",
            {"endpoint": endpoint, "id": obj.get("id")},
        )
    if type(obj.get("project_id")) is not int:
        raise HelperError(
            "malformed_payload",
            f"MR {iid} response carries no integer project_id",
            {"endpoint": endpoint, "project_id": obj.get("project_id")},
        )
    head_sha = obj.get("sha")
    if not isinstance(head_sha, str) or not head_sha:
        raise HelperError(
            "malformed_payload",
            f"MR {iid} response carries no head sha",
            {"endpoint": endpoint},
        )
    return head_sha


def get_mr(host, project, iid, timeout_s):
    endpoint = f"projects/{quote(project, safe='')}/merge_requests/{iid}"
    obj = fetch_single_object(host, endpoint, timeout_s)
    _check_mr_identity(obj, iid, endpoint)
    _check_mr_web_url(obj.get("web_url"), host, endpoint, iid)
    _check_mr_references(obj.get("references"), project, iid, endpoint)
    head_sha = _check_mr_payload_fields(obj, iid, endpoint)
    return obj, head_sha


def check_thread_notes(thread_notes, discuss_id):
    for note in thread_notes:
        if not isinstance(note, dict) or type(note.get("id")) is not int:
            raise HelperError(
                "malformed_payload",
                f"discussion {discuss_id!r} holds a note without an integer id; census unusable",
                {"discussion_id": discuss_id},
            )


def check_census(discussions, notes):
    for index, discussion in enumerate(discussions):
        discuss_id = discussion.get("id") if isinstance(discussion, dict) else None
        if not isinstance(discuss_id, str) or not discuss_id:
            raise HelperError(
                "malformed_payload",
                f"discussion #{index} has no string id; census unusable",
                {"index": index},
            )
        thread_notes = discussion.get("notes")
        if not isinstance(thread_notes, list):
            raise HelperError(
                "malformed_payload",
                f"discussion {discuss_id!r} carries no notes array; census unusable",
                {"discussion_id": discuss_id},
            )
        check_thread_notes(thread_notes, discuss_id)
    for index, note in enumerate(notes):
        if not isinstance(note, dict) or type(note.get("id")) is not int:
            raise HelperError(
                "malformed_payload",
                f"root note #{index} has no integer id; census unusable",
                {"index": index},
            )


def read_census(host, project, iid, timeout_s):
    _, head_before = get_mr(host, project, iid, timeout_s)
    base = f"projects/{quote(project, safe='')}/merge_requests/{iid}"
    discussions = fetch_complete_list(host, f"{base}/discussions?per_page={PER_PAGE}", timeout_s)
    notes = fetch_complete_list(host, f"{base}/notes?per_page={PER_PAGE}", timeout_s)
    _, head_after = get_mr(host, project, iid, timeout_s)
    if head_before != head_after:
        raise HelperError(
            "head_changed",
            f"MR head changed during census ({head_before} -> {head_after}); prior evidence is stale",
            {"head_before": head_before, "head_after": head_after,
             "discussions_fetched": len(discussions), "notes_fetched": len(notes)},
        )
    check_census(discussions, notes)
    return head_before, discussions, notes


def _extract_thread_note_ids(discussions):
    thread_note_ids = set()
    for d in discussions:
        for n in d.get("notes", []):
            if isinstance(n, dict) and type(n.get("id")) is int:
                thread_note_ids.add(n["id"])
    return thread_note_ids


def _collect_unique_note(note, thread_note_ids, seen_note_ids, normalized_notes):
    if isinstance(note, dict) and type(note.get("id")) is int:
        nid = note["id"]
        if nid not in thread_note_ids and nid not in seen_note_ids:
            seen_note_ids.add(nid)
            normalized_notes.append(note)


def normalize_census_notes(discussions, notes, thread_note_ids):
    normalized_notes = []
    seen_note_ids = set()
    for n in notes:
        _collect_unique_note(n, thread_note_ids, seen_note_ids, normalized_notes)
    for d in discussions:
        if d.get("individual_note") is True:
            for n in d.get("notes", []):
                _collect_unique_note(n, thread_note_ids, seen_note_ids, normalized_notes)
    return normalized_notes


def cmd_list(host, project, iid, timeout_s):
    head_sha, discussions, notes = read_census(host, project, iid, timeout_s)
    real_discussions = [d for d in discussions if not d.get("individual_note", False)]
    thread_note_ids = _extract_thread_note_ids(real_discussions)
    normalized_notes = normalize_census_notes(discussions, notes, thread_note_ids)
    print(json.dumps({
        "provider": PROVIDER,
        "host": host,
        "project": project,
        "iid": iid,
        "head_sha": head_sha,
        "discussions": real_discussions,
        "notes": normalized_notes,
        "coverage": {
            "discussions_fetched": len(real_discussions),
            "notes_fetched": len(normalized_notes),
            "raw_discussions_fetched": len(discussions),
            "raw_notes_fetched": len(notes),
            "discussions_complete": True,
            "notes_complete": True,
            "head_stable": True,
            "complete": True,
        },
    }, indent=2, sort_keys=True))


def cmd_thread(host, project, iid, timeout_s, note_id):
    head_sha, discussions, _ = read_census(host, project, iid, timeout_s)
    matches = []
    for discussion in discussions:
        for note in discussion.get("notes", []):
            if isinstance(note, dict) and type(note.get("id")) is int and note.get("id") == note_id:
                matches.append(discussion)
                break
    if not matches:
        raise HelperError(
            "note_not_found",
            f"note {note_id} is in no discussion of this census (root notes live outside threads)",
            {"note_id": note_id, "discussions_searched": len(discussions)},
        )
    if len(matches) > 1:
        raise HelperError(
            "ambiguous_note",
            f"note {note_id} appears in {len(matches)} discussions; refusing to guess",
            {"note_id": note_id,
             "discussion_ids": [d.get("id") for d in matches if isinstance(d, dict)]},
        )
    discussion = matches[0]
    print(json.dumps({
        "provider": PROVIDER,
        "host": host,
        "project": project,
        "iid": iid,
        "head_sha": head_sha,
        "note_id": note_id,
        "discussion_id": discussion.get("id"),
        "discussion": discussion,
    }, indent=2, sort_keys=True))


def read_body_file(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            body_text = handle.read()
    except OSError as err:
        raise HelperError(
            "body_read_failed",
            f"cannot read body file {path}: {err}",
            {"body_file": path},
        ) from err
    except UnicodeDecodeError as err:
        raise HelperError(
            "body_read_failed",
            f"body file {path} is not valid UTF-8",
            {"body_file": path},
        ) from err
    if not body_text.strip():
        raise HelperError(
            "empty_body",
            f"body file {path} is empty; refusing to post an empty reply",
            {"body_file": path},
        )
    return body_text


def _raise_head_mismatch(current_head, expected_head):
    raise HelperError(
        "head_mismatch",
        f"MR head {current_head} does not match expected head {expected_head}; refusing to write",
        {"head_before": current_head, "expected_head": expected_head},
    )


def _fetch_discussion(host, endpoint, discussion_id, timeout_s):
    obj = fetch_single_object(host, endpoint, timeout_s)
    if obj.get("id") != discussion_id:
        raise HelperError(
            "wrong_identity",
            f"discussion identity mismatch: asked for {discussion_id!r}, got {obj.get('id')!r}",
            {"endpoint": endpoint, "discussion_id": discussion_id},
        )
    return obj


def _execute_mutation(argv, timeout_s, endpoint, discussion_id, op_name):
    action_verb = "re-post" if "POST" in op_name else "re-resolve"
    try:
        proc = _run(argv, timeout_s, endpoint)
        _refuse_failed(proc, endpoint)
        return _parse_json(proc.stdout, endpoint)
    except HelperError as err:
        raise HelperError(
            err.code,
            f"{err.message}; {op_name} was attempted; outcome unknown; do not {action_verb}",
            {"endpoint": endpoint, "discussion_id": discussion_id,
             "mutation_attempted": True, "outcome_unknown": True, "retryable": False,
             **err.details},
        ) from err


def _cleanup_temp_file(path):
    if path:
        try:
            os.unlink(path)
        except OSError as err:
            print(f"warning: could not remove temp file {path}: {err}", file=sys.stderr)


def _validate_reply_receipt(receipt, endpoint, discussion_id, mr_obj):
    if not isinstance(receipt, dict) or type(receipt.get("id")) is not int:
        raise HelperError(
            "missing_receipt",
            f"reply POST returned no note id for discussion {discussion_id!r}; "
            f"mutation attempt was made, outcome unknown; do not re-post",
            {"endpoint": endpoint, "discussion_id": discussion_id,
             "mutation_attempted": True, "outcome_unknown": True, "retryable": False},
        )
    for key, want in (("project_id", mr_obj.get("project_id")), ("noteable_id", mr_obj.get("id"))):
        got = receipt.get(key)
        if type(got) is not int or type(want) is not int or got != want:
            raise HelperError(
                "wrong_identity",
                f"reply POST receipt {key} {got!r} is outside the requested scope ({want!r}); do not re-post",
                {"endpoint": endpoint, "discussion_id": discussion_id,
                 "note_id": receipt.get("id"), "mutation_attempted": True,
                 "outcome_unknown": True, "retryable": False},
            )
    return receipt["id"]


def _verify_readback_reply(host, single, timeout_s, discussion_id, note_id):
    try:
        after = fetch_single_object(host, single, timeout_s)
    except HelperError as err:
        raise HelperError(
            err.code,
            f"{err.message}; reply was accepted as note {note_id}, do not re-post",
            {"discussion_id": discussion_id, "note_id": note_id,
             "mutation_attempted": True, "outcome_unknown": True, "retryable": False, **err.details},
        ) from err
    if after.get("id") != discussion_id:
        raise HelperError(
            "wrong_identity",
            f"read-back discussion identity mismatch: asked for {discussion_id!r}, "
            f"got {after.get('id')!r}; reply was accepted as note {note_id}, do not re-post",
            {"endpoint": single, "discussion_id": discussion_id, "note_id": note_id,
             "mutation_attempted": True, "outcome_unknown": True, "retryable": False},
        )
    after_notes = after.get("notes")
    if not isinstance(after_notes, list) or not any(
            isinstance(n, dict) and type(n.get("id")) is int and n.get("id") == note_id for n in after_notes):
        raise HelperError(
            "readback_mismatch",
            f"reply was accepted as note {note_id} but is absent on read-back; do not re-post",
            {"discussion_id": discussion_id, "note_id": note_id,
             "mutation_attempted": True, "outcome_unknown": True, "retryable": False},
        )


def _verify_post_mutation_head(mr_target, head_before, discussion_id, note_id=None):
    host, project, iid, timeout_s = mr_target
    action = f"reply was accepted as note {note_id}" if note_id is not None else f"resolve was accepted for {discussion_id!r}"
    verb = "do not re-post" if note_id is not None else "do not re-resolve"
    details = {
        "discussion_id": discussion_id,
        "mutation_attempted": True,
        "outcome_unknown": True,
        "retryable": False,
    }
    if note_id is not None:
        details["note_id"] = note_id
    try:
        _, head_after = get_mr(host, project, iid, timeout_s)
    except HelperError as err:
        raise HelperError(
            err.code,
            f"{err.message}; {action}, {verb}",
            {**details, **err.details},
        ) from err
    if head_before != head_after:
        raise HelperError(
            "head_changed",
            f"{action} but MR head moved ({head_before} -> {head_after}); {verb}",
            {**details, "head_before": head_before, "head_after": head_after},
        )
    return head_after


def cmd_reply(host, project, iid, timeout_s, discussion_id, body_file, expected_head):
    body_text = read_body_file(body_file)
    mr_obj, head_before = get_mr(host, project, iid, timeout_s)
    if head_before != expected_head:
        _raise_head_mismatch(head_before, expected_head)
    base = f"projects/{quote(project, safe='')}/merge_requests/{iid}"
    single = f"{base}/discussions/{quote(discussion_id, safe='')}"
    _fetch_discussion(host, single, discussion_id, timeout_s)
    endpoint = f"{single}/notes"
    tmp_path = ""
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                         delete=False, encoding="utf-8") as tmp:
            json.dump({"body": body_text}, tmp)
            tmp_path = tmp.name
        argv = ["glab", "api", "--hostname", host, endpoint, "-X", "POST",
                "--input", tmp_path, "--output", "json"]
        receipt = _execute_mutation(argv, timeout_s, endpoint, discussion_id, "reply POST")
    finally:
        _cleanup_temp_file(tmp_path)
    note_id = _validate_reply_receipt(receipt, endpoint, discussion_id, mr_obj)
    _verify_readback_reply(host, single, timeout_s, discussion_id, note_id)
    mr_target = (host, project, iid, timeout_s)
    head_after = _verify_post_mutation_head(mr_target, head_before, discussion_id, note_id)
    print(json.dumps({
        "provider": PROVIDER,
        "host": host,
        "project": project,
        "iid": iid,
        "head_sha": head_after,
        "discussion_id": discussion_id,
        "note_id": note_id,
        "accepted": True,
        "readback": True,
        "note": receipt,
    }, indent=2, sort_keys=True))


def _is_unusable_note_entry(entry):
    if not isinstance(entry, dict) or type(entry.get("id")) is not int:
        return True
    if type(entry.get("resolvable")) is not bool:
        return True
    if entry.get("resolvable") is True and type(entry.get("resolved")) is not bool:
        return True
    return False


def _check_pre_resolve_notes(current, endpoint, discussion_id):
    thread_notes = current.get("notes")
    if not isinstance(thread_notes, list) or not thread_notes:
        raise HelperError(
            "malformed_payload",
            f"discussion {discussion_id!r} carries no notes array; resolvability unknown",
            {"endpoint": endpoint, "discussion_id": discussion_id},
        )
    for entry in thread_notes:
        if _is_unusable_note_entry(entry):
            raise HelperError(
                "malformed_payload",
                f"discussion {discussion_id!r} holds an unusable note entry; resolvability unknown",
                {"endpoint": endpoint, "discussion_id": discussion_id},
            )
    return thread_notes


def _validate_resolve_receipt(updated, endpoint, discussion_id):
    if not isinstance(updated, dict):
        raise HelperError(
            "missing_receipt",
            f"resolve PUT returned no discussion object for {discussion_id!r}; "
            f"mutation attempt was made, outcome unknown; do not re-resolve",
            {"endpoint": endpoint, "discussion_id": discussion_id,
             "mutation_attempted": True, "outcome_unknown": True, "retryable": False},
        )
    if updated.get("id") != discussion_id:
        raise HelperError(
            "wrong_identity",
            f"resolve PUT returned discussion {updated.get('id')!r}, not {discussion_id!r}; "
            f"mutation attempt was made, outcome unknown; do not re-resolve",
            {"endpoint": endpoint, "discussion_id": discussion_id,
             "mutation_attempted": True, "outcome_unknown": True, "retryable": False},
        )
    updated_notes = updated.get("notes")
    if not isinstance(updated_notes, list) or not updated_notes:
        raise HelperError(
            "missing_receipt",
            f"resolve PUT response for {discussion_id!r} carries no notes array to confirm; "
            f"mutation attempt was made, outcome unknown; do not re-resolve",
            {"endpoint": endpoint, "discussion_id": discussion_id,
             "mutation_attempted": True, "outcome_unknown": True, "retryable": False},
        )
    for entry in updated_notes:
        if _is_unusable_note_entry(entry):
            raise HelperError(
                "malformed_payload",
                f"resolve PUT response for {discussion_id!r} holds an unusable note entry; "
                f"mutation attempt was made, outcome unknown; do not re-resolve",
                {"endpoint": endpoint, "discussion_id": discussion_id,
                 "mutation_attempted": True, "outcome_unknown": True, "retryable": False},
            )
    resolvable_updated = [entry for entry in updated_notes if entry.get("resolvable") is True]
    if not resolvable_updated or not all(entry.get("resolved") is True for entry in resolvable_updated):
        raise HelperError(
            "missing_receipt",
            f"resolve PUT response does not confirm resolution of {discussion_id!r}; "
            f"mutation attempt was made, outcome unknown; do not re-resolve",
            {"endpoint": endpoint, "discussion_id": discussion_id,
             "mutation_attempted": True, "outcome_unknown": True, "retryable": False},
        )


def _verify_readback_resolve(host, single, timeout_s, discussion_id):
    try:
        after = fetch_single_object(host, single, timeout_s)
    except HelperError as err:
        raise HelperError(
            err.code,
            f"{err.message}; resolve was accepted for {discussion_id!r}, do not re-resolve",
            {"discussion_id": discussion_id, "mutation_attempted": True,
             "outcome_unknown": True, "retryable": False, **err.details},
        ) from err
    if after.get("id") != discussion_id:
        raise HelperError(
            "wrong_identity",
            f"read-back discussion identity mismatch: asked for {discussion_id!r}, "
            f"got {after.get('id')!r}; resolve was accepted; do not re-resolve",
            {"endpoint": single, "discussion_id": discussion_id,
             "mutation_attempted": True, "outcome_unknown": True, "retryable": False},
        )
    after_notes = after.get("notes")
    if not isinstance(after_notes, list) or not after_notes:
        raise HelperError(
            "malformed_payload",
            f"read-back discussion {discussion_id!r} carries no notes array; do not re-resolve",
            {"endpoint": single, "discussion_id": discussion_id,
             "mutation_attempted": True, "outcome_unknown": True, "retryable": False},
        )
    for entry in after_notes:
        if _is_unusable_note_entry(entry):
            raise HelperError(
                "malformed_payload",
                f"read-back discussion {discussion_id!r} holds an unusable note entry; do not re-resolve",
                {"endpoint": single, "discussion_id": discussion_id,
                 "mutation_attempted": True, "outcome_unknown": True, "retryable": False},
            )
    resolvable_after = [entry for entry in after_notes if entry.get("resolvable") is True]
    if not resolvable_after or not all(entry.get("resolved") is True for entry in resolvable_after):
        raise HelperError(
            "readback_mismatch",
            f"resolve was accepted for {discussion_id!r} but read-back is unresolved; do not re-resolve",
            {"discussion_id": discussion_id, "mutation_attempted": True,
             "outcome_unknown": True, "retryable": False},
        )


def cmd_resolve(host, project, iid, timeout_s, discussion_id, expected_head):
    _, head_before = get_mr(host, project, iid, timeout_s)
    if head_before != expected_head:
        _raise_head_mismatch(head_before, expected_head)
    base = f"projects/{quote(project, safe='')}/merge_requests/{iid}"
    single = f"{base}/discussions/{quote(discussion_id, safe='')}"
    current = _fetch_discussion(host, single, discussion_id, timeout_s)
    thread_notes = _check_pre_resolve_notes(current, single, discussion_id)
    resolvable = [entry for entry in thread_notes if entry.get("resolvable") is True]
    if not resolvable:
        raise HelperError(
            "nonresolvable",
            f"discussion {discussion_id!r} has no resolvable notes; refusing to resolve",
            {"endpoint": single, "discussion_id": discussion_id},
        )
    if all(n.get("resolved") is True for n in resolvable):
        print(json.dumps({
            "provider": PROVIDER,
            "host": host,
            "project": project,
            "iid": iid,
            "head_sha": head_before,
            "discussion_id": discussion_id,
            "resolved": True,
            "mutated": False,
        }, indent=2, sort_keys=True))
        return
    endpoint = f"{single}?resolved=true"
    argv = ["glab", "api", "--hostname", host, endpoint, "-X", "PUT", "--output", "json"]
    updated = _execute_mutation(argv, timeout_s, endpoint, discussion_id, "resolve PUT")
    _validate_resolve_receipt(updated, endpoint, discussion_id)
    _verify_readback_resolve(host, single, timeout_s, discussion_id)
    mr_target = (host, project, iid, timeout_s)
    head_after = _verify_post_mutation_head(mr_target, head_before, discussion_id)
    print(json.dumps({
        "provider": PROVIDER,
        "host": host,
        "project": project,
        "iid": iid,
        "head_sha": head_after,
        "discussion_id": discussion_id,
        "resolved": True,
        "mutated": True,
    }, indent=2, sort_keys=True))


def build_parser():
    parser = argparse.ArgumentParser(
        description="GitLab merge-request review helper (read census, thread lookup, reply, resolve)")
    parser.add_argument("--host", required=True, help="GitLab hostname, e.g. gitlab.com")
    parser.add_argument("--project", required=True, help="GitLab project path, e.g. group/subgroup/project")
    parser.add_argument("--mr", required=True, help="Merge request IID (integer)")
    parser.add_argument("--timeout", default=DEFAULT_TIMEOUT_S,
                        help=f"Per-subprocess timeout in seconds (default {DEFAULT_TIMEOUT_S})")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    subparsers.add_parser("list", help="Fetch census of discussions and notes")

    thread_p = subparsers.add_parser("thread", help="Look up a thread discussion by note id")
    thread_p.add_argument("--note", required=True, help="Note ID (integer)")

    reply_p = subparsers.add_parser("reply", help="Reply to a discussion")
    reply_p.add_argument("--discussion", required=True, help="Discussion ID")
    reply_p.add_argument("--body-file", required=True, help="Path to a file containing the reply text")
    reply_p.add_argument("--expected-head", required=True,
                         help="Expected MR head commit SHA; refusing to post if head has moved")

    resolve_p = subparsers.add_parser("resolve", help="Resolve a discussion")
    resolve_p.add_argument("--discussion", required=True, help="Discussion ID")
    resolve_p.add_argument("--expected-head", required=True,
                           help="Expected MR head commit SHA; refusing to resolve if head has moved")
    return parser


def _dispatch_subcommand(args, host, project, iid, timeout_s):
    sub = args.subcommand
    if sub == "list":
        cmd_list(host, project, iid, timeout_s)
        return True
    if sub == "thread":
        cmd_thread(host, project, iid, timeout_s, check_note_id(args.note))
        return True
    if sub == "reply":
        cmd_reply(
            host, project, iid, timeout_s,
            check_discussion(args.discussion),
            args.body_file,
            check_expected_head(args.expected_head),
        )
        return True
    if sub == "resolve":
        cmd_resolve(
            host, project, iid, timeout_s,
            check_discussion(args.discussion),
            check_expected_head(args.expected_head),
        )
        return True
    return False


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        host = check_host(args.host)
        project = check_project(args.project)
        iid = check_iid(args.mr)
        timeout_s = check_timeout(args.timeout)
        if not _dispatch_subcommand(args, host, project, iid, timeout_s):
            parser.print_help(file=sys.stderr)
            return 2
    except HelperError as err:
        host = args.host
        project = args.project
        raw_iid = args.mr
        try:
            iid = int(raw_iid)
        except ValueError:
            iid = raw_iid
        emit_error(err, host, project, iid)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
