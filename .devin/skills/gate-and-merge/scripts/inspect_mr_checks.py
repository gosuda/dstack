#!/usr/bin/env python3
"""Inspect failing GitLab merge-request CI via the glab API.

Binds an explicit HOST, project path, and MR IID, resolves the MR head SHA,
selects the current head pipeline, lists its jobs (paginated), and extracts
failure snippets from failed-job traces.

Read-only: issues GET requests plus single-job trace reads only. It never
retries, reruns, cancels, creates, or deletes pipelines or jobs, and it never
prints credential values. Every transport hop is a single bounded attempt
(SUBPROCESS_TIMEOUT) that fails closed with a zero-retry budget.

Exit status: 0 only for verified green (head-pipeline success with matching
head SHA, passing jobs, and no unresolved required jobs). 1 when the head
pipeline has required failed jobs or the helper itself fails. 2 when the state
is indeterminate (running, missing, skipped, or unrelated pipelines). A nonzero
exit never means green; in particular, the absence of failed jobs is not
success.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path
from urllib.parse import quote

JsonDict = dict[str, "JsonValue"]
JsonList = list["JsonValue"]
JsonValue = JsonDict | JsonList | str | int | float | bool | None
FAILURE_MARKERS = (
    "error",
    "fail",
    "failed",
    "traceback",
    "exception",
    "assert",
    "panic",
    "fatal",
    "timeout",
    "segmentation fault",
)

DEFAULT_MAX_LINES = 160
DEFAULT_CONTEXT_LINES = 30
PENDING_TRACE_MARKERS = (
    "still in progress",
    "log will be available when it is complete",
    "job is still running",
)

FAILED_JOB_STATUSES = {"failed"}
SKIPPED_JOB_STATUSES = {"canceled", "skipped", "manual"}
TERMINAL_JOB_STATUSES = ("success", *FAILED_JOB_STATUSES, *SKIPPED_JOB_STATUSES)

INDETERMINATE_VERDICTS = ("missing", "unrelated", "running", "skipped")

MISSING_HEAD_NOTE = "MR exposes no head SHA; no pipeline can be bound to it."
MISSING_PIPELINE_NOTE = (
    "The MR records no head pipeline; no CI is bound to the current "
    "revision, never green.")
UNRELATED_PIPELINE_NOTE = (
    "The MR head moved past its recorded head pipeline; "
    "that pipeline is unrelated to the current revision, never green.")
INCOMPLETE_JOBS_NOTE = (
    "Pipeline jobs include incomplete work; incomplete checks are not "
    "diagnosed, never green.")

SUBPROCESS_TIMEOUT = 120


def run_glab_raw(args: Sequence[str], cwd: Path) -> tuple[int, bytes, str]:
    """Run glab once under a hard timeout; transport faults fail closed."""
    try:
        process = subprocess.run(
            ["glab", *args],
            cwd=cwd,
            capture_output=True,
            timeout=SUBPROCESS_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return 1, b"", "glab command timed out."
    except FileNotFoundError:
        return 1, b"", "glab executable not found on PATH."
    return (process.returncode, process.stdout,
            process.stderr.decode(errors="replace"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect GitLab MR CI: bind host/project/MR IID, select the head "
            "pipeline, list jobs, and extract failed-job log snippets."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--host", required=True, help="GitLab hostname.")
    parser.add_argument(
        "--project",
        required=True,
        help="Project path GROUP/PROJECT (URL-encoded by the helper).",
    )
    parser.add_argument("--mr", required=True, help="Merge request IID.")
    parser.add_argument(
        "--repo",
        default=".",
        help="Working directory; used as subprocess cwd only.",
    )
    parser.add_argument(
        "--json", action="store_true", help="Emit JSON instead of text output."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = bind_target(args)
    if target is None:
        return 1
    cwd, iid, project = target
    mr = fetch_mr(args.host, project, iid, cwd)
    if mr is None:
        return 1
    head_sha = extract_head_sha(mr)
    pipeline, verdict, note = select_head_pipeline(mr, head_sha)
    summary = summarize(args, mr, head_sha, verdict, pipeline, note)
    if pipeline is None or verdict in INDETERMINATE_VERDICTS:
        emit(args, summary, [])
        return 2

    jobs = fetch_pipeline_jobs(args.host, project, pipeline_id(pipeline), cwd)
    if jobs is None:
        return 1
    jobs_verdict, jobs_note = completed_pipeline_jobs_verdict(jobs)
    outcome = resolve_outcome(verdict, jobs_verdict)
    if outcome == "green":
        emit(args, summary, summarize_jobs(jobs))
        return 0
    if outcome != "failed":
        summary["verdict"] = outcome
        summary["note"] = jobs_note
        emit(args, summary, summarize_jobs(jobs))
        return 2
    summary["verdict"] = "failed"
    results = failed_job_analyses(args, project, cwd, jobs)
    summary["note"] = failure_note(jobs_verdict, jobs_note, note, pipeline,
                                   len(results))
    emit(args, summary, results or summarize_jobs(jobs))
    return 1


def bind_target(args: argparse.Namespace) -> tuple[Path, int, str] | None:
    """Resolve the repo cwd, gate on glab auth, and bind the MR identity."""
    cwd = resolve_cwd(Path(args.repo))
    if cwd is None:
        print("Error: --repo is not a directory.", file=sys.stderr)
        return None
    if not ensure_glab_available(cwd, args.host):
        return None
    iid = parse_iid(args.mr)
    if iid is None:
        return None
    return cwd, iid, encode_project(args.project)


def parse_iid(raw: str) -> int | None:
    try:
        return int(str(raw).strip())
    except ValueError:
        print(f"Error: --mr must be a numeric IID, got {raw!r}.",
              file=sys.stderr)
        return None


def resolve_cwd(repo: Path) -> Path | None:
    if not repo.exists() or not repo.is_dir():
        return None
    return repo.resolve()


def ensure_glab_available(cwd: Path, host: str) -> bool:
    returncode, stdout, stderr = run_glab_raw(
        ["auth", "status", "--hostname", host], cwd=cwd)
    if returncode != 0:
        message = "\n".join(
            filter(None, [stderr, stdout.decode(errors="replace")])).strip()
        print(message or f"Error: glab auth failed for host {host}. "
              "Run glab auth login --hostname HOST.", file=sys.stderr)
        return False
    return True


def encode_project(project: str) -> str:
    return quote(project.strip(), safe="")


def parse_json_payload(text: str) -> JsonValue | None:
    """Parse one JSON document, falling back to concatenated JSON lines."""
    try:
        return json.loads(text or "null")
    except json.JSONDecodeError:
        return parse_json_lines(text)


def parse_json_lines(text: str) -> JsonList | None:
    payload: JsonList = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload.append(json.loads(line))
        except json.JSONDecodeError:
            print("Error: unable to parse API JSON payload.", file=sys.stderr)
            return None
    return payload


def api_get(host: str, endpoint: str, cwd: Path,
            paginate: bool) -> JsonValue | None:
    args = ["api", "--hostname", host, endpoint, "--output", "json"]
    if paginate:
        args.append("--paginate")
    returncode, payload, stderr = run_glab_raw(args, cwd=cwd)
    if returncode != 0:
        message = (stderr or payload.decode(errors="replace") or "").strip()
        print(message or f"Error: glab api {endpoint} failed.",
              file=sys.stderr)
        return None
    return parse_json_payload(payload.decode(errors="replace"))


def fetch_mr(host: str, project: str, iid: int,
             cwd: Path) -> JsonDict | None:
    data = api_get(host, f"projects/{project}/merge_requests/{iid}",
                   cwd, paginate=False)
    if not isinstance(data, dict):
        print("Error: unexpected MR JSON shape.", file=sys.stderr)
        return None
    return data


def select_head_pipeline(
    mr: JsonDict,
    head_sha: str,
) -> tuple[JsonDict | None, str, str]:
    """Bind the declared head pipeline to the current MR revision, or refuse."""
    if not head_sha:
        return None, "missing", MISSING_HEAD_NOTE
    declared = mr.get("head_pipeline")
    if not isinstance(declared, dict):
        return None, "missing", MISSING_PIPELINE_NOTE
    raw_id = declared.get("id")
    if type(raw_id) is not int or raw_id <= 0:
        return None, "missing", MISSING_PIPELINE_NOTE
    if pipeline_sha(declared) != head_sha:
        return declared, "unrelated", UNRELATED_PIPELINE_NOTE
    return classify_pipeline(declared)


def is_valid_job(job: JsonValue) -> bool:
    if not isinstance(job, dict):
        return False
    job_id = job.get("id")
    if type(job_id) is not int or job_id <= 0:
        return False
    status = job.get("status")
    return isinstance(status, str) and bool(status.strip())


def fetch_pipeline_jobs(host: str, project: str, pipeline_id_value: JsonValue,
                        cwd: Path) -> list[JsonDict] | None:
    if type(pipeline_id_value) is not int or pipeline_id_value <= 0:
        print(f"Error: pipeline ID must be a positive integer, got {pipeline_id_value!r}.",
              file=sys.stderr)
        return None
    data = api_get(
        host, f"projects/{project}/pipelines/{pipeline_id_value}/jobs",
        cwd, paginate=True)
    if data is None:
        return None
    if not isinstance(data, list):
        print("Error: unexpected jobs JSON shape.", file=sys.stderr)
        return None
    items: list[JsonValue] = []
    for entry in data:
        if isinstance(entry, list):
            items.extend(entry)
        else:
            items.append(entry)
    jobs: list[JsonDict] = []
    for item in items:
        if not is_valid_job(item) or not isinstance(item, dict):
            print("Error: unexpected jobs JSON shape.", file=sys.stderr)
            return None
        jobs.append(item)
    return jobs


def extract_head_sha(mr: JsonDict) -> str:
    sha = mr.get("sha")
    if isinstance(sha, str) and sha.strip():
        return sha.strip()
    return ""


def pipeline_sha(pipeline: JsonDict) -> str:
    return str(pipeline.get("sha") or "")


def pipeline_id(pipeline: JsonDict) -> JsonValue:
    return pipeline.get("id")


def pipeline_status(pipeline: JsonDict) -> str:
    return normalize(pipeline.get("status"))


def job_status(job: JsonDict) -> str:
    return normalize(job.get("status"))


def classify_pipeline(
    pipeline: JsonDict,
) -> tuple[JsonDict | None, str, str]:
    status = pipeline_status(pipeline)
    if status == "success":
        return pipeline, "green", ""
    if status == "failed":
        return (pipeline, "failed",
                f"Head pipeline {pipeline_id(pipeline)} reported failure.")
    if status in SKIPPED_JOB_STATUSES:
        return (pipeline, "skipped",
                f"Head pipeline {pipeline_id(pipeline)} ended as {status}; "
                "a skipped pipeline is not a pass.")
    return (pipeline, "running",
            f"Head pipeline {pipeline_id(pipeline)} is {status or 'unknown'}; "
            "incomplete checks are not diagnosed.")


def is_allow_failure(job: JsonDict) -> bool:
    return job.get("allow_failure") is True


def is_failed_job(job: JsonDict) -> bool:
    return job_status(job) in FAILED_JOB_STATUSES


def is_incomplete_job(job: JsonDict) -> bool:
    return job_status(job) not in TERMINAL_JOB_STATUSES


def authoritative_ci_jobs(jobs: list[JsonDict]) -> list[JsonDict]:
    return [job for job in jobs if not is_allow_failure(job)]


def completed_pipeline_jobs_verdict(jobs: list[JsonDict]) -> tuple[str, str]:
    """Verdict a completed pipeline: green demands real passing required work."""
    if not jobs:
        return ("missing",
                "Pipeline returned no jobs; no CI is proven, never green.")
    passing = [job for job in jobs if job_status(job) == "success"]
    if not passing:
        return verdict_without_passing_jobs(jobs)
    return required_gate_verdict(authoritative_ci_jobs(jobs))


def verdict_without_passing_jobs(jobs: list[JsonDict]) -> tuple[str, str]:
    """No job passed: the run proves nothing; incomplete work is undiagnosed."""
    if any(is_incomplete_job(job) for job in jobs):
        return ("running", INCOMPLETE_JOBS_NOTE)
    failed = [job for job in jobs if is_failed_job(job)]
    if not failed:
        return ("skipped",
                "Pipeline returned only skipped jobs; a skipped set is not a "
                "pass, never green.")
    required_failed = authoritative_ci_jobs(failed)
    if required_failed:
        return ("failed",
                f"Required jobs failed ({len(required_failed)} failed); "
                "never green.")
    return ("failed",
            f"No jobs passed and {len(failed)} failed (all optional); "
            "without passing checks, failures cannot be overlooked, "
            "never green.")


def required_gate_verdict(required: list[JsonDict]) -> tuple[str, str]:
    """Required jobs gate green: failure blocks, incomplete is undiagnosed."""
    required_failed = [job for job in required if is_failed_job(job)]
    if required_failed:
        return ("failed",
                f"Required jobs failed ({len(required_failed)} failed); "
                "never green.")
    if any(is_incomplete_job(job) for job in required):
        return ("running", INCOMPLETE_JOBS_NOTE)
    if any(job_status(job) in SKIPPED_JOB_STATUSES for job in required):
        return ("skipped",
                "Required jobs were skipped or canceled; a skipped required "
                "check is not a pass, never green.")
    if not any(job_status(job) == "success" for job in required):
        return ("missing",
                "Pipeline returned no passing required jobs; no required CI "
                "is proven, never green.")
    return ("green", "")


def resolve_outcome(verdict: str, jobs_verdict: str) -> str:
    """Merge verdicts: a required job failure overrides cached success."""
    if verdict == "failed" or jobs_verdict == "failed":
        return "failed"
    if jobs_verdict == "green":
        return "green"
    return jobs_verdict


def job_identity(job: JsonDict) -> JsonDict:
    """Project the typed identity fields every job record carries."""
    return {
        "name": job.get("name", ""),
        "jobId": job.get("id"),
        "stage": job.get("stage", ""),
        "status": job_status(job),
    }


def analyze_job(
    job: JsonDict,
    host: str,
    project: str,
    cwd: Path,
    max_lines: int,
    context: int,
) -> JsonDict:
    base = job_identity(job)
    pipeline_ref = job.get("pipeline")
    base["pipelineId"] = (pipeline_ref.get("id")
                          if isinstance(pipeline_ref, dict) else pipeline_ref)
    base["webUrl"] = job.get("web_url", "")
    if is_allow_failure(job):
        base["allow_failure"] = True
    log_text, log_error = fetch_job_trace(host, project, base["jobId"], cwd)
    if log_error and is_pending_message(log_error):
        base["log_status"] = "log_pending"
        base["note"] = log_error
    elif log_error:
        base["log_status"] = "log_unavailable"
        base["error"] = log_error
    else:
        base["log_status"] = "ok"
        base["logSnippet"] = extract_failure_snippet(
            log_text, max_lines=max_lines, context=context)
        base["logTail"] = tail_lines(log_text, max_lines)
    return base


def fetch_job_trace(host: str, project: str, job_id: JsonValue,
                    cwd: Path) -> tuple[str, str]:
    returncode, payload, stderr = run_glab_raw(
        ["api", "--hostname", host, f"projects/{project}/jobs/{job_id}/trace"],
        cwd=cwd,
    )
    if returncode != 0:
        message = (stderr or payload.decode(errors="replace")).strip()
        return "", message or "glab api job trace failed"
    return payload.decode(errors="replace"), ""


def failed_job_analyses(args: argparse.Namespace, project: str, cwd: Path,
                        jobs: list[JsonDict]) -> list[JsonDict]:
    """Fetch and snippet each failed job's trace, one bounded read per job."""
    return [
        analyze_job(
            job,
            host=args.host,
            project=project,
            cwd=cwd,
            max_lines=DEFAULT_MAX_LINES,
            context=DEFAULT_CONTEXT_LINES,
        )
        for job in jobs
        if is_failed_job(job)
    ]


