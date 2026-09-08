<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Contributing

This repo follows the ParkviewLab conventions. The essentials are below; the
authoritative, org-wide version of all of this is the
[ParkviewLab handbook](https://github.com/ParkviewLab/handbook).

## Branch & PR flow

- Branch off **`develop`** into an ephemeral worktree named with a prefix:
  `feature-`, `bug-`/`fix-`, `doc-`, `test-`, `ops-`, `ci-`, `build-`, `release-`
  (hyphen, not slash). See the handbook's `branching.md`.
- Open a PR into **`develop`**. The repo is **squash-only**, so the merge button
  can only squash; **merging is the maintainer's action.**
- Releases are cut from **`main`** via the CLI (`git merge --no-ff develop`, then
  bump + tag), not a PR. See the handbook's `releases.md`.

## The documents lead

The northstar is the authority for intent and the specification for structure
and behaviour (`docs/specification/decisions.md`, D1). A pull request that
changes what the application is for, or how an axiom is honoured, amends
`docs/northstar.md` in the same PR; one that changes structure or behaviour
the specification states amends the specification in the same PR, the
Markdown first and its HTML twin with it. An unintended disagreement between
the code and either document is a defect in the code, not in the document.

## Commit / PR-title convention (this is what the changelog reads)

Because PRs are squash-merged, **the PR title becomes the commit subject**, and
the changelog is generated from it (via [git-cliff](https://git-cliff.org/) +
`cliff.toml`). Prefix every PR title with a [Conventional
Commit](https://www.conventionalcommits.org/) type:

| Prefix | CHANGELOG section | Notes |
|---|---|---|
| `feat:` | Features | user-visible |
| `fix:` | Bug fixes | user-visible |
| `perf:` | Performance | user-visible |
| `refactor:` | Refactor | |
| `docs:` | Docs | |
| `test:` | Tests | |
| `chore:` / `ci:` / `build:` / `style:` | _(dropped)_ | stays in git history, not surfaced |

A PR title without a recognised prefix is **silently dropped** from the
changelog. So: prefix it.

## Local checks before opening a PR

Run the same checks CI requires, so the PR is green on arrival. Until the Cargo
workspace exists, only the REUSE lint applies.

```bash
cargo fmt --all -- --check
cargo clippy --all-targets -- -D warnings
cargo test
uvx --from "reuse[charset-normalizer]" reuse lint
```

A PR **can't be merged until the required checks pass** (format, clippy, tests,
REUSE, the version guard; see the handbook's `ci.md`). Push after each commit.

## Versioning

The version lives in **`Cargo.toml` only**, as the workspace's package version;
never hard-code it elsewhere, and never type it on a `git tag` line. Use
`git bump` / `git release` from
[`dev-tools`](https://github.com/ParkviewLab/dev-tools); see the handbook's
`releases.md`. (The helpers do not yet read a `Cargo.toml`; see
[`in-flight_ideas.md`](in-flight_ideas.md).)

## AI contributors

Read `docs/northstar.md` first, and follow the behavioural contract in the
handbook's `ai-collaboration.md` (notably: merging, tagging, and releasing each
need an explicit, per-action go-ahead).
