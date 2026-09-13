# Fathers — session handoff

Updated 2026-09-13. The owner authorized the audit, repairs, source checks and deployment.

## Current state

Deployed successfully through scripts/ship.sh:
- Production: https://fathers.saneapps.com
- Deployment: https://805826ea.fathers-site.pages.dev
- Site implementation commit: e5e5b18
- Corpus implementation commit: c07955e79
- CSS version: 898957519c
- Built artifact: 4a7a9381ed0f51a58cec9910ce944c9e507a5d34ccb52af186dadf111b871bd7

The screened build has 606 candidate works: 573 withheld and 33 retained provisionally. It publishes 1,925 topic excerpts and 2,698 work sections. These counts are not a whole-corpus fidelity certificate.

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

The permanent live gate is now in scripts/check_links.py and runs from ship.sh. It checks current homepage, catalogue, search index and assets, then probes every held work URL for a real 404 without scaffold text. The first production run correctly failed: the custom domain returned 200 for all 573 held URLs, while the Pages deployment URL returned 404. Host, URL, prefix and zone cache purges did not clear those old Pages edge objects. A scoped cache Page Rule lacked effect and was removed. The DNS record and original fathers-site binding were restored after a temporary validation experiment. Production must remain a no-go until the custom domain serves the same 404s as the Pages deployment.

## Incident and remaining work

A separate Cursor publishing job restored the old builder from a22c2b7 and pushed c64b187, removing safeguards. Only its unsafe upload process group 35630 was terminated, before completion. Other work and source files were preserved. Do not restore an old builder to add a loader glob.

Source authenticity, completeness and fidelity review remain unfinished for legacy content. Repair held families one at a time through the existing claim queue; do not use catalogue volume as a quality target. No open GitHub issues were returned in either repository during this audit. No Logos recompilation was performed during the website audit.

Shared work guards remain active because other Mini work continues. Do not stop unrelated jobs.