def failure_note(jobs_verdict: str, jobs_note: str, pipeline_note: str,
                 pipeline: JsonDict, analyzed: int) -> str:
    """Pick the failed-verdict note: job evidence outranks boilerplate."""
    if jobs_verdict == "failed" and jobs_note:
        return jobs_note
    if analyzed:
        return f"{analyzed} failed jobs analyzed."
    return (jobs_note
            or pipeline_note
            or f"Head pipeline {pipeline_id(pipeline)} reported failure.")


def summarize_jobs(jobs: list[JsonDict]) -> list[JsonDict]:
    out: list[JsonDict] = []
    for job in jobs:
        entry = job_identity(job)
        if is_allow_failure(job):
            entry["allow_failure"] = True
        if job.get("web_url"):
            entry["webUrl"] = job.get("web_url")
        out.append(entry)
    return out


def normalize(value: JsonValue) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return ""
    return str(value).strip().lower()


def is_pending_message(message: str) -> bool:
    lowered = message.lower()
    return any(marker in lowered for marker in PENDING_TRACE_MARKERS)


def extract_failure_snippet(log_text: str, max_lines: int,
                            context: int) -> str:
    lines = log_text.splitlines()
    if not lines:
        return ""
    marker_index = find_failure_index(lines)
    if marker_index is None:
        return "\n".join(lines[-max_lines:])
    start = max(0, marker_index - context)
    end = min(len(lines), marker_index + context)
    window = lines[start:end]
    if len(window) > max_lines:
        window = window[-max_lines:]
    return "\n".join(window)


