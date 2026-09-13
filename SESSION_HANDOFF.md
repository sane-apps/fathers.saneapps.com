# Fathers — session handoff
Updated 2026-09-13. Owner authorized audit, fixes, source checks and deployment; no further approval needed for this scope.

## Current state
Website implementation verified and ready for canonical deployment. Corpus fixes committed/pushed as c07955e79 in sane-apps/translations. Site commit/deployment receipt follows below after completion.
606 candidate works:573 held,33 retained provisionally.1925topic excerpts;2698work sections. This is a targeted legacy screen, not whole-corpus fidelity certification.

## Fixed
Author headings and work titles dominate the catalogue; removed repeated Available/Unknown and unsupported first-English labels. Century chronology and author/title views fixed. Incorporated mergedPR1 mobile/search/link fixes.
Known scaffold, contaminated sources and false complete-work summaries are withheld without deleting corpus files. Removed blind OnPrayer/Martyrdom tip overlays; both works remain held. BaseOnPrayer also omits surviving Greek after a lacuna; do not approve it from the fuller text alone.
Seven topic citation collisions and nine collective-letter fragment collisions fixed while preserving existing canonical links. Shared numeric locus sorting restores canonical JSON order for330passages across fourJulianworks; repeated-locus fragments keep source order. Reader labels hide internal id suffixes.
Source review corrected JulianToFlorus1.27's two displaced Bible refs; exact passage-only packet/receipt under corpus books/julian-of-eclanum/reviews/audit/. Jeremiah6.1 love/agency/sixBibletargets corrected againstprint; not newlypublished here.

## Mandatory gates
Use scripts/ship.sh only. It holds an exclusive kernel lock, requires catalogue/actualbrowser/image review even with --skip-build, rechecks current published source receipts, and uploads an immutable reviewed build copy.
The publication index binds identity, edition, locus, ordered work scope and per-passagepayload. Existing legacy hashes are provisional; never refresh them to bypass a failure. New/changed passages need current raw-source-backed semantic review; samples approve only selected passages.
Canonical draft/promotion now reject missing evidence, omissions, false/uncertain checks, same-family checkers and stalefiles. Config supports two independentCFcheckerfamilies; overnightprep remainsdefault. No inference calls were needed for this audit.

## Verification
27corpusQA/promotion tests pass. Site catalogue/publication attack tests,7JS tests,2visualgate tests,allgeneratedlinks/anchors/duplicateids pass.
32MiniBraveview/state images inspected,includingphone/tablet/desktop catalogue,search/retry/empty/focus/menu,reader/Contents,templates,actualHelp/Methodologycopy andJulianBible/source details. Citationorder is now an explicit visualcheck. DarkOSpreference preserves intendedlightpalette.
Approvedartifact:4a7a9381ed0f51a58cec9910ce944c9e507a5d34ccb52af186dadf111b871bd7
Runner:0f85c45ec81f441c0b89226161a71f415a666cb5c31b724d414e7ea79e83cb3c
Receipt:outputs/ui-review/browser-receipt.json
Logs:outputs/audit-source-order-dry-run.log;corpus outputs/qa-audit/final-regressions.log.
Full findings:docs/IA.md;visualcoverage:docs/UI_REVIEW.md.

## Incident and remaining work
A separateCursorpublisher restored oldbuildera22c2b7 and pushedc64b187, removing safeguards. Only its unsafeupload processgroup35630 was terminated beforecompletion. Preservedsourceandotherwork. Do not restoreoldbuildertoaddglobs.
Sourceauthenticity/completeness andfidelityreviewremainunfinishedforlegacycontent. Repairheldfamilies one at a time usingexistingclaimqueue; no catalogue-volume target. NoopenGitHubissuesreturnedbyghissue list in eitherrepo. NoLogosrecompileperformed duringthissiteaudit.
SharedworkguardsremainactivebecauseotherMiniworkcontinues; do not stopotherjobs.
