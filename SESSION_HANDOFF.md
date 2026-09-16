# Fathers — session handoff

## Epistula Canonica live ship (2026-09-15 ~2:41 PM ET)

- tip-ready OK; verify_docx OK; Canones GR Canon I locked; scaffold discarded; Pass A≠B OK
- Deploy: https://5590190c.fathers-site.pages.dev
- Live: https://fathers.saneapps.com/works/gregory-thaumaturgus-epistula-canonica/
- Also live: https://fathers.saneapps.com/works/gregory-thaumaturgus-ecclesiastes-metaphrase/
- live_works=43; held=577
- Claims remain prepped
- Next densify: serapion, epiphanius-* (still scaffold English — need real-lock)


## Ecclesiastes metaphrase live ship (2026-09-15 ~2:36 PM ET)

- tip-ready OK; verify_docx OK; MGR Greek Cap. I tip locked (TLG 2063.006); scaffold English discarded; Pass A≠B OK
- Publication review registered (scope + section 1); catalogue kept
- Deploy: https://1b34f63e.fathers-site.pages.dev
- Live: https://fathers.saneapps.com/works/gregory-thaumaturgus-ecclesiastes-metaphrase/ → HTTP 200
- live_works=42; held=578
- Claim greg-thaum-eccl-metaphrase-densify remains prepped
- Next densify: epistula-canonica, serapion, epiphanius-* (real-lock standard)


Updated 2026-09-15 12:38 PM ET. Nemesius tip shipped live (see below).

## Nemesius live ship (2026-09-15 12:38 PM ET)

Stephan approved live ship. CoS spot-check: tip-ready OK, verify_docx OK, English 1.1–1.3 real Pass B, OCR Greek damaged but disclosed.

- tip-ready: `nature_hominis_english.json` + `nature_hominis_source.json` → ok
- Dry-run / LIVE allowlist includes `/works/nemesius-de-natura-hominis/`
- Deployed via `scripts/ship.sh --skip-build` after artifact-bound visual review (32 screenshots inspected)
- Pages deployment: https://58e0f435.fathers-site.pages.dev
- Live work: https://fathers.saneapps.com/works/nemesius-de-natura-hominis/ → HTTP 200; title **De natura hominis**; Nemesius of Emesa; sections 1.1–3.1 visible
- Live gate: first post-deploy check had 2 SHA mismatches on `/` and `/data/search-index.json` (edge cutover lag); recheck → 588 checks, 0 failures
- CSS ?v=898957519c; live works count 34 (includes Nemesius tip)
- CLAIMS: left `nemesius-de-natura-hominis-densify` **prepped** (full-work densify row; tip ship is not full densify done; no established non-ai_promote densify-tip stamp)

Do not stop/pause OpenCode or unrelated Mini jobs.

## Current state

Deployed successfully through scripts/ship.sh (Nemesius tip live 2026-09-15 12:38 PM ET):
- Production: https://fathers.saneapps.com
- Deployment: https://58e0f435.fathers-site.pages.dev
- Live work: https://fathers.saneapps.com/works/nemesius-de-natura-hominis/
- CSS version: 898957519c
- Built artifact (this ship): e20cd96166986b9b69c88c6f7510aef057e68682bed81c84ed24dfdeab2dfba2

Current screened build publishes 34 live works (583 held), 1923 topic excerpts and 2706 work sections. These counts are not a whole-corpus fidelity certificate.

## Repairs

Author headings and work titles now lead the catalogue. Repeated Available/Unknown labels and unsupported first-English claims are removed. Century chronology and author/title views are corrected. The merged PR1 mobile, search and internal-link fixes are included.

Known scaffolds, contaminated source texts and false complete-work summaries are withheld without deleting corpus files. Blind On Prayer and Exhortation to Martyrdom tip overlays no longer replace whole chapters. Both works remain withheld. The fuller base of On Prayer still omits surviving Greek after a lacuna; it must not be approved merely because it is longer.

Seven topic citation collisions and nine collective-letter fragment collisions are fixed while preserving existing canonical links. Numerical locus sorting restores canonical JSON order for 330 passages across four Julian works. Equal-locus fragments keep source order. Readers see edition references, while unique suffixes remain in route IDs.

A primary-source review corrected two displaced Bible references in Julian, To Florus 1.27. Its exact passage-only packet and receipt are in the corpus under books/julian-of-eclanum/reviews/audit/. Jeremiah 6.1 was corrected against the printed Greek: love, agency, and six Bible targets. It was not newly published by this audit.

## Required gates

Use scripts/ship.sh. It locks publication, requires catalogue and real-browser checks even with --skip-build, requires inspected images tied to the built files, rechecks current published source receipts, and uploads a private immutable copy.

The publication index binds author, work, edition, locus, ordered scope and each passage payload. Legacy hashes remain provisional. Never refresh them to bypass a failed review. New or changed passages require current raw-source-backed semantic review. Samples approve only their selected passages.