def find_failure_index(lines: Sequence[str]) -> int | None:
    for idx in range(len(lines) - 1, -1, -1):
        lowered = lines[idx].lower()
        if any(marker in lowered for marker in FAILURE_MARKERS):
            return idx
    return None


def tail_lines(text: str, max_lines: int) -> str:
    if max_lines <= 0:
        return ""
    return "\n".join(text.splitlines()[-max_lines:])


def summarize(args: argparse.Namespace, mr: JsonDict, head_sha: str,
              verdict: str, pipeline: JsonDict | None, note: str) -> JsonDict:
    return {
        "provider": "gitlab",
        "host": args.host,
        "project": args.project,
        "iid": args.mr,
        "mr_state": mr.get("state", ""),
        "head_sha": head_sha,
        "verdict": verdict,
        "sha_match": pipeline is not None
        and pipeline_sha(pipeline) == head_sha,
        "pipeline": summarize_pipeline(pipeline),
        "note": note,
    }


def emit(args: argparse.Namespace, summary: JsonDict,
         results: Iterable[JsonDict]) -> None:
    record = dict(summary)
    record["results"] = list(results)
    if args.json:
        print(json.dumps(record, indent=2))
    else:
        render_results(record)


def summarize_pipeline(pipeline: JsonDict | None) -> JsonDict:
    if pipeline is None:
        return {}
    return {
        "id": pipeline.get("id"),
        "status": pipeline.get("status", ""),
        "sha": pipeline.get("sha", ""),
        "ref": pipeline.get("ref", ""),
        "source": pipeline.get("source", ""),
        "web_url": pipeline.get("web_url", ""),
    }


