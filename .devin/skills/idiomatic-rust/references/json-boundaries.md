# JSON Boundaries: Representations, Tagged Enums, and Lossless Decodes

Changing how a value looks on the wire is not a formatting choice. List every role the representation plays before touching it.

## Map the contracts before changing anything

Inventory numeric range and equality, object ordering and duplicate-key handling, raw-fragment fidelity, null transitions, control identifiers, error mapping, and full-input rejection. If any of these is contractual, the new representation must honor it too.

## Keep semantic and byte-exact preservation apart

Preserving a value's meaning is not the same as preserving the exact bytes of an opaque raw fragment. Decide which one each consumer needs, and hold the line on raw bytes only where a consumer depends on them.

## Check installed versions before reaching for workarounds

Crate-specific behavior moves with serializer and deserializer versions and feature flags. Confirm the installed versions before using a workaround that only holds for one version.

## Raw values inside tagged enums need special care

Check whether derived or manual buffering still leaves the original raw token reachable, including transitive member subtrees. A fresh per-variant decode fits only while discriminator handling, duplicate-field behavior, unknown-tag handling, and error behavior stay contractual.

## Check the conversion chain, not the macro name

For DOM conversion, verify both that parsing ran to completion and the concrete serializer chain that follows. Never assume a macro or adapter preserves raw fragments or large numbers just because of its name.

## Convert only where the change applies

Centralize conversion at the affected boundaries. Do not add new text round-trips at sites the change does not touch.

## Prove the change against real traffic

Exercise real producers and consumers with representative raw-bearing variants, large numbers, malformed trailing input, control identifiers, and state transitions. Hold three predicates over that traffic: decoded values stay equal including numeric range, raw fragments stay byte-identical wherever a consumer depends on them, and trailing input is rejected. Break the decode on purpose (drop a discriminator branch, accept a duplicate field, swallow an unknown tag, remap an error) and require at least one predicate to fail. A run that only renames fixtures, narrows filters, or changes inputs to match proves nothing.

## Remove the old path after cutover

Once consumers have moved, delete the obsolete representation paths. Enforce any requested dependency ban through the project's current mechanism.
