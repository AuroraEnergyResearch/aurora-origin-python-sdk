# Dependabot Triage — 2026-06-15

## Summary table

| Severity | Total | 🔴 True positive | 🟡 False positive | Pending merge |
|---|---|---|---|---|
| Critical | 1 | 0 | 1 | — |
| High | 47 | 3 | 44 | 3 (PR #63) |
| Medium | 49 | 0 | 49 | — |
| Low | 13 | 1 | 12 | 1 (PR #63) |
| **Total** | **110** | **4** | **106** | **4** |

All true positives are fixed by lockfile-only bumps on branch `dependabot-high-alerts`, [PR #63](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/pull/63).

---

## Critical

### 🟡 False positive

#### #143 — `shell-quote` · CVE-2026-9277 · [Alert](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/security/dependabot/143)

- **Manifest:** `docsite/package-lock.json`
- **Chain:** `@docusaurus/core` → `webpack-dev-server` → `launch-editor` → `shell-quote` 1.8.0; also `@docusaurus/core` → `react-dev-utils` → `shell-quote`
- **Reasoning:** `shell-quote`'s vulnerable `quote()` is called only by `launch-editor` (open file in editor during dev server) and `react-dev-utils` CLI tooling. Both run only on a developer's local machine during `docusaurus start`. The vulnerable code path runs only on the local dev server/build machine, is never bundled into the static docs output, and receives no untrusted input.
- **Action:** Dismissed `not_used`.

---

## High

### 🔴 True positives → fixed in PR #63

#### #66, #67, #68 — `urllib3` · CVE-2025-66418, CVE-2025-66471, CVE-2026-21441 · [#66](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/security/dependabot/66) [#67](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/security/dependabot/67) [#68](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/security/dependabot/68)

- **Manifest:** `uv.lock`
- **Chain:** `aurora_origin_sdk` → `requests` (core runtime dep) → `urllib3` 2.5.0
- **Reasoning:** `urllib3` is genuinely in the production code path — every HTTP response is decompressed by it. Three CVEs cover decompression-bomb scenarios (unbounded chain, streaming API, redirect path). The streaming-specific CVEs (#67, #68) are technically unreachable since the SDK never uses `stream=True`, and all traffic is to trusted Aurora infrastructure. However the fix is a zero-risk lockfile bump so these are treated as true positives.
- **Fix:** `uv lock --upgrade-package urllib3` → 2.7.0 on Python ≥3.10, 2.6.3 on Python 3.9. Both satisfy the patch floors for all three CVEs. Lockfile-only change.

### 🟡 False positives (pip)

#### #130 — `urllib3` · CVE-2026-44431 · [Alert](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/security/dependabot/130)

- **Chain:** as above
- **Reasoning:** CVE-2026-44431 (sensitive headers forwarded in proxied low-level redirects) is in urllib3's own `urlopen(redirect=True)` path under a proxy. `requests` always calls urllib3 with `redirect=False` and resolves redirects itself (stripping auth headers cross-host), so the vulnerable path is never exercised. Additionally, urllib3 2.7.0 (the patched version) dropped Python 3.9 support, so no fix is available for the SDK's Python 3.9 floor — accepted risk.
- **Action:** Dismissed `not_used`.

#### #87, #101 — `tornado` · CVE-2026-31958, CVE-2026-35536

- **Chain:** `aurora_origin_sdk[notebooks]` → `ipykernel` / `jupyter-client` → `tornado` 6.5.1
- **Reasoning:** `[notebooks]` is a user-installable optional extra; however these two CVEs cover (a) multipart DoS in the HTTP server and (b) cookie attribute injection in `set_cookie()`. While ipykernel does run a tornado HTTP server, `set_cookie()` is never called in that context. Both are fixed by the tornado bump in PR #63 regardless.
- **Action:** Dismissed `not_used` (cookie path unreachable); bump in PR #63 fixes them anyway.

#### #74, #107, #116 — `pillow` · CVE-2026-25990, CVE-2026-40192, CVE-2026-42311

- **Chain:** `aurora_origin_sdk[notebooks]` → `matplotlib` → `pillow` 11.3.0
- **Reasoning:** Initially dismissed as notebooks-only; revised to true positive after recognising `[notebooks]` is user-installable. Image-loading vulnerabilities (OOB write in PSD, FITS GZIP decompression bomb, PSD tile integer overflow) are reachable by any user who loads image files via matplotlib or `PIL.Image.open()`. Fixed by bump to pillow 12.2.0 on Python ≥3.10 in PR #63. Python 3.9 has no patched 11.x available — accepted risk.
- **Action:** Bumped in PR #63.

#### #88 — `black` · CVE-2026-32274

- **Chain:** `aurora_origin_sdk[development]` and `pydoc-markdown` (doc generation)
- **Reasoning:** Dev-only formatter. Never shipped with the SDK nor imported by runtime code.
- **Action:** Dismissed `not_used`.

### 🟡 False positives (npm / docsite — 37 alerts)

All 37 docsite high-severity alerts were dismissed. The docsite (`docsite/`) is a static documentation site: `docusaurus build` emits static HTML/JS to `../docs` for GitHub Pages. Two buckets:

**Bucket A — build/dev/CLI tooling, never in the shipped static bundle (35 alerts)**

Packages in this bucket run only on the developer's machine or CI build server. None appear in the final HTML/JS shipped to GitHub Pages.

| Alerts | Package(s) | Immediate consumer |
|---|---|---|
| #45, #78, #119, #123, #124, #137, #138, #140, #141, #142 | `axios` | `wait-on` (Docusaurus build/CLI URL poller) |
| #59, #61, #94, #95, #96, #97 | `node-forge` | `selfsigned` → `webpack-dev-server` |
| #31, #36, #99 | `path-to-regexp` 0.1.7 | `express` → `webpack-dev-server` |
| #25 | `path-to-regexp` 2.2.1 | `serve-handler` (`docusaurus serve`) |
| #19, #20 | `ws` 7.x | `webpack-dev-server`, `webpack-bundle-analyzer` |
| #33 | `http-proxy-middleware` | `webpack-dev-server` |
| #139 | `launch-editor` | `webpack-dev-server` |
| #30 | `body-parser` | `express` → `webpack-dev-server` |
| #85 | `serialize-javascript` | terser/copy/css-minimizer webpack plugins |
| #84 | `svgo` | `@svgr/plugin-svgo`, `postcss-svgo` |
| #1 | `trim` | `remark-parse` (build-time markdown parsing) |
| #34 | `cross-spawn` | `execa`, `react-dev-utils` |
| #18 | `braces` | `chokidar`, `micromatch` |
| #81, #82, #83 | `minimatch` | `glob`, `copyfiles`, `fork-ts-checker`, `serve-handler` |
| #91 | `picomatch` | `micromatch`, `anymatch`, `readdirp`, `jest` |
| #129 | `@babel/plugin-transform-modules-systemjs` | `@babel/preset-env` |

**Bucket B — ships to browser, but no untrusted input reaches the vulnerable path (2 alerts)**

| Alert | Package | Reasoning |
|---|---|---|
| #26 | `path-to-regexp` 1.8.0 | Ships via `react-router` for client-side routing; ReDoS is compiled from route patterns, which are author-defined and statically generated at build — not user input |
| #103 | `lodash` 4.17.21 | Ships in client bundle via Docusaurus theme/utils; `_.template` code-injection requires attacker-controlled template strings; the static docs site never feeds untrusted input to `_.template` |

---

## Medium

All 49 medium alerts were dismissed as false positives. Same two-bucket framework as high.

### 🟡 False positives (pip — 8 alerts)

| Alert | Package | CVE | Reasoning |
|---|---|---|---|
| [#132](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/security/dependabot/132) | `idna` | CVE-2026-45409 | Used by `requests` internally to encode hostnames; SDK only connects to hardcoded `api.auroraer.com` and Aurora-issued S3 URLs — no attacker-controlled hostname reaches `idna.encode()` |
| [#93](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/security/dependabot/93) | `requests` | CVE-2026-25645 | CVE is in `extract_zipped_paths()`; certifi ships its CA bundle as a regular `.pem` file — `os.path.exists()` returns `True` immediately and the vulnerable temp-file creation code is never reached |
| [#108](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/security/dependabot/108) | `pytest` | CVE-2025-71176 | `[development]`/`[tests]` extras only |
| [#65](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/security/dependabot/65) | `fonttools` | CVE-2025-66034 | CVE is in `fontTools.varLib` (font building). `matplotlib` uses `fonttools.ttLib` for reading and subsetting — `varLib` is not in the rendering code path. Dismissed even for `[notebooks]` users |
| #86 | `tornado` | GHSA-78cv-mqj4-43f7 | Incomplete cookie validation; `ipykernel` never calls `set_cookie()` |
| #115, #117, #118 | `pillow` | various | Initially dismissed as notebooks-only; revised to true positive for Python ≥3.10 (fixed in PR #63). Python 3.9 accepted risk |

### 🟡 False positives (npm / docsite — 41 alerts)

All 41 dismissed. New packages compared to high severity:

**Bucket A additions (build/dev/CLI tooling):**

| Alerts | Package(s) | Immediate consumer |
|---|---|---|
| #13, #110, #111, #121, #122, #125, #126, #127, #128, #136 | `axios` (more CVEs) | `wait-on` |
| #109 | `follow-redirects` | `axios` (wait-on) + `http-proxy` (dev-server) |
| #2 | `got` | `package-json` → `latest-version` → `update-notifier` → `@docusaurus/core` |
| #47, #48 | `http-proxy-middleware` (more CVEs) | `webpack-dev-server` |
| #49, #50, #133 | `webpack-dev-server` | dev server itself (source-theft attacks require developer to visit malicious site while running it) |
| #79, #80 | `ajv` | `schema-utils` → webpack plugins |
| #112 | `brace-expansion` | `minimatch` |
| #145 | `joi` | `@docusaurus/utils-validation`, `wait-on` |
| #56, #57 | `js-yaml` | Docusaurus content plugins, `cosmiconfig` |
| #22 | `micromatch` | `@docusaurus/utils`, `fast-glob`, `http-proxy-middleware` |
| #35 | `nanoid` | `postcss` |
| #114 | `postcss` | CSS processor (build-time; all styles author-controlled) |
| #62 | `qs` | `body-parser` → `express` → `webpack-dev-server` |
| #135 | `uuid` | `sockjs` → `webpack-dev-server` |
| #131 | `ws` 8.x | `webpack-dev-server`, `webpack-bundle-analyzer` |
| #90 | `yaml` | `cosmiconfig`, `cssnano` |
| #23 | `webpack` (AutoPublicPath DOM Clobbering) | Build bundler; DOM Clobbering requires injecting attacker-controlled HTML — static site has no user-submitted HTML |
| #38, #60, #92, #134 | `serialize-javascript`, `node-forge`, `picomatch` (medium variants) | Same as high-severity counterparts |

**Bucket B additions (ships to browser, no untrusted input):**

| Alerts | Package | Reasoning |
|---|---|---|
| #42, #43, #44 | `@babel/helpers`, `@babel/runtime`, `@babel/runtime-corejs3` | CVE-2025-27789 ReDoS in transpiled named-capture-group helpers; ships in bundle but only triggered by regexes processing user input — static docs site has none |
| #41 | `prismjs` | Ships for syntax highlighting; CVE-2024-53382 DOM Clobbering requires injecting attacker-controlled HTML — all content is trusted static docs |
| #69, #102 | `lodash` (more CVEs) | Prototype pollution in `_.unset`/`_.omit`; ships in bundle but requires attacker-controlled input to those functions |

---

## Low

### 🔴 True positive → fixed in PR #63

#### #146 — `tornado` · CVE-2026-49854 · [Alert](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/security/dependabot/146)

- **Chain:** `aurora_origin_sdk[notebooks]` → `ipykernel` → `tornado` 6.5.1
- **Reasoning:** Out-of-bounds read in `websocket_mask()` C extension, reachable from the XSRF token decoder when `xsrf_cookies=True` and the native speedups extension is loaded. `ipykernel` uses tornado WebSockets for kernel communication, making this potentially reachable by `[notebooks]` users.
- **Fix:** tornado → 6.5.7 in PR #63.

### 🟡 False positives

#### #100 — `Pygments` · CVE-2026-4539 · [Alert](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/security/dependabot/100)

- **Chain:** `aurora_origin_sdk[notebooks]` → `ipykernel` → `ipython` → `pygments`; also `aurora_origin_sdk[development]` → `pytest` → `pygments`
- **Reasoning:** CVE is in `AdlLexer` — the Archetype Description Language lexer, used for medical record modelling files (`.adl`). IPython uses Pygments to highlight Python code; the ADL lexer is never invoked. Advisory also notes "attack is only possible with local access."
- **Action:** Dismissed `not_used`.

#### #27, #28, #29, #32, #51, #52, #70, #71, #72, #75, #120 — npm docsite (11 alerts)

All dev/build tooling chains through `webpack-dev-server` or `@docusaurus/core` build utilities. Never shipped in static output.

| Alert | Package | Via |
|---|---|---|
| #120 | `axios` | `wait-on` |
| #52 | `brace-expansion` | `minimatch` |
| #32 | `cookie` | `express` → `webpack-dev-server` |
| #70 | `diff` | `ts-node` → `postcss-loader` / `cosmiconfig-typescript-loader` |
| #29 | `express` | `webpack-dev-server` |
| #51 | `on-headers` | `compression` → `webpack-dev-server` |
| #75 | `qs` | `body-parser` / `express` → `webpack-dev-server` |
| #28 | `send` | `express` → `webpack-dev-server` |
| #27 | `serve-static` | `express` → `webpack-dev-server` |
| #71, #72 | `webpack` (buildHttp SSRF) | `buildHttp`/`HttpUriPlugin` not configured in `docusaurus.config.js`; build-time only |

---

## Prioritised action table

| Priority | Action | Status |
|---|---|---|
| 1 | Merge [PR #63](https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk/pull/63) — closes urllib3 (#66, #67, #68), tornado (#146), and also bumps pillow and tornado for the `[notebooks]` extra | ⏳ Open |
| 2 | Monitor for pillow 11.x security backports for Python 3.9 (no upstream fix exists today; accepted risk) | 🔵 Watch |
| 3 | Monitor for urllib3 security backports for Python 3.9 (CVE-2026-44431; no upstream fix exists today; accepted risk) | 🔵 Watch |
| 4 | Consider upgrading `@docusaurus/core` to a version that pulls in patched transitive deps (would address the large docsite false-positive surface in one shot) | 🔵 Consider |