def render_results(record: JsonDict) -> None:
    print(f"MR !{record['iid']} on {record['host']}/{record['project']}: "
          f"verdict {record['verdict']}.")
    print(f"MR state: {record.get('mr_state', '')}")
    render_head_binding(record)
    pipeline = record.get("pipeline")
    if isinstance(pipeline, dict) and pipeline:
        render_pipeline_summary(pipeline)
    if record.get("note"):
        print(f"Note: {record['note']}")
    results = record.get("results")
    if not isinstance(results, list):
        results = []
    for result in results:
        if isinstance(result, dict):
            render_job_result(result)
    print("-" * 60)


def render_head_binding(record: JsonDict) -> None:
    head_sha = str(record.get("head_sha") or "")
    if head_sha:
        print(f"Head SHA: {head_sha[:12]} "
              f"(match: {'yes' if record.get('sha_match') else 'no'})")


def render_pipeline_summary(pipeline: JsonDict) -> None:
    print(f"Pipeline: {pipeline.get('id', '')} "
          f"({pipeline.get('status', '')})")
    if pipeline.get("ref") or pipeline.get("sha"):
        print(f"Pipeline ref/SHA: {pipeline.get('ref', '')} "
              f"{str(pipeline.get('sha', ''))[:12]}")
    if pipeline.get("web_url"):
        print(f"Pipeline URL: {pipeline['web_url']}")


def render_job_result(result: JsonDict) -> None:
    print("-" * 60)
    print(f"Job: {result.get('name', '')}")
    render_job_fields(result)
    if result.get("allow_failure"):
        print("Allowed to fail: yes")
    if result.get("error"):
        print(f"Error fetching logs: {result['error']}")
        return
    snippet = result.get("logSnippet") or ""
    if snippet:
        print("Failure snippet:")
        print(indent_block(str(snippet), prefix="  "))
    elif "logSnippet" in result:
        print("No snippet available.")


def render_job_fields(result: JsonDict) -> None:
    if result.get("jobId") is not None:
        print(f"Job ID: {result['jobId']}")
    for key, label in (("status", "Status"), ("stage", "Stage"),
                       ("webUrl", "Details"), ("note", "Note")):
        if result.get(key):
            print(f"{label}: {result[key]}")


def indent_block(text: str, prefix: str = "  ") -> str:
    return "\n".join(f"{prefix}{line}" for line in text.splitlines())


if __name__ == "__main__":
    raise SystemExit(main())
