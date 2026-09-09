<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# The command layer and the store

The authority for how a change reaches disk: what a command is, the single path every command takes, where validation happens, the shape of the stored record in outline, and how the store is written. It exists so that the invariant list in the [structural model](structural-model.md) is a property of the system rather than a hope. An invariant is only as strong as the narrowest path to disk; two paths mean two checkers, and two checkers drift.

It is not the catalogue of commands, which is the [command catalogue](command-catalogue.md), nor the automation server's tool surface ([automation server](automation-server.md)), nor the on-disk schema in detail ([persistence](persistence.md)), nor the layout engine.

---

## 1. One authority, one write path

Everything that changes a domain goes through one function. The window's menus, its dialogs, its glyph clicks, its drag-and-drop, and every tool of the automation server are callers of it, and there is no second way in.

The automation server runs inside the application process, so there is exactly one writer, and the two callers reach the same function rather than two copies of a library. The consequences are worth being explicit about, because they are what the rest of the document does not have to handle: no inter-process locking, no lease, no split-brain, and no protocol between the two callers. An agent can act only while the application is running, which is the arrangement in which the user watches the work happen.

The layering is three deep and each layer has one job. The **mutations** are pure functions of the shape `(record, …args) → nextRecord`; they know the model and nothing about storage. The **command layer** owns the sequence: load, parse, migrate, apply, validate, persist. The **store** owns the filesystem: path derivation, bounds checking, atomic replacement, and nothing about the model. A mutation that reached for a file, or a store that understood a node, would be the beginning of the second path this document exists to prevent.

## 2. There is no cached model

The command layer holds no in-memory copy of a domain. Every command reads the file, works, and writes it back.

This is worth stating as a decision rather than an omission, because the obvious design is the other one. Holding the model in memory buys speed and costs a cache-coherence rule, a rollback path for a write that fails after the in-memory apply succeeded, and a class of fault in which what is drawn and what is stored disagree. Reading per command costs one parse and one serialization of a domain, which at the scale this application works at is a millisecond or so, incurred once per user action rather than once per frame.

Three things fall out of it. Because the whole sequence from load to save runs under one lock (section 4), the window and the automation server cannot interleave inside an operation. An edit made out of band, by a text editor or a restored backup, cannot be missed, because the next command reads it; there is nothing to invalidate. And the undo pre-image is free, since the command already holds the record it loaded.

The renderer does hold an in-memory structure, its computed layout, but that is derived from the record and rebuilt when the record changes. It is not the authority and nothing reads back from it.

## 3. A command

A command is a name, a domain, and an argument list, with its provenance.

```
Command  { name, domain, args, origin, actor, revision? }
  name      a member of the catalogue
  domain    a domain id, its name, or its directory path
  args      the arguments the named mutation takes after the record
  origin    ui | automation
  actor     { kind: user | agent, name }   recorded on any log entry written
  revision  optional: the domain revision the caller last read
```

`revision` is the caller's statement of what it believes the record to be. When it is present and differs from the stored revision, the command is refused as `stale` before anything is applied: another writer has changed the domain since the caller read it, and a write computed against the old state must not land on the new one. The window passes the revision its drawing was rendered from, so a drop begun on one state and released on another is refused rather than landing somewhere the author did not aim. An agent passes the revision its last read returned. A caller that omits it is asserting that it has read afresh, and the command layer takes it at its word.

The result is one of two shapes and never both.

```
Ok       { record, revision, undoable }
Refused  { code, message }
```

`record` is the new record, which the caller renders; the automation server returns it as the agent's new ground truth so an agent never has to guess what its write produced. `revision` is the new revision.

Refusal codes are a small closed set, so a caller can branch on the code and show the message.

| Code | Meaning |
| --- | --- |
| `unknown_command` | the name is not in the catalogue |
| `scope_denied` | the automation server's configured tier does not include this command |
| `not_found` | the domain, or an id the arguments name, does not exist |
| `bad_arguments` | an argument is of the wrong shape or kind |
| `refused` | the mutation's own precondition failed; the message names the rule |
| `invalid` | the result failed the invariant check; the message names the invariant |
| `stale` | the caller's `revision` is not the stored revision |
| `read_failed` | the domain file could not be read or parsed |
| `write_failed` | a file could not be written |

The chrome's `Change not saved` dialog shows the message verbatim.

## 4. The pipeline

Ten steps, in order, under one lock held for the whole sequence so that no two commands interleave. Any step may refuse, and a refusal before step nine has touched no storage.

