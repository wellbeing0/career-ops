# Verification

Implementation is authorized; release activation remains owner-run.

Local tests cover reviewed registration, unchanged primary CV, canonical numbered report/JD, Evaluated-only status, initial status ledger, immutable original review, backup, idempotency and duplicate posting refusal. Fault injection exercises write-ahead replay and refusal after unrelated tracker changes. Canonical tracker-lock contention is tested against another process; automatic backup refuses pending registration journals. Candidate-bound IDs, symlink escapes, stale quality/evidence fingerprints, exact resume extraction, unavailable check coverage and inert external HTML/image text are tested.

## Qualified staging release

Release: `/home/codex-deploy/apps/career-ops-editor/releases/20261008-application-export-01`
Source commit: `b117c122aec731bda887bbf012e0fcbe30f0e9dc`
Seal: 689 system-code files, both candidate build IDs, all four public guide hashes and source-commit manifest.

- All 902 web tests passed; 17 Python portal tests passed; TypeScript check passed; OpenSpec strict validation passed. Autonomy check found no installed OpenSpec skill copies; no skills were changed.
- Both production builds passed. The first staging build exposed an external dependency symlink constraint; copying existing web dependencies into this isolated release resolved it without changing the live release. A browser qualification exposed missing native-runtime import handling for checker modules; this was repaired using the existing webpack-ignore import convention and the complete flow rerun.
- Final fictional browser acceptance passed phone (390×844) and desktop themes, interaction feedback, all existing guided tasks, evaluated-record creation, immediate Applications refresh, explicit PDF acknowledgment, actual PDF save/download, document visibility and candidate isolation with zero browser page errors. Eight non-billing stub calls, zero paid/provider calls. Prior guided model trials are not claimed as new export trials.
- A four-page US Letter fictional resume was rendered by the actual VPS Chromium PDF engine. Every final page was rendered and visually inspected locally. Text extraction, Unicode name, page numbering, wrapping and intact short employment blocks passed. External HTML/script/image text remained inert; rendering disables JavaScript and blocks network requests. This is a text-based layout and diagnostic keyword coverage, not an ATS acceptance guarantee.
- PDF/check saves retain a private original-render/checksum receipt for immutable retries. Registration uses both hosted backup coordination and the canonical tracker lock, with private prior tracker copies and expected-hash journal recovery. The canonical report keeps the exact JD/original review and uses reviewed company/role/score fields in its first Machine Summary; remaining summary fields are still AI review material.
- Current candidate services and both backup timers remained active. No production candidate documents or facts were changed for qualification; no OpenClaw provider configuration or credentials were changed.

Private fictional acceptance evidence: `/home/codex-deploy/.local/share/career-ops-tests/application-export-20261008`.

## Owner activation handoff

```sh
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261008-application-export-01/portal/deploy/activate-application-export.py
```

The root helper verifies the seal, both build IDs and guide hashes, preserves rollback env/unit records, and switches candidate-specific code plus backup helper references. `--rollback` restores prior definitions without removing candidate documents. Shared login, authoritative roots, model configuration, history and backup timers remain.

After activation, verify both live workspaces and deployed guide context. Find the two new actions in Documents; only current hosted evaluation Markdown can be registered, and current Markdown CV/application documents can be exported. Source/primary/selected evaluation changes after review require refreshed checks. Number/title/keyword checks explicitly expose incomplete coverage and are not comprehensive factual verification. Owner activation and bounded live acceptance are complete; see below.


## Live verification after owner activation — 2026-10-08

Steve ran the activation helper successfully. Both live candidate services use the `20261008-application-export-01/web` directory. Both backup timers are active and their services reference this release's backup helper. The deployed public guide manifest binds all four updated guides to source commit `b117c122aec731bda887bbf012e0fcbe30f0e9dc`.

Authenticated Chromium at 390×844 verified both current CV document cards: Review and export PDF opens, Run quality review completes against actual candidate-local files, the PDF save button remains disabled without acknowledgment, pointer feedback and dark theme work, and the page has no horizontal overflow or browser errors. Applications opens successfully. No candidate document, registration or PDF was saved by this live UI check. Neither workspace yet contains an eligible current `reports/hosted-*.md` evaluation, so registration remains covered by the qualified fictional end-to-end test rather than a fabricated production record. Actual PDF rendering/download is likewise covered by staged fictional qualification; no real candidate PDF was generated merely to test deployment.

One authorized read-only website Assistant conversation per candidate completed. Both replies identified this release and the correct GitHub repository, explained Documents → Record reviewed evaluation → Save as Evaluated and Documents → Review and export PDF, and correctly stated the diagnostic limits and no-submission behavior. Primary files were hash-identical before and after each conversation; only normal conversation records were created. Private reply evidence: `/home/codex-deploy/.local/share/career-ops-tests/application-export-context-verification.json`.

Anonymous document API access returns 401. Public OpenClaw `/v1/models` and POST `/v1/chat/completions` return 404. Existing authentication and public API restrictions remain. This verifies deployed routing, real quality-check execution and Assistant guide delivery; it does not claim that a candidate has reviewed/applied to a job or exported an application.