Canonical drafting and promotion reject missing evidence, omissions, false or uncertain checks, same-family checkers and stale files. The CF configuration permits two checker families distinct from each configured draft family. Overnight prep remains the default. No inference calls were needed for this audit.

## Verification and evidence

- 27 corpus QA/promotion tests passed.
- Publication attack regressions, 7 JavaScript tests and 2 visual-gate tests passed.
- 4,775 generated pages and 115,587 local links were checked: zero failures, including duplicate IDs.
- 32 Mini Brave view/state images were inspected. Coverage includes desktop, tablet and phone catalogue; search, retry, empty state, focus and menu; reader and Contents; home, author, topic and Explore; actual Help/Methodology copy; and Julian Bible/source details.
- Source/citation order is now an explicit visual inspection item. Dark OS preference preserves the intended light palette.
- Browser receipt: outputs/ui-review/browser-receipt.json
- Deployment log: outputs/audit-final-deploy.log
- Source-order checks: outputs/audit-source-order-dry-run.log
- Corpus tests: outputs/qa-audit/final-regressions.log in the translations repo
- Findings: docs/IA.md
- Visual coverage: docs/UI_REVIEW.md

Live byte comparisons and post-deployment screenshots are recorded below when completed.

The permanent live gate is now in scripts/check_links.py and runs from ship.sh. It checks current homepage, catalogue, search index and assets, then probes every held work URL for a real 404 without scaffold text. The first production run correctly failed: the custom domain returned 200 for all 573 held URLs, while the Pages deployment URL returned 404. Host, URL, prefix and zone cache purges did not clear those old Pages edge objects. A scoped cache Page Rule lacked effect and was removed. The DNS record and original fathers-site binding were restored after a temporary validation experiment. Production was a no-go until the Pages Function allowlist shipped (see below).

## Incident and remaining work

A separate Cursor publishing job restored the old builder from a22c2b7 and pushed c64b187, removing safeguards. Only its unsafe upload process group 35630 was terminated, before completion. Other work and source files were preserved. Do not restore an old builder to add a loader glob.

Source authenticity, completeness and fidelity review remain unfinished for legacy content. Repair held families one at a time through the existing claim queue; do not use catalogue volume as a quality target. No open GitHub issues were returned in either repository during this audit. No Logos recompilation was performed during the website audit.

Shared work guards remain active because other Mini work continues. Do not stop unrelated jobs.


## Withdrawn-URL preservation cache (2026-09-13)

**Symptom:** custom domain returned HTTP 200 for all held `/works/<slug>/` URLs (often with `x-robots-tag: noindex`), while the matching `*.fathers-site.pages.dev` deployment returned 404. Purge by URL/host and zone Cache/Page/Transform checks did not clear it. DNS and the `fathers-site` domain binding were clean.

**Cause:** Cloudflare Pages asset-server preservation for the custom hostname when the current deployment has no file for that path. `_redirects` 404 rules are not enough on that hostname.

**Fix:** `scripts/generate_works_gate.py` writes `functions/works/[[path]].js` (live-slug allowlist) plus staging `_routes.json` (`include: ["/works/*"]`). `scripts/ship.sh` regenerates both after the reviewed artifact is staged. Denied slugs return a synthetic 404 body containing `Page unavailable` and never call `ASSETS.fetch` on the withdrawn path. Keep `_redirects` as a second layer for the deployment hostname. Live gate remains `scripts/check_links.py --live`.

**Verified live 2026-09-13:** deployment `https://edaf2b75.fathers-site.pages.dev`. `check_links.py --live https://fathers.saneapps.com` → 578 checks, 573 held → 404 with `Page unavailable`, 0 failures. A live work (`/works/cyril-adoration-1/`) and `/works/` remain 200. First ship after the Function upload failed the live gate only because of edge cutover lag; ship.sh now probes one held URL for 404 before the full gate.

**Ops note:** Pages Functions on the Workers free plan can "fail open" to static assets when the daily Functions allowance is exhausted — prefer fail-closed for this project in the dashboard if available.


## Gregory Thaumaturgus In annuntiationem tip live (2026-09-15 ~1:45 PM ET)

- Live: https://fathers.saneapps.com/works/gregory-thaumaturgus-in-annuntiationem/ → HTTP 200
- Section: `/1/` → HTTP 200
- Deploy: https://a6ca72bd.fathers-site.pages.dev
- live_works=39; claim left **prepped**
- OpenCode left alone


## Gregory Thaumaturgus Sermo in omnes sanctos tip live (2026-09-15 ~1:55 PM ET)

- Live: https://fathers.saneapps.com/works/gregory-thaumaturgus-sermo-in-omnes-sanctos/ → HTTP 200
- Section: `/1/` → HTTP 200
- Deploy: https://6dba211d.fathers-site.pages.dev
- live_works=40; claim left **prepped**
- OpenCode left alone