1. **Admit.** The command name is checked against the catalogue. For a command from the automation server, its scope tier is checked here (section 9). Refusals: `unknown_command`, `scope_denied`.
2. **Resolve the domain.** An id, a name, or a path becomes a directory. Refusal: `not_found`.
3. **Load.** The domain file's text is read. Refusal: `read_failed`.
4. **Parse and migrate.** The text is parsed by the tolerant reader and brought to the current schema version (section 6). Refusal: `read_failed` with the parser's own message.
5. **Check the revision.** If the command carries one and it differs from the loaded record's, refuse. Refusal: `stale`.
6. **Apply.** The named mutation runs against the loaded record and returns a new one. A mutation refuses by returning an error whose message is the user-facing explanation. Refusals: `bad_arguments`, `not_found`, `refused`.
7. **Validate.** The *result* is checked against every invariant in section 4 of the structural model. Refusal: `invalid`.
8. **Write note files**, if the command produces any, before the record that names them (section 7). Refusal: `write_failed`.
9. **Write the record**, atomically, with its revision incremented. Refusal: `write_failed`.
10. **Return and notify.** The undo slot is set if the command qualifies (section 8), and observers are told (section 10).

Two properties of this order are the point of it. Nothing is written until the result has been proved legal, so the stored record satisfies the invariants at every instant a reader could observe it. And because the pre-image is never mutated, a refusal at step six or seven needs no rollback: the working record is simply discarded.

## 5. Two kinds of validation, and why both

Step six and step seven check different things and neither replaces the other.

A mutation's own precondition asks whether the command makes sense: does this node exist, is it of a kind this operation accepts, is the target on the same workflow, would this leave a branch reaching out of its scope. It knows the operation's intent, so it can say what would have been legal instead, and its message is written for a person or an agent to act on.

The invariant check asks whether the result is a legal record at all. It knows nothing about the operation and is the same code for every command. Its job is to catch a mutation that is wrong rather than a command that is wrong, which is the class of defect that otherwise reaches disk and is discovered later as corruption.

So the precondition is the interface and the invariant check is the safety net. Remove the first and refusals become unhelpful; remove the second and a single faulty mutation silently writes an illegal record.

Both mutations and the validator read the stored record only. Neither may consult a derived index, since an index built from a broken record would make the broken record look consistent.

## 6. The record on disk

One file per domain, in the domain's own directory alongside its bookmarks file and its `notes/` directory. A domain is small enough that one file makes atomic replacement a single rename, which is the property worth optimising for. The schema in full is in the [persistence](persistence.md) document; the rules that shape the write path are these.

**Tolerant read, canonical write.** The reader accepts a permissive superset (unquoted keys, trailing commas, comments), so a file edited by hand still opens; every write from the application is strict, canonical JSON with a stable key order and a trailing newline. The asymmetry is deliberate: it costs nothing to accept more than one emits, and it means a hand-edited file is repaired rather than rejected.

**Canonical form.** Absent optional fields are omitted rather than written null, false booleans are omitted, and a gap whose four side lists are all empty is written as an empty object. That last one is most of the file: nearly every gap in a domain is an ordinary space between two nodes. The gap's identity and its position still come from the workflow's `gaps` list, which carries every gap id in order, so omitting the contents loses nothing.

**Schema version and migration.** The record carries a schema version. On load, a migration brings an older record to the current version, and the upgrade is written back exactly once, only when the migration changed something. A record whose version is newer than the application understands is refused rather than guessed at.

## 7. The write

The record is written to a temporary file in the destination directory, flushed to disk, and renamed over the target; the directory is then flushed so the rename itself survives a crash. Rename within one directory is the atomic primitive; a reader sees either the whole old file or the whole new one, never a partial write. On a platform whose rename does not replace an existing file, use its replace primitive rather than unlinking first, since unlink-then-rename has a window in which the file does not exist.

**Ordering against note files.** A command that writes note files writes them before the record that references them. A failure then leaves an unreferenced note file, which the structural model already treats as a legal orphan, rather than a node whose reference names a file that was never created. The reverse order has no such safe failure.

## 8. Undo

One slot, not a stack, holding the pre-image of the last human operation (D9).

The slot is set at step ten, and only when the command's `origin` is `ui` and the command is marked undoable in the catalogue. Its contents are the record as loaded at step four, before the mutation ran, together with the command's name for the menu label and the revision the command produced. Undoing writes that record back through steps seven to nine as a command of its own, carrying the produced revision as its `revision`, so that an undo is validated like any other write and is refused as `stale` if anything has written since; it then clears the slot. There is no redo.

Restoring a pre-image removes whatever activity-log entry the operation wrote, because the pre-image predates it. That is a property of snapshotting rather than a rule to implement, and it is the reason to snapshot rather than to compute an inverse: an inverse that is subtly wrong is worse than no undo, and nothing verifies an inverse the way the pre-image verifies itself.

