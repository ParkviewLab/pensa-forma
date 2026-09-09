<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# The automation server

The authority for the application's programmatic interface: a local server speaking the Model Context Protocol (MCP), through which external tools and AI agents read and write the open library while the application runs. It wraps the [command catalogue](command-catalogue.md) and nothing else; every tool is a call into the [command layer](command-layer.md), so an agent edits the live application exactly as a person does, through the one write path that validates before it persists.

---

## 1. Goal

An agent should be able to read a domain's workflows and act on them the way a person does: see the tasks set up next, add or complete tasks, set a cursor, restructure, and leave a record in the activity log. The motivating case is "look in there and see the tasks I set up for you to do next," made easy for an agent. Read and write from the start, not read-only: every write passes the same validation gate, so a write is no more dangerous to data integrity than a read, and the residual risk is semantic, which is the agent's responsibility with any tool.

## 2. Architecture

The application is the server. While it is open, it hosts an MCP endpoint on the loopback interface, and an agent talks to the live application; every edit is the application's own edit.

The server is a small module in the application process. It runs on its own runtime thread, separate from the interface's frame loop, and every request it handles ends in a call into the command layer, which serialises it under the same lock the window's own commands take. Reads take the lock too, so a read never observes a half-written record. Because the authority is in-process, a successful automation write notifies the window, which re-renders the open domain (section 8).

The transport is Streamable HTTP, served by a loopback HTTP listener at a single `/mcp` path. The server is **stateless**: each request carries a complete JSON-RPC message, the endpoint accepts `POST` only, and it answers `405 Method Not Allowed` to `GET` and `DELETE`, since a stateless server has no server-initiated stream to open and no session to terminate. A `GET /health` beside it answers `{ ok, name, version, revisionOf }` for a liveness check, where `revisionOf` maps each open domain's id to its revision.

## 3. Binding and lifecycle

- Bind to `127.0.0.1` only, never to every interface. The endpoint is reachable by local clients and by nothing on the network.
- Fixed default port `35899`, settable in `settings.json` (D29). It sits below the ephemeral port ranges of macOS and Windows; on Linux it falls inside the default ephemeral range, where a transient outbound socket could hold it at the moment the application starts, a low-probability case the fail-visible behaviour covers.
- The port does not roam. A user registers the URL once with their client, so it must be stable across restarts; trying a port and falling back to the next free one would silently invalidate the registration. If the configured port is in use, the server does not start and says so in the chrome's automation pill, leaving the user to choose another port and register it once.
- A single-instance lock, so only one process runs and therefore only one binds the port; a second launch focuses the existing window and exits.
- Starts when the application is ready, if enabled; stops on quit; reachable at `http://127.0.0.1:35899/mcp` while running.
- Enabled by default, with the pill in the header showing the URL, copying it, and switching the server off and on.

## 4. Security posture

No authentication on the loopback endpoint in the first version, because every client of interest accepts a bare localhost endpoint and a required token is friction at exactly the moment it should just work. The guardrails instead are:

- loopback-only binding, so only local processes can reach it;
- the single-instance lock;
- DNS-rebinding protection on the transport: the `Host` header must be `127.0.0.1:<port>` or `localhost:<port>`, and an `Origin` header, when present, must be `http://127.0.0.1:<port>` or `http://localhost:<port>`, or the request is answered `403`. This closes the one avenue by which a malicious web page open in a browser could post to the port;
- the scope tiers (section 5);
- the validation gate every write already passes.

A per-install bearer token, generated once, kept in settings, shown in the pill, and passed by the client as a header, is an easy later addition for defence in depth and composes with all of the above.

## 5. Scope tiers

The server is configured at one of three tiers, `read-only`, `read-write`, and `destructive`, each including the ones before it, from `server.scope` in the settings or the `PENSAFORMA_SERVER_SCOPE` environment variable. Every tool is declared at the tier it needs, and a tool above the configured tier is **not registered**: an agent never sees a tool it cannot use, so it plans around the surface it actually has. The tier is read when a session's tool surface is built, so changing it takes effect for new sessions.

`destructive` holds the three commands that remove nodes or files: `delete_node`, `delete_note`, `delete_domain`. Everything else that writes is `read-write`. Prompts that name write tools are registered at `read-write` and above, not at `read-only`, so a read-only session is never handed a recipe it cannot follow.

## 6. What the client is told at connect

The server's initialise response carries these instructions, which every client shows its model:

