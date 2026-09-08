<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Persistence

The authority for everything on disk: where the application keeps its data,
how a library and a domain are laid out, the canonical form of the domain
record, the note and bookmark files, the settings and view-state files, the
atomic-write protocol, schema versioning, and the path-safety rules. The
structure of the record is the [structural model](structural-model.md)'s;
this document says how that structure is written down. The write path that
produces it is the [command layer](command-layer.md)'s.

The files are the user's (northstar, axiom 8). Everything here is designed so
that a domain can be read, moved, copied, diffed, and edited with ordinary
tools, and so that the application's own writes are safe against interruption.

---

## 1. Locations

The application keeps its own state in the platform's per-user application
data directory for the identifier `ai.parkviewlab.pensa-forma`, resolved as
the `directories` convention resolves a project with qualifier `ai`,
organisation `parkviewlab`, and application `pensa-forma`:

| Platform | Data directory |
| --- | --- |
| macOS | `~/Library/Application Support/ai.parkviewlab.pensa-forma/` |
| Linux | `$XDG_DATA_HOME/pensa-forma/` (default `~/.local/share/pensa-forma/`) |
| Windows | `%APPDATA%\parkviewlab\pensa-forma\data\` |

Inside it:

| Entry | Holds |
| --- | --- |
| `settings.json` | the durable settings (section 6) |
| `viewstate.json` | disposable per-domain view state (section 7) |
| `domains/` | the default library root (section 2) |

The identifier is the application's own, so this directory never coincides
with any other application's, and the library it creates is its own (D24).

## 2. The library and the domain directory

The **library** is one directory holding one subdirectory per domain. Its
root is the `libraryRoot` setting, defaulting to `domains/` in the data
directory; the user may point it anywhere, for instance into a directory that
another tool synchronises.

A **domain directory** is named for what it is, what it holds, and which
domain it is:

```
pensaforma_domain_<slug>_<id>        e.g.  pensaforma_domain_homelab_d_mrtwgppt01
pensaforma_domain_<id>               when the name yields no slug
```

The prefix says which application owns the directory, the slug keeps a
listing readable, and the id makes it findable. The **id is the identity and
the label is decoration**: the record inside is the only authority for the
domain's id and name, and the directory name is derived from it, never the
other way round. Listing the library reads each candidate directory's record
for its id and name; a directory whose name does not carry the prefix and a
well-formed id is not the application's and is ignored, so a library root may
hold unrelated folders safely. A directory whose label has drifted from its
record (a rename by hand, a copy) is re-labelled from the record at the next
listing, and `rename_domain` re-derives it at once.

The slug: the name lowercased, every run of characters outside `a-z0-9`
collapsed to a single hyphen, leading and trailing hyphens stripped, the
result cut to twenty-four characters, and a trailing hyphen left by the cut
stripped again. A name of only punctuation or symbols slugs to the empty
string, and the segment and its underscore are then omitted.

Inside a domain directory:

| Entry | What it is |
| --- | --- |
| `domain.json` | the record (section 3) |
| `domain.schema.json` | the JSON Schema of the record, with a description of every field (section 3.1) |
| `README.md` | a page of prose describing the directory and the record's fields (section 3.1) |
| `bookmarks.json` | the saved views (section 5); absent until the first bookmark |
| `notes/` | one markdown file per node note (section 4) |

A domain name is one to sixty-four characters, trimmed, with no control
characters; separators are allowed ("AI/ML" is a reasonable name) because no
path is ever derived from the name directly. Names are unique within the
library.

Deleting a domain moves the whole directory to the system's Trash, record,
bookmarks, and notes together, from which it can be restored whole.

## 3. The domain record

`domain.json` is the record of the structural model, section 2, in JSON.

**Tolerant read.** The reader accepts JSON5: comments, unquoted keys,
trailing commas, single-quoted strings. A file edited by hand still opens.

**Canonical write.** Every write from the application is strict JSON, keys
in the order the tables below give, two-space indentation, a trailing
newline, and the omissions that follow, so that two writes of the same record
are byte-identical and a diff shows only what changed.

- An absent optional field is omitted, never written as `null`; a `false`
  boolean is omitted; an empty list on a gap is omitted.
- A gap whose four lists are all empty is written as `{}`. Nearly every gap
  is such a gap, so the `gaps` map is mostly empty objects; each gap's
  identity and position still come from its workflow's `gaps` list.
- `nodes`, `gaps`, and `workflows` are maps keyed by id, with the id repeated
  as the object's own `id` field for legibility. Map keys are written in
  ascending id order, which is creation order.
- Timestamps are RFC 3339 in UTC with millisecond precision.

The top level:

```
$schema     string       "domain.schema.json", the schema file beside the record
schema      integer      1
revision    integer
id          d_…
name        string
mains       [w_…]
workflows   { w_…: Workflow }
nodes       { n_…: Node }
gaps        { g_…: Gap }
```

`$schema` is written first and names the schema file by its relative name; it
is not model state, and a record that lacks it still loads. A workflow: `id`,
`nodes` (list), `gaps` (list). A node: `id`, `kind`, then
the fields its kind carries in the order `title`, `pair`, `status`, `completedAt`, `here`,
`flagged`, `note`, `log`; a log entry: `id`, `at`, `author`, `origin`,
`event`, `text`, `editedAt`, `editedBy`, with the last three omitted when
null. A gap: `id`, then whichever of `branchLeft`, `branchRight`,
`returnLeft`, `returnRight` are non-empty.

The worked instance of the structural model, section 8, in canonical form:

```json
{
  "$schema": "domain.schema.json",
  "schema": 1,
  "revision": 7,
  "id": "d_ex01",
  "name": "Example",
  "mains": ["w_main"],
  "workflows": {
    "w_docs": { "id": "w_docs", "nodes": ["n_s3", "n_t6", "n_f3"], "gaps": ["g_9", "g_10"] },
    "w_main": {
      "id": "w_main",
      "nodes": ["n_s1", "n_t1", "n_b1", "n_t2", "n_t3", "n_e1", "n_t4", "n_f1"],
      "gaps": ["g_0", "g_1", "g_2", "g_3", "g_4", "g_5", "g_6"]
    },
    "w_qa": { "id": "w_qa", "nodes": ["n_s2", "n_t5", "n_f2"], "gaps": ["g_7", "g_8"] }
  },
  "nodes": {
    "n_b1": { "id": "n_b1", "kind": "begin", "title": "Build", "pair": "n_e1", "log": [] },
    "n_e1": { "id": "n_e1", "kind": "end", "pair": "n_b1" },
    "n_f1": { "id": "n_f1", "kind": "finish" },
    "n_f2": { "id": "n_f2", "kind": "finish" },
    "n_f3": { "id": "n_f3", "kind": "finish" },
    "n_s1": { "id": "n_s1", "kind": "start", "title": "Ship v1", "log": [] },
    "n_s2": { "id": "n_s2", "kind": "start", "title": "QA pass", "log": [] },
    "n_s3": { "id": "n_s3", "kind": "start", "title": "Write docs", "log": [] },
    "n_t1": { "id": "n_t1", "kind": "task", "title": "Draft spec", "status": "completed", "completedAt": "2026-09-01T16:20:00.000Z", "log": [] },
    "n_t2": { "id": "n_t2", "kind": "task", "title": "Backend", "status": "in-progress", "here": true, "log": [] },
    "n_t3": { "id": "n_t3", "kind": "task", "title": "Frontend", "status": "todo", "log": [] },
    "n_t4": {
      "id": "n_t4", "kind": "task", "title": "Announce", "status": "todo", "flagged": true,
      "note": "n_t4_announce.md",
      "log": [
        {
          "id": "e_mrtwgppt02", "at": "2026-09-02T18:04:11.212Z",
          "author": { "kind": "system", "name": "pensa-forma" },
          "origin": "system", "event": "created", "text": "Created above \"the close of Build\"."
        }
      ]
    },
    "n_t5": { "id": "n_t5", "kind": "task", "title": "Write tests", "status": "in-progress", "here": true, "log": [] },
    "n_t6": { "id": "n_t6", "kind": "task", "title": "API reference", "status": "todo", "log": [] }
  },
  "gaps": {
    "g_0": {}, "g_1": {}, "g_2": {},
    "g_3": { "id": "g_3", "branchLeft": ["w_qa"] },
    "g_4": { "id": "g_4", "returnLeft": ["w_qa"] },
    "g_5": {},
    "g_6": { "id": "g_6", "branchRight": ["w_docs"] },
    "g_7": {}, "g_8": {}, "g_9": {}, "g_10": {}
  }
}
```

(The fixture's ids are shortened for reading; real ids are the twelve
characters of the structural model, section 1.)

**Schema version and migration.** `schema` is `1` for this specification.
On load, a record whose `schema` is lower than the application's is brought
up by the migration for each step, and the upgraded record is written back
exactly once, only when the migration changed something. A record whose
`schema` is higher than the application understands is refused with a message
that names both versions; the application never guesses at a format it does
not know.

### 3.1 The directory describes itself

A domain is plain JSON and markdown so that it can be read without the
application, and a reader with only the directory must not have to divine
what the record's fields mean. The description therefore travels with the
data, as two files the application writes beside the record (D36).

`domain.schema.json` is a JSON Schema for `domain.json`, with a `description`
on every property, taken from the structural model's tables. The record's
first field, `$schema`, names it by relative name, so an editor that
understands JSON Schema explains each field on hover and flags a hand edit
that breaks the shape, and any JSON Schema validator can check a file with
no application present.

`README.md` is the same description for a person: a page of prose saying
what the three kinds of file in the directory are, how the record is laid
out, with a table of its fields, how a note file's name carries its node's
id, and what the bookmarks file holds.

Both are the application's. They are generated from one source, the
schema's descriptions, which are authored once in the repository beside the
`store` crate and checked against the structural model by test; the README
is rendered from the schema. The application writes both when it creates a
domain and rewrites both whenever the record's `schema` version changes,
and never reads either for data: the record is the only authority, and a
hand edit to these two files is overwritten at the next such write. Neither
is part of section 8's atomic write of the record; each is written whole on
its own.

Comments in the record itself were considered and rejected. The application
rewrites the whole record on every save, and a writer that reconstructs the
text from the data model strips whatever the text carried that the model
does not, so a comment would survive exactly until the next save. The
tolerant read (section 3) still accepts a file with comments or trailing
commas; it does not preserve them.

## 4. Note files

A note lives at `notes/<nodeId>_<slug>.md`, or `notes/<nodeId>.md` when the
title yields no slug. The slug is built from the node's title at the moment
the note is first written: lowercased, runs of non-alphanumerics collapsed to
single hyphens, leading and trailing hyphens stripped, cut to twelve
characters, and a trailing hyphen left by the cut stripped again. The order
matters: a title beginning with punctuation sheds its leading hyphen before
the cut, so the twelve characters are content. The slug is decorative and is
not kept in step with a later retitle; the id is what resolves, and the node's
`note` field holds the whole filename.

The file is created on the first non-empty save, file first and record
second (command layer, section 7). Emptying a note writes an empty file and
keeps the reference. Deleting a node leaves its file as an orphan; only
`delete_note` while the node exists, or deleting the domain, removes one. A
note not yet written reads as empty.

A note filename is validated on every use: a bare name with no path
separators, no control characters, at most 128 characters, ending in `.md`,
and not a reserved dot name. The `notes/` segment is added by the store and
cannot be supplied by a caller.

## 5. Bookmarks

`bookmarks.json` holds the domain's saved views: named view state, the one
kind of view state that may travel with the data (northstar, axiom 9),
because a name makes it shareable.

```json
{
  "bookmarks": [
    { "name": "Build, this week", "folded": ["n_b1"], "nodes": ["n_b1", "n_t2", "n_t3", "n_e1", "n_s2", "n_t5", "n_f2"] }
  ]
}
```

A bookmark is a name, the opener ids (begin or start) folded when it was saved, and the ids of
every node drawn wholly inside the viewport when it was saved (D32). It holds
no zoom and no camera coordinate, because a field that travels must mean the
same thing on every client, and a pixel-anchored camera is one screen's
framing. Restoring a bookmark applies the fold set, drops ids that no longer
exist, and frames the surviving nodes under a maximum scale and a minimum
padding; only an empty survivor set is a broken bookmark. Names are unique
within the domain.

The file is absent until the first bookmark is added and is written
atomically like every other file.

## 6. Settings

`settings.json` in the data directory holds the durable settings. It is
small, and it holds the pointer to the user's data, so it is treated with
care: a present-but-unreadable file (corrupt JSON, a permissions error, a
synchronisation conflict) is never overwritten. Reads fall back to defaults
without writing anything, so the bad file is preserved for recovery, and
writes are refused with a message until it is repaired.

```json
{
  "libraryRoot": "/Users/gary/Library/Application Support/ai.parkviewlab.pensa-forma/domains",
  "lastDomain": "d_mrtwgppt01",
  "server": { "enabled": true, "port": 35899, "scope": "read-write" },
  "theme": "azure",
  "note": { "split": 0.5, "wrap": true, "fontSize": 16 }
}
```

| Field | Default | Meaning |
| --- | --- | --- |
| `libraryRoot` | the data directory's `domains/` | where the domain directories live |
| `lastDomain` | none | the domain to reopen at launch, by id |
| `server.enabled` | `true` | whether the automation server starts with the application |
| `server.port` | `35899` | its loopback port; never roams |
| `server.scope` | `read-write` | `read-only`, `read-write`, or `destructive` |
| `theme` | `azure` | `azure` or `navy` |
| `note.split` | `0.5` | the note editor's divider fraction |
| `note.wrap` | `true` | soft wrapping in the note source pane |
| `note.fontSize` | `16` | the preview's base text size, 12 to 28 |

The environment variable `PENSAFORMA_SERVER_SCOPE`, when set to one of the three
tiers, overrides `server.scope` for that launch, so an operator can widen or
narrow the surface without editing the file.

## 7. View state

`viewstate.json` in the data directory holds the client's live view state per
domain, keyed by domain id:

```json
{ "d_mrtwgppt01": { "folded": ["n_b1", "n_b7"] } }
```

It is disposable: a corrupt or missing file reads as empty and is overwritten
by the next write. It is kept out of the domain directory because it is this
client's state, not the domain's (northstar, axiom 9).

The theme, the flagged-only toggle, the copy clipboard, and the zoom and pan
are not persisted here: the theme is a setting, and the rest are session
state.

## 8. The atomic write

Every file the application writes, records, notes, bookmarks, settings, and
view state, is written the same way:

1. Write the whole content to a temporary file in the destination directory,
   named for the target with a suffix that marks it as temporary.
2. Flush the temporary file to disk.
3. Rename it over the target. On a platform whose rename does not replace an
   existing file, use its atomic replace primitive; never unlink first, since
   unlink-then-rename has a window in which the file does not exist.
4. Flush the directory, so the rename itself survives a crash or power loss;
   where the platform does not support flushing a directory, this step is
   skipped.

A reader therefore sees either the whole old file or the whole new one, never
a partial write, and an interrupted save never truncates a good file. A
temporary file left behind by a crash is ignored by every reader (it does not
match any expected name) and replaced by the next write.

## 9. Path safety

Every path the store touches is derived by the store and bounds-checked
before use; no caller, the window or the automation server, ever supplies a
path the store trusts.

- A domain directory must be an immediate child of the current library root.
  A path that resolves elsewhere is refused.
- A note filename must pass section 4's validation, and the resolved path
  must lie within the domain's `notes/` directory.
- Resolution is against the canonical absolute root, and the test is that the
  resolved path equals the root or begins with the root followed by a
  separator, so a sibling directory whose name merely begins with the root's
  name cannot pass.

The one deliberate write outside the library is markdown export, which
writes wherever the user chose in the platform's save dialog; its trust
boundary is that dialog, and the write is still atomic.

## 10. One writer, and edits from outside

Within a running application there is exactly one writer, the command layer,
under one lock; the window and the automation server both go through it. A
second instance of the application is prevented from running by the
single-instance lock, so no two processes write the same library through the
application.

The files remain the user's, and a user may edit a record or a note in a text
editor while the application runs. The application does not watch the
filesystem in its first version; the next command reads the file afresh and
sees the edit, and the tolerant reader accepts what a person is likely to
have typed. A change made by hand while a command is in flight is overwritten
by that command's write, which is the ordinary consequence of two writers
and one file; the record's `revision` protects the application's own callers
from each other, not from an editor. Reflecting external edits live, by
watching the directory, is recorded as an in-flight idea.