A command whose `origin` is `automation` never fills the slot, and it clears whatever the slot holds. Switching or deleting the open domain clears the slot, as does quitting.

Two commands are marked not undoable because their effect is outside the record: deleting a note, whose file is gone and whose text the chrome's dialog already warns is unrecoverable, and deleting a domain, which moves a directory to the system Trash and is recovered from there.

## 9. Scopes

The automation server is configured at one of three tiers, `read-only`, `read-write`, and `destructive`, each including the ones before it. Every tool is declared at the tier it needs, and a tool above the configured tier is **not registered** rather than registered and refused.

Not registering is the better failure: an agent never sees a tool it cannot use, so it plans around the surface it actually has instead of discovering a prohibition by trying. The tier is read when a session's tool surface is built.

A command is `destructive` when it removes nodes or files: deleting a node or an extent, deleting a note, deleting a domain. Everything else that mutates is `read-write`. Reads do not pass through the pipeline, since a read cannot break an invariant; they take the lock, read the record, and answer from it, returning the revision with the answer.

## 10. Notification

Observers within the process are told after a successful write. The canvas re-renders, coalesced to at most one render per displayed frame, holding the camera, the zoom, and the fold state; the note editor reconciles if the node it is editing was removed or its file rewritten.

A change made through the window is rendered by the window's own code path, so the notification fires only for writes whose origin is `automation`. Firing for both would render the window's own echo twice.

## 11. A refusal is part of the interface

A refusal message is read by a person in a dialog and by an agent as the answer to its tool call, and in both cases it is the only thing that says why. So a mutation's refusal names the rule that failed and, where there is one, the action that would have been legal instead: not "invalid return point" but that the branch would return past the close of the scope it was opened in, and that a branch cannot reach out of its scope.

This matters more for the automation surface than for the window. An agent that is told a rule will plan around it; an agent that is told "invalid" will retry the same call. Refusal text is therefore specified with each command in the catalogue rather than left to the implementation.

---

## Appendix: one command traced

Against the worked instance in section 8 of the structural model. The command moves the task `n_t4` ("Announce") onto the middle edge of gap `g_3`, which lies inside the "Build" project.

**Before.** `w_main` has nodes `[n_s1, n_t1, n_b1, n_t2, n_t3, n_e1, n_t4, n_f1]` and gaps `[g_0 … g_6]`. Gap `g_3` holds `branchLeft [w_qa]`, `g_4` holds `returnLeft [w_qa]`, and `g_6` holds `branchRight [w_docs]`. The revision is 7.

**Steps 1 to 5.** The name is in the catalogue; the domain resolves; the file loads, parses, and needs no migration; the command carries revision 7, which matches.

**Step 6, the mutation.** Removing `n_t4` from node index 6 merges the gap below it, `g_5`, with the gap above it, `g_6`. The merged gap keeps `g_5`'s id and its branch point, and takes `g_6`'s departures beyond its own, so `w_docs` now departs at `g_5`; `g_6`'s record is discarded. Inserting `n_t4` on the middle edge of `g_3` splits that gap: the record follows its branch point, so `g_3` keeps its id and its `branchLeft [w_qa]` below the new node, and a fresh gap `g_11` takes the return point above it.

**After.** `w_main` has nodes `[n_s1, n_t1, n_b1, n_t2, n_t4, n_t3, n_e1, n_f1]` and gaps `[g_0, g_1, g_2, g_3, g_11, g_4, g_5]`. One entry is appended to `n_t4`'s activity log and to no other node's.

**Step 7, validation.** Eight nodes and seven gaps satisfies I3. The project `n_b1`/`n_e1` now spans node indices 2 to 6, so it contains gaps 2 through 5, which are `g_2`, `g_3`, `g_11`, and `g_4`. Branch `w_qa` departs at `g_3` (gap index 3) and returns at `g_4` (gap index 5): the return is above the departure, satisfying I11; both lie inside exactly the project "Build", satisfying I12; and both are left-side, satisfying I10. `w_docs` departs at `g_5`, which is in no project, and appears in no return list, so it is open, which I8 permits. `n_t4` has moved into the "Build" scope, which is the visible effect of the command.

**Steps 8 to 10.** No note files. The record is written atomically at revision 8. The undo slot takes the pre-image, since the origin is `ui` and the command is undoable. Observers are not notified, the origin being the window itself.

**A refusal on the same fixture.** Moving `w_qa`'s return to `g_5` passes the mutation's own precondition if that precondition only checks the workflow, and is then caught at step seven by I12, since `g_5` lies outside the project whilst the departure lies inside. Better is for the mutation to refuse it at step six with the rule named, leaving I12 as the net that catches the case the mutation forgot.
