<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Licensing

Copyright © 2026 **Gary Frattarola**.

## How this project is licensed

This project is **dual-licensed**:

### The open-source option (default)

The code is free software under the GNU Affero General Public License, version 3 or (at your option) any later version (AGPL-3.0-or-later). You may use, study, modify, and redistribute it under those terms. The full text is in [`LICENSE`](LICENSE) and [`LICENSES/`](LICENSES/).

Note the AGPL's network clause (section 13): if you run a modified version and let users interact with it over a network, you must offer them the corresponding source.

### The commercial option

If you cannot or prefer not to comply with the AGPL, for example to embed this work in a closed-source product or to avoid the source-disclosure obligation, a separate commercial license is available from the copyright holder. Inquiries: **garyf@parkviewlab.ai**.

## Per-bucket licensing

Different kinds of content carry different licenses, encoded in [`REUSE.toml`](REUSE.toml) and in per-file SPDX headers:

| Bucket | License |
|---|---|
| Code, build configuration, workflows, lockfile (`src/**`, `crates/**`, `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `.github/**`, `scripts/**`, `cliff.toml`) | `AGPL-3.0-or-later` |
| Documentation (`docs/**`, `README.md`, `CHANGELOG.md`, this file) and repository metadata | `CC-BY-4.0` |
| Bundled third-party fonts, when vendored | their upstream license, never relabelled (the SIL Open Font License 1.1 for the faces the interface uses) |
| ParkviewLab brand marks, if vendored | `LicenseRef-AllRightsReserved` |

## REUSE compliance

This repo is [REUSE](https://reuse.software/)-compliant. Every file has a license via an SPDX header or a `REUSE.toml` annotation. Verify with:

```bash
uvx --from "reuse[charset-normalizer]" reuse lint
```

Any new file needs an SPDX header or a `REUSE.toml` entry, or the lint breaks.
