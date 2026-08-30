# {{PROJECT_NAME}} — HADH (process)

You are the main session. Your job is the flow below. The hooks hold the
boundaries, so spend your attention on the work — not on policing authority.

## Flow
- On `main`/`master` you're in ideation: discuss, shape ideas into FML entries.
  No feature code on `main`.
- Start real work by cutting a branch.
- Features go **Spec → Plan → Code**: write the spec and plan, commit them on the
  branch, and let the operator review before code lands. Pure bug fixes skip to the fix.
- Delegate the build to an `implementer` subagent; review the actual diff before accepting.
- Land everything through a PR. Never commit straight to `main`.

## Ledger (FML)
- Remembered capabilities live in `docs/fml/`. Edit `docs/fml/fml_data.py`, then run
  `python3 docs/fml/generate_fml.py`. Never hand-edit generated files.
- Idea → capture as an FML (`life=captured`). Bake it (→`woven`) before building.
- One lifecycle transition per PR — bake, spec+plan, and build land separately.
  Ideation-capture is docs-only: auto-merge it immediately.

## Docs
- Any PR updates every document its change touches. Nothing is marked live until the
  work is shipped and accepted.

## Orient
- graphify (code/doc structure) and claude-mem (past sessions) orient you; verify
  against the canonical repo docs before acting.
- Before the closing PR, refresh orientation: run `graphify check-update <path>`, and if
  it flags `needs_update`, `graphify update <path>` (incremental — never a full rebuild).
  Confirm claude-mem captured the session.

## Gates
- If a command is blocked, a gate did it — return to the flow, don't fight it.
- You can do more than a heavy contract implies. If unsure whether you can do something,
  try it before refusing.

<!-- BEGIN PROFILE OVERLAY -->
<!-- Project-specific rules are appended here by bootstrap from the profile. -->
<!-- END PROFILE OVERLAY -->
<!-- HADH:LOCAL:BEGIN -->
<!-- HADH:LOCAL:END -->
