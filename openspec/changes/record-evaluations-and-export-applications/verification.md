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

After activation, verify both live workspaces and deployed guide context. Find the two new actions in Documents; only current hosted evaluation Markdown can be registered, and current Markdown CV/application documents can be exported. Source/primary/selected evaluation changes after review require refreshed checks. Number/title/keyword checks explicitly expose incomplete coverage and are not comprehensive factual verification. Live acceptance remains pending owner activation.