> PensaForma is a LIVE store: its user, and other agents, can change it at any moment. Never rely on an earlier read. Treat anything you read (domains, workflows, flagged nodes, statuses, notes) as possibly stale the instant after you read it. Before you act, and always immediately before a write, re-read the current state with the relevant tool (find_flagged, read_domain, read_workflow, read_project, read_node, read_note) and resolve any description such as "the flagged one" or "the current task" against that fresh read, not against memory. Every read returns the domain's revision; pass it as `revision` on your write, and a write against a changed domain is refused as stale rather than landing on the wrong state. Every write returns the affected id, the new revision, and the re-rendered outline; treat that as your new ground truth.
>
> The model: a domain holds workflows. A workflow opens at a start node and closes at a finish node; between them sit tasks, projects (a begin node paired with an end node, and everything between), and gaps. Between every pair of consecutive nodes is one gap, which owns a branch point (lower) where branches depart and a return point (upper) where branches arrive; a node can be inserted on a gap's outgoing, middle, or incoming edge, which differ in whether it lands below, between, or above the gap's departures and arrivals. A branch is a workflow of its own; it departs from a branch point on one side, left or right, at an order position among its siblings, and it may return to a return point at or above its departure, on the same side, inside exactly the same projects, or it may run open. A finish node and an end node carry no title; a workflow is named by its start node and a project by its begin node. Only a task has a status or the "here" cursor. Growth is upward.
>
> The tools speak that vocabulary and no other. Every id-valued parameter takes an id; titles are not addresses, since a title can change between your read and your write. Positions are given as a gap id with an edge (outgoing, middle, incoming), a gap id with a side and index at its branch point, or an index among the domain's main workflows.

## 7. The tool surface

Every tool takes an optional `domain` (an id, a name, or a path; default the last-opened domain) and every write takes an optional `revision`. A write returns `{ id, revision, outline }`: the id of the subject or new object, the new revision, and the outline of the affected workflow. A refusal returns the command layer's code and message as the tool error, so the agent reads the rule and the legal alternative.

Parameter names follow one rule: a parameter that takes a node of any kind is `node_id`; one that takes a particular kind names it (`task_id`, `begin_id`, `start_id`, `workflow_id`); a gap is `gap_id`; a position is `target`, in the catalogue's grammar; a second node in a relation keeps its role name (`from_id`, `to_id`). A tool is named for the command it wraps, and a tool that takes one kind says so in its description and refuses the rest naming the tool that accepts them.

A note, a flag, and a log belong to openers and tasks only (D11 as amended); `read_note`, `read_log`, `set_note`, `delete_note`, `set_flag`, and the three log tools refuse a finish or end node with the catalogue's message.

### Read-only

| Tool | Wraps |
| --- | --- |
| `list_domains()` | `list_domains` |
| `read_domain(domain?, include_notes?)` | `read_domain` |
| `read_workflow(workflow_id, include_notes?)` | `read_workflow` |
| `read_project(begin_id, include_notes?)` | `read_project` |
| `read_node(node_id, include_note?)` | `read_node` |
| `read_note(node_id)` | `read_note` |
| `read_log(node_id)` | `read_log` |
| `find_flagged(domain?)` | `find_flagged` |
| `copy_project(begin_id)` | `copy_project`, returning a clip for `paste` |

### Read-write

| Tool | Wraps |
| --- | --- |
| `create_domain(name)` | `create_domain` |
| `rename_domain(domain, name)` | `rename_domain` |
| `create_workflow(title, target?)` | `create_workflow` |
| `move_workflow(start_id, target)` | `move_workflow` |
| `set_title(node_id, title)` | `set_title` |
| `insert_task(gap_id, position, title)` | `insert_task` |
| `add_task(node_id, above_or_below, title)` | `insert_task` at the derived gap and position |
| `move_task(task_id, target)` | `move_task` |
| `set_status(task_id, status)`, `cycle_status(task_id)` | the two status commands |
| `set_here(task_id)`, `clear_here(task_id)` | the two cursor commands |
| `set_flag(node_id, flagged)` | `set_flag` |
| `wrap_run(from_id, to_id, title)` | `wrap_run` |
| `unwrap_project(begin_id)` | `unwrap_project` |
| `convert_task_to_project(task_id)`, `convert_project_to_task(begin_id)` | the two conversions |
| `move_project(begin_id, target)` | `move_project` |
| `open_branch(gap_id, side, title)` | `open_branch` |
| `add_branch(node_id, above_or_below, side, title)` | `open_branch` at the derived gap |
| `attach_return(start_id, gap_id)` | `attach_return` |
| `detach_return(start_id)` | `detach_return` |
| `set_note(node_id, text)` | `set_note` |
| `add_log_entry(node_id, text)`, `edit_log_entry(node_id, entry_id, text)`, `delete_log_entry(node_id, entry_id)` | the three log commands |
| `paste(clip, target)` | `paste` |

An agent's log entries carry `author: { kind: agent, name }`, where `name` is the client's declared name from the MCP initialise handshake, or `"agent"` when it declares none.

### Destructive

| Tool | Wraps |
| --- | --- |
| `delete_node(node_id)` | `delete_node` |
| `delete_note(node_id)` | `delete_note` |
| `delete_domain(domain)` | `delete_domain`; the argument is required |

### Deliberately absent

The library root and the settings: user settings whose change needs a native dialog or a restart; an agent works within the existing library. Bookmarks and fold state: view state, not data. A tool that reorders a side list by index alone: side and order are set through `move_workflow`, one gesture and one tool for one fact.

## 8. Prompts

A prompt is fetched by the client for the user's own menu and costs nothing unless invoked, and it is the one place the surface can state an **order** of operations rather than a rule. Two are offered, sparingly.

**`work_flagged`.** For the common "work the flagged nodes" flow: call `find_flagged` first; for each flagged node call `read_node` (and `read_project` for the enclosing project's context when one is reported); plan; then, immediately before each write, re-read the node and pass the revision. Every tool the prompt names is a tool on the surface at the session's tier, and a test holds it there.

**`decompose_project`.** For breaking a project into tasks, sub-projects, and branches, in the order that keeps every step legal: insert the tasks along the line first, then wrap runs of them as sub-projects, then open branches off the gaps and attach their returns last. The order matters because `wrap_run` refuses a run that a branch departs inside and returns outside, so opening branches before wrapping can make the intended wrap illegal, and an agent that branches first discovers that as a refusal after the work is done.

Prompts are registered at the tier of the tools they name.

## 9. Resources

None in the first version. In the protocol a resource is application- or user-controlled and is fetched and pinned into a conversation as an attachment, which is precisely the stale-read hazard this surface is built against: nothing in a transcript distinguishes an attachment fetched a minute ago from one fetched an hour ago. A resource is also addressed by a URI template with no schema and no enum, and a failure is a protocol error rather than the prose refusal that names the sibling tool. If resources ever earn a place it is for notes, which are genuinely documents with filenames and where a stale copy costs little; that is recorded as an in-flight idea.

## 10. Live view

When the server changes a domain, the window updates the displayed domain live, so the user can watch the agent work. After every successful automation write the command layer notifies the window; if the open domain is the one changed, it re-reads the record and re-renders (measure, layout, draw), coalesced to at most one render per displayed frame. Every notification follows a validated write, so the live view is never half-formed.

Rules:

- The user always controls the camera. A live update never moves the camera and never changes pan or zoom; new nodes appear in place. Fold state is preserved likewise; both are client view state (northstar, axiom 9).
- No changed-node highlight; the update is silent.
- A burst of agent edits coalesces into one render per frame.
- The window applies the results of its own commands directly and treats a notification only as "another writer changed this domain", so nothing renders twice.
- An automation write clears the undo slot (command layer, section 8).
- If a task's note is open in the editor while the server writes that note, the editor reloads it when it has no unsaved edits and warns rather than overwrites when it does; if the server deletes the node whose note is open, the editor closes with a notice. A user's in-progress note is never silently discarded. The exact dialogs are in the [UI chrome](ui-chrome.md).

## 11. Clients

Any MCP client that connects to a Streamable HTTP endpoint on localhost without authentication can use the server. Registration is a one-time step in the client; for Claude Code it is

```bash
claude mcp add --transport http pensa-forma http://127.0.0.1:35899/mcp
```

A client that reconnects with backoff when the endpoint is down will attach whenever the application comes up; one that does not must be started with the application already running, or reconnected by hand.

## 12. Deferred

A stdio transport, which a client spawns per session; HTTP is chosen because the user controls when the application is up, and a spawned process cannot attach to an already-running one. The per-install token. A discovery file in the data directory holding the current endpoint, so tooling can find the URL without the user copying it. A server mode in which one authoritative store on a LAN host serves several windows, which would fall out of the single command interface but assumes a reachable host and a live-update channel.
