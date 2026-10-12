---
name: hasf-spec-authoring
description: Use when authoring HASF specs or driving the FML flow (capture/bake/plan/build) in h00pz repos.
---

# HASF Specification Authoring (h00pz repos)

Use when asked to "write the architecture", "write the spec", or produce an
architecture document in a repo that carries HASF (`docs/hasf/current.md`,
h00pz repos such as h00pz-infra). Produces a HASF §5-conformant specification
on a canonical spec branch, ready for operator ratification.

Also covers **pre-plan design shaping** for h00pz architecture — the review
and design conversation that follows a spec and precedes the plan:
- *interrogating an existing spec* — "do we have seams?", "how many
  subsystems?", and gaps between what the acceptance plan tests and what the
  architecture declares — see `references/seams-and-subsystems.md`.
- *designing integration seams* — how the store integrates with external
  tools (monitoring, Ansible/AAP, NetBox), read seam vs write seam,
  grounded-source-not-inventory, freshness gating — see
  `references/integration-seams.md`.

Also covers the **rest of the repo flow after the spec** — capturing and
baking FMLs, writing the build plan, and landing each stage as a PR — see
`references/fml-lifecycle.md` and `references/gitea-and-prs.md`.

Also covers **documenting an existing running subsystem** (e.g. Vault, AAP) as
its own grounded HASF spec, and the **secret-safe recon + live-config**
procedure that precedes it — see `references/vault-and-secrets.md`.

## Standing rules (apply to every spec you write for this user)

- **Spec stage is target design, not a build plan.** No build slices, no
  build order, no risk tables, no "first we do X, then Y" sequencing — that
  is the Plan stage. If you are writing steps to execute, stop; you have
  crossed the stage boundary. The user has a name for this failure ("you are
  solutioning") and will reject the document for it.
- **In design conversation, resolve a new field down the grade ladder before
  proposing a mechanism.** When the operator names a new attribute ("is it
  applied", "where is it applied"), ask in order: is it OBSERVABLE (grade O —
  a wire probe / file read)? DERIVABLE from existing convention or tags
  (grade D)? and ONLY if neither, does it need an ASSERTED writer (grade A)?
  The recurring failure is reaching straight for a new collector, a store
  write-back, or an explorer discovery pass for something an existing
  observation or the tag convention already covers — the operator collapses
  it ("is it applied is observation-based"; "where is it applied goes back to
  the profiles/tags"). Propose the MINIMAL model grounded in what is already
  built; add a data source or a writer only when the estate shows the pain,
  not on a hypothetical. "Best route, hard work upfront" means getting the
  MODEL right, not building the most machinery. See
  `references/integration-seams.md` for the worked collapses.
- **A machine gate that means to REPLACE a human judgement relocates the
  judgement, it does not remove it — scale the machine's verdict authority
  with how much the estate already KNOWS.** When the operator wants inference
  to stand in for judgement (a fail-closed corroboration gate, a classifier, a
  validation threshold), a FIXED rule/signature/threshold IS the recognition
  trilemma: too specific and true positives fall out (nothing gets in), too
  wide and false positives sail through (everything gets in), and the
  rule has to be authored by SOMEONE — hand-authored is the NetBox rot the
  store exists to kill, agent-authored under starvation is the confabulation
  you were trying to stop. So a fixed rule just moves the judgement to whoever
  writes it. Resolve it like a brain recognizing against known knowledge:
  (1) ground the check in the OBSERVED SHAPE of the already-RATIFIED
  exemplars, not a written pattern — specificity is then LEARNED from the
  corpus and sharpens as more members are ratified (grade-D off the live
  vocabulary), never a dial a human sets too-tight/too-loose; (2) verdict
  AUTHORITY is gated by corpus sufficiency — when the corpus is too thin to
  discriminate the machine CANNOT EARN a reject, so it flags-and-passes to the
  human ratification gate (fail-closed = *defaults to the human*, NOT
  defaults to machine-no; a reject it can't ground floods the human with
  actually-known items, the too-specific horn); (3) the machine does only the
  cheap repeatable half — "have I seen this before?"; the human keeps the real
  judgement — NAMING the genuinely-new — and the residue of that naming (the
  ratified vocabulary) IS the corpus the machine recognizes against. Cold
  start is a newborn brain: the first member has no exemplar to resemble, so
  it falls through to the human and becomes exemplar #1; recognition
  accumulates, it is not supposed to work on day one. Surface the
  not-recognized branch LOUDLY (recognition-against-known biases toward the
  familiar and can suppress the genuinely-new, the one failure the estate
  refuses). Real discrimination is usually BLOCKED on corpus enrichment
  (richer observed shape) — land the seam + the authority-scaling now, the
  sharpening arrives later for free as its own dependency edge.
- **Resolve a new concept to a FIELD-BUNDLE on an existing kind before
  minting a new record kind.** When a new attribute ("what is stateful about
  this app") looks like it needs its own kind, first ask whether it can ride
  as a *sparse* field-bundle on a kind that already exists — present only
  where relevant, absent where not, and the absence itself is often a useful
  scope (stateful-vs-disposable = the backup scope). Mint a new kind ONLY
  when the thing needs identity or a lifecycle independent of any existing
  record. WHY: a fixed kind-count model (the estate's seven kinds / ADR-007)
  is a load-bearing invariant; an eighth kind is queryable no better than a
  populated field and costs the invariant. This is the structure-level twin
  of the grade-ladder rule above — resolve DOWN before adding machinery.
- **When the operator DOES decide a new kind is warranted, execute it as a
  design-only supersession — never a quiet edit, and never as code in the
  same pass.** A recurring class with distinct semantics and its own
  identity/lifecycle (e.g. a substrate other things run *on*, when more of
  them are coming) is the deliberate exception to resolve-down, and the
  operator owns that call. When they make it: (1) SUPERSEDE the invariant's
  ADR openly — amend the old ADR's consequence to `superseded by ADR-NNN`,
  mark its revisit trigger *triggered*, and write a NEW continuously-numbered
  ADR carrying the decision and re-closing the set at the new count (a
  further addition faces the same bar); do not silently rewrite the old ADR's
  text. (2) TRACE THE BLAST RADIUS before writing the ADR — grep code, tests,
  and docs and probe the live store for every place the old invariant is
  asserted (the kind registry, the validator's count/reject message, per-kind
  field/ownership/derive tables, the seed, and the tests that assert the old
  count), and record that map as the deferred build's scope. "Figure out the
  implications" IS the design work, not a follow-on. (3) Keep the change
  DOCS-ONLY: the ADR + spec section + a fresh `captured` build FML are the
  design; the enforcement code and any live-store data migration are the
  BUILD — defer them, touch no store `.py` in the design PR, and do NOT
  falsify the live FML that still describes the invariant (see
  `references/fml-lifecycle.md`).
- **In design conversation, TALK — no multiple-choice menus.** This operator
  works discussion-first and rejects clarify-style menus outright ("I hate
  menus, only conversations"). When a design fork needs his input, state your
  honest read of the options and the tradeoff in prose and ask the open
  question; do not fire single/multi-select forms with recommended options —
  he will skip them and tell you to stop. WHY: a menu pre-commits the framing
  to your enumerated choices and asks him to pick, which is the opposite of
  the lateral, falsifying reasoning he uses design walks for; prose keeps the
  fork open for him to reframe. Reserve structured questions for genuinely
  independent, non-design logistics.
- **The operator drives design by Socratic questioning — converge on the
  evidence, do not perform novelty.** He walks you through cases
  deliberately so you rebuild the reasoning chain and reach his conclusions
  with the evidence in hand; that is the method working, not you
  discovering. Converge when a case earns it, push back where the framing is
  genuinely net-new, and never dress a conclusion he led you to as your own
  insight ("you just defined what the estate is for") — it reads as a mirror,
  and he wants a partner who *falsifies*. State honestly which forks were his
  prior versus where you actually added something. WHY: the deliverable of a
  design walk is a reconstructable evidence chain each field can be defended
  from at review, not agreement; a walk that only nods produces a spec no
  reviewer can challenge.
- **When the operator declares a milestone reached ("we have X now!"), trace
  the actual chain to the deliverable and name the remaining gap BEFORE
  agreeing — celebration is not a status report.** A ratified artifact is not
  the live capability: a merged recipe/spec/PR is the DESIGN or the PROPOSAL,
  and the composed, queryable result still needs the executor to run and the
  store to compose it. Walk the full observe→derive→compose chain, mark each
  link done/undone with evidence (grep for the missing executor; probe the
  live store's image/kinds), and separate "the discovery half works" (tonight's
  real win) from "the composed artifact exists as a live read" (deploys away).
  WHY: this operator wants a partner who falsifies over one who mirrors, and
  "we have X" quietly becoming "we're done" is exactly the drift he relies on
  you to catch. Deliver the honest asterisk warmly — name the win, then the
  gap.
- **Architecture is end state, no as-built.** The document specifies the
  target; where the estate is not yet in that shape, the estate moves to the
  document. No hedging prose like "currently not verified, but…".
- **After a context/memory blowout, reconstruct state from git, never from
  recall — and say so.** When compaction failed and context capped (memory is
  lossy or stale), the surviving truth is the repo: `git log --all --oneline`,
  `git branch -a --contains <sha>`, and `git merge-base --is-ancestor <sha>
  master` to place work; read the actual SKILL.md/config/code on the branch;
  and RE-RUN the suite rather than trusting a commit message's "N tests green".
  A recent PR often carries the work you think was lost — check whether its
  branch merged to master before assuming anything must be rebuilt. WHY: this
  operator will tell you plainly that you "lost memory"; treating your recall
  as authoritative there fabricates a rebuild that git shows is unnecessary.
  Separately reconstruct what git CANNOT hold — the design conversation's
  reasoning and open forks — and name that gap rather than inventing it. To
  recover that reasoning, the cross-session tool is `session_search`
  (discovery shape: `query=`; then scroll `session_id`+`around_message_id`);
  it is NOT named `chat_history_lookup` and is deferred (find it via
  tool_search "session_search", not the catalog name). But it can come back
  EMPTY — a still-open session isn't indexed until it closes, and a thin index
  returns nothing for the topic. When recall genuinely fails, SAY "history
  lookup couldn't recover it" and rebuild the shape from what the operator
  tells you now; never present a reconstructed-from-guess design as the
  recovered prior decision.
- **ADR statuses reflect operator decisions only.** Mark an ADR `accepted`
  only when the operator explicitly decided it (quote the decision in the
  status). Everything else is `proposed` (your proposal, requirement ratified)
  or `unresolved` (operator asked for more info). Never write "my lean" as a
  disposition — a suggested disposition is labeled as such and the status
  stays unresolved. After writing, re-check every ADR status against the
  operator's actual words; an ADR marked accepted that the operator never
  decided is the failure mode. Across review rounds, **number ADRs
  continuously** (a round-2 ADR is 007, not a re-open of 001) and cite the
  round in the status (`accepted (operator, review round 2: "…")`); a
  single ADR may be **partly accepted** (the requirement is ratified) with
  the modeling/mechanism still `unresolved` — state both halves.
- **Never invent document structure from memory.** Read the framework's
  required-structure section before writing a single line of the doc. The
  section list is load-bearing; a home-grown structure gets rejected even
  when the content is right.
- **A subsystem gets its own spec, not an appendix to its consumer.** When a
  distinct piece of infra (a credential broker, a message bus, an executor)
  has its own lifecycle, trust boundary, and failure modes, write it as a
  standalone HASF spec that the consumer's spec cross-references — do not bury
  it as a section or a runbook under the thing that happens to use it. The
  operator will ask for this explicitly ("it's also a subsystem of our
  infra"); recognize it first.
- **Documenting an EXISTING running system: the spec is grounded in read-only
  recon, and §AD records CURRENT-STATE observed facts** (version, mounts,
  auth methods, config) as the verified starting point — distinct from the
  target, which is stated as target. This is the one place "as-built" facts
  belong in a spec: a labeled current-state row in §AD/§W, never as a hedge in
  the body. Name each observed gap as WORK (an ADR), not as a caveat. See
  `references/vault-and-secrets.md` for the recon procedure.
- **Never handle a credential in chat or in shell history.** To load a token
  onto a host, have the operator paste it into a silent reader
  (`read -rs`) that writes a root-`600` file and prints only a byte count;
  never echo it, never accept it in conversation, never pass it as a command
  argument. Recon and config print only non-secret fields (names, shapes,
  policies, TTLs) — never a secret value. See `references/vault-and-secrets.md`.
- **One lifecycle transition per PR.** The spec *weaves* captured FMLs
  (feature-recall pass) but promotes none; capture/bake/spec+plan/build land
  in separate PRs.
- **When the operator asks whether new design work alters an existing
  capability, separate the ACTUATOR/pipeline from the DATA MODEL — do not
  answer with a flat "no".** A new design often leaves the running pipeline
  untouched *and yet* identifies new fields the underlying store must carry
  (e.g. reasoning through a deployment model surfaces per-point observation
  fields the existing renewal flow never had). A clean "no" that ignores the
  fields you identified will be corrected ("right but we DID identify fields
  needed in ground to support X"). Name both halves: what stays the same
  (the gated launch, the coupled v0) and what the design added to the model
  (the new observed fields, and which future split depends on them).
- **Under an explicit full-auto grant, execute and delegate deeply and prepare
  a coherent return report** ("how everything is working") for when the
  operator is back — but do NOT sweep real host mutations or shared-estate
  changes under it. Restarting a shared model other services use, or changing a
  host, still warrants a deliberate pause and (where feasible) confirmation;
  full-auto covers the build-and-land flow, not estate surgery. The operator
  picks the cautious path here (pilot-on-one-host-first) — offer it.
- **Check the FML ledger BEFORE planning or building — the recurring
  failure is skipping it.** A merged spec does NOT mean the capability is on
  the ledger; a spec can land over an empty slot. The flow is idea →
  *capture* (`life=captured`) → *bake* (`life=woven`) → spec/plan → *build*,
  and only a baked (`woven`) FML is build-ready. Before writing a plan or any
  code, read `docs/fml/ledger.md`; if the capability has no FML entries,
  capture them first (docs-only, auto-merge), then bake, each as its own PR.
  Decompose fine-grained (one capability/seam per FML), never a few coarse
  chunks — see `references/fml-lifecycle.md`.
- **When the feature has a human UI, prototype it before the plan locks.**
  The operator wants to *see* the surface and iterate to think laterally and
  surface what the spec missed — do this before committing the build. Build
  it as a spike (see the `spike` skill): a single self-contained HTML file,
  no framework/CDN/build step (matches the estate's KISS/air-gapped
  reality), seeded with realistic estate data, kept OUTSIDE the repo tree so
  it can't be mistaken for product code or dirty the branch, served with
  `python3 -m http.server` on the host so you can hand the operator a real
  URL (`hostname:port`). Wire in a state switcher that exercises the
  spec's forbidden UI states (stale, API-down/stale-mirror, empty) so the
  operator can feel the discipline, not just read it. The switcher is a
  test harness, not a product feature — say so, and do not let it leak into
  the spec as a real surface.
  - **When the product ALREADY has a live UI + API, GROUND the prototype in it —
  copy the real page and proxy to live data; do NOT hand-build fresh chrome +
  seed.** For a NEW surface that extends an existing shipped SPA (e.g. adding
  per-asset Details/CRAP/Timeline subpages to the estate page's record
  detail), the honest spike is: copy the real `app/assets/<page>.html`, extend
  its real render functions (reuse its nav/subnav/CSS verbatim — add a state
  var + a subnav + a new render fn), and serve it behind a tiny stdlib proxy
  that forwards `/api/*` to the LIVE store (self-signed → unverified ctx) so
  it renders REAL composed data. The operator's correction is literal: a
  freestanding page with invented nav + seed data draws "this is not grounded
  in ground" / "with the current navigation this page would show up under
  estate→kind→asset" — the surface must live INSIDE the existing navigation
  and read the real read-model, and a from-scratch mock also can't show the
  honest-PARTIAL state that is the whole point (profiles ratified but 0 CIs
  observed today) unless it pulls the actual store. Seed-only self-contained
  mocks are right ONLY when no product UI/API exists yet.
  - **Iterate one concern per round.** The prototype is a conversation
    driver: each reload the operator surfaces one missed seam or concept
    (an integration, a domain distinction, a new sub-view). Wire that one
    concern in, reserve it back, and only then move on — batching several
    guesses per round wastes the lateral-thinking loop.
  - **Fold every surfaced concept back into the spec before the plan
    locks** — a new ADR, section text, a forbidden-outcome, an acceptance
    class. The prototype's value is the spec edits it provokes, not the HTML.
  - **Never seed convention-derivable values as hand-asserted data.** If a
    value follows a rule (a console URL = `https://{fqdn}:{port}`), derive
    it at render time (grade D) from one convention constant; typing it per
    record is the NetBox data-entry rot the store exists to kill, and the
    operator will catch it.
  - **Sanity-check a single-file HTML spike before serving:** extract the
    `<script>` body and `new Function(body)` it (node) to catch syntax
    errors, then `curl | grep` for the markers you just added — a broken
    inline script fails silently as a blank page.
  - **After the operator approves a prototype ("that's perfect"), "capture
    it" / "do it now" is AMBIGUOUS — confirm ledger-capture vs
    build-and-ship before acting.** A warmly-received prototype often means
    the operator now expects the BUILT artifact IN THE PRODUCT, not just an
    FML idea logged. The recurring miss: reading "capture" in the strict FML
    sense (a docs-only ideation entry) when the operator meant "port this
    into the real code and deploy it" — he was genuinely surprised to find
    only a ledger entry where he pictured shipped code ("I thought you wrote
    the code for it after the prototype landed perfectly"). When the two
    readings diverge, name both and ask. WHY: the prototype's whole value is
    the build it unblocks; treating approval as the finish line strands the
    work one step short. When it IS a build off an already-LIVE endpoint
    (read-only UI, no new backend), the bake may be folded into the build PR
    (state it in the commit) so port+deploy is one pass, not three gated PRs.

## Procedure

1. **Confirm the framework.** Read `docs/hasf/current.md` → the framework
   file. Read its required-spec-structure section (and the naming contract
   sections) end to end before drafting. Do this even if you've read the
   framework before in the session — the structure list must be in front of
   you while writing.
2. **Run the feature-recall pass.** Read `docs/fml/ledger.md` (and
   `fml_data.py` if the ledger is stale). Classify every captured FML: how
   the spec touches it, which section weaves it. This is a required section
   of the spec, not an optional appendix.
3. **Preflight with the real system when access exists** (§AD discipline):
   run the read-only commands (`oc get …`, API probes, etc.) and record
   verified rows. Every unverified capability gets an honest fallback in the
   table — never design around an assumed capability. If the operator
   dismisses a preflight item, record the dismissal as an operator decision
   and move on — do not re-litigate it.
4. **Cut the canonical branch** before writing: `<product-domain>-<capability>/spec`.
   Canonical spec ID and filename per the naming contract: display title
   `<Product or domain> — <Specific capability or operator outcome>
   Specification`, file `<canonical-id>-spec.md`. No `Phase 3` / `PR1` /
   `final-v2` identifiers. Working names (e.g. a product's tentative name)
   are held in an ADR as `unresolved`, not baked into the spec's identity.
5. **Write the spec following the framework's section list exactly.**
   Answer each section or mark it n/a *with a reason* — never skip silently.
   See `references/structure-and-stages.md` for the section map and the
   spec-vs-plan-vs-code boundary table.
6. **Decisions go in ADRs** in the spec's ADR section, each with status,
   context, decision, consequences, alternatives, revisit trigger.
7. **Commit on the spec branch.** Stage only the spec file(s); do not sweep
   pre-existing working-tree dirt (modified AGENTS.md, stray tarballs,
   untracked tokens) into the commit. If the repo has no local git identity,
   take it from the repo's commit history, not from the machine.
8. **Report the unresolved ADRs and open questions explicitly** in the
   summary — those are the operator's to decide, and the spec's stop rule is
   the operator's ratification, not your completion message.

### Revising an already-merged spec

When the spec PR already merged and a later review round (or prototype
iteration) produces changes, this is a **new revision**, not continued work
on the old branch:

- Cut a fresh branch off updated master (`git checkout master && git pull
  --ff-only`, then `<canonical>/spec-r2`). The old spec branch is 0-ahead
  of master — committing there produces nothing mergeable.
- Keep the canonical id and filename; bump the front-matter `Document
  revision` and record the round in it. Supersede in place (same file), do
  not fork a second spec doc — HASF wants one ratifiable architecture.
- **Re-read every section a new concept touches before adding it**, and grep
  for sentences that now contradict the addition. A new surface (e.g. a
  dashboard) can conflict with an existing feature-recall row or a "no X
  surface" line — fix the old sentence, don't append a contradicting one.
- After editing, grep the section headings and ADR list against the file on
  disk to confirm A–AG completeness and continuous ADR numbering, and grep
  for the replacement character to catch mojibake from copied glyphs.

## Pitfalls

- **Crossing the stage boundary is the recurring failure.** The tell: you
  catch yourself writing "slice 1", acceptance criteria per slice, a
  risk table, or a recommendation with a rationale for your preferred
  option. Cut it — that content belongs in the plan, and the ADR stays
  unresolved. WHY: the operator ratifies the architecture before any
  sequencing exists; a spec that smuggles in the plan makes ratification
  impossible and reads as the agent having decided for them.
- **Preflight is verification, not constraint-gathering.** Run it to fill
  the capability table honestly; do not let probe results (e.g. a port being
  closed) drive the design when the operator has declared connectivity an
  estate concern. Record the finding, apply the operator's decision.
- **"End state" cuts both ways.** It also forbids pinning the doc to
  as-built quirks (a tool running in an unexpected place, a legacy artifact
  still in service) — the doc states the target and names the correction as
  work, not as a caveat.
- **Read before claiming the file is complete.** Long writes can land
  truncated or with your own planned tail missing; verify the section list
  against the file on disk (grep the headings) before committing and
  reporting.

## Support files

- `references/structure-and-stages.md` — HASF §5 section map (A–AF + AG),
  the spec/plan/code stage-boundary table, and ADR status discipline.
  Distilled from HASF v1.2.2; re-verify against the repo's framework file
  before relying on it.
- `references/seams-and-subsystems.md` — reviewing a spec for seams
  (testability boundaries) and counting subsystems: the §AC-vs-§V
  cross-check for undeclared ports, common missing seams, the overcounting
  traps, and the deliberately un-seamed live-chain rule.
- `references/integration-seams.md` — designing the boundary between the
  grounded store and an external tool: read seam vs write seam, monitoring
  as a read integration, the store as an inventory *source* (not an
  inventory), freshness-as-a-knob for a blind executor, delivering observed
  state honestly, DNS/zone grounding, provisioning-as-read ("what is free"),
  derive-at-read-time conventions (constructable ≠ reachable), the DNS zone as
 the authoritative self-classifying SEED source (re-grounding an inaccurate
 inventory), the anti-NetBox capability-profile tags as the join key, CI
 identity as a per-profile declaration (`identity:{kind,root,local_key}`, root
 to a vessel/substrate) rather than a rebuilt matching engine, and the
 CI-proposal write gate (classify new/shape-change/value-change; hold shape,
 flow value; hold as a `change` record; the agentic grounded PR report that
 cites evidence and flags hypotheses), the **profile.<tag> corroboration gate**
 (fail-closed recognition against the corpus-learned exemplar signature, not a
 hand-authored pattern; three outcomes; demote-coherently; discrimination
 blocked on service-shape enrichment), the recipe-on-CI model (a recipe is DATA
 ABOUT A THING -> field-bundle on the service CI, tag = capability name, CRAP
 composes per-asset; recipes live in ground, git was only a temporary approval
 ceremony superseded by ground's change-flow — NOT a write path), and
  **monitor-and-rebuild as one purpose-bounded discovery** (emit rebuild-grade
  CIs from day one even while only monitor is wired; exploration open-ended in
  method, capped by purpose not a facet checklist; rebuild-completeness is a
  hypothesis until a restore-test oracle proves it).
- `references/fml-lifecycle.md` — the FML flow after the spec: the ledger
  gate, editing `fml_data.py` + `generate_fml.py` (never hand-edit generated
  ideation-capture (soft-edge-only, held out of the build order),
  fine-grained decomposition, dependency edges, baking
  (captured→woven) past the weave gate (altitude + in-cluster acceptance),
  and recording new design on an already-LIVE capability (capture a fresh FML,
  never rewrite the live one).
- `references/gitea-and-prs.md` — landing PRs in h00pz gitea repos with no
  gh/tea CLI: the Gitea API + `.git-token`, self-signed TLS, auto-merging
  ideation-capture, commit identity from history, keeping working-tree
  dirt out of commits, and authenticated clone/push over HTTP via a
  credential-helper (token never in the URL) incl. setting a file's exec bit.
- `references/build-deploy-openshift.md` — the code stage: reviewing a
  delegated build (re-run tests + drive the live path; the two defect classes
  a green suite misses), UBI9 build + SA-token registry login + pin-by-digest,
  in-cluster token generation, deploy/seed (`oc cp` bare pod name to a
  writable `/tmp` path; `0 committed` = no inventory found; re-seed for a new
  kind; a mixed A+O record is rejected WHOLE so ratify carries only asserted
  fields), a one-off collector Job for collector-based acceptance, the
  read-back-clock staleness pitfall, second-channel value verification,
  stdlib-only image parsing via base binaries, grepping the test tree before
  widening a shared contract, live acceptance as the gate to `deployed=live`,
  the wire-contract check before blaming the code, diagnosing an agentic
  worker run by its OUTCOME line (grant_failed/tool_calls / 403≠401 /
  the stage-by-stage outcome progression grant_failed→parse_failed→PR-step→
  candidate_pr_opened, and parse_failed-after-a-walk = max_tokens truncation),
  the agentic worker whose sole write is a PR must CLONE a token-authed working
  copy first (`/app` is not a checkout; mounted-secret filename must equal the
  key), and when live acceptance is BLOCKED on unattended-unsafe estate config — prove
  the whole workflow with a real-module e2e fed captured input + write the
  operator-fix doc, never fabricate a live result.
- `references/platform-service-integration.md` — wiring an estate worker to
  in-cluster platform services: model serving (KServe Route-not-predictor,
  OpenAI API at `/v1`, pick the ready isvc, **model endpoint+id as a swappable
  deployment env — and a manifest env is dead unless the code reads it**),
  **building a model-driven agentic loop** across swappable models (native
  `tool_calls` vs text-protocol fallback, reasoning-model `<think>`+`max_tokens`
  truncation, over-explorer budget-salvage, 5xx retry, JSON-escape repair,
  prove-on-the-live-model), pacing sweeps against the shared single-GPU replica
  (concurrency wedge, heavy-model crash-loop, cold-start retry,
  model-failure-as-honest-gap), and MLflow tracing (JSON run API not
  OTLP-protobuf, SA-token + `X-MLflow-Workspace` auth where the SA can create,
  enabled≠wired, traces land only in-cluster), plus the
  probe-every-dependency-before-building rule.
- `references/aap-inventory-wiring.md` — the operational AAP consuming side of
  the work-query seam: surveying the live controller read-only
  (`/api/controller/v2/`, read token via silent file), delivery as an SCM
  inventory source from a git project (not UI paste), Route-not-Service +
  verify-TLS + no-token for the off-cluster consumer, script-vs-plugin (prefer
 a stdlib script for a server-filtered feed), the create/sync mechanics
 (private-repo git 403, the exec-bit `Permission denied`, the
 project→inventory sync chain, host-list-equals-work-query acceptance), the
 closing-the-loop caveat (the consumer play is not a drop-in; don't auto-fire
 the actuator at the broker host), **executing the cutover + live renewal**
 (repoint-via-PATCH with rollback record; JTs have NO enabled field; the play
 runs on the CONTROL host so add it as a static inventory member or the run
 false-greens "no hosts matched"; static host survives overwrite-sync; never
 trust status:successful — read PLAY RECAP; second-channel verify on the RIGHT
 port e.g. cockpit :9090; close the loop by re-observation not deploy-trust),
 **surgical-vs-bulk** (renew only the work-query set; ACME duplicate-cert quota;
 `expiring_hosts` override to scope a run), the AAP-controller-cert-is-self-
 signed (`curl -k` the controller API, verify TLS only on the ground Route),
 and the N-asserted→M-observed demonstration number.
- `references/vault-and-secrets.md` — documenting an existing running
  subsystem as its own grounded spec (§AD = current-state observed facts),
  the secret-safe read-only recon procedure (print names/shapes never
  values), the Vault SSH-CA setup done this-estate's-way: bootstrap root
  once → scoped admin token, enable the SSH secrets engine in CA mode, a
  short-TTL signing role, and the safe host CA-trust enrollment (drop-in +
  `sshd -t` + reload-not-restart + keep a fallback session), and **Kubernetes
  auth so an in-cluster worker mints its own per-run token** (retire the static
  Secret token; least-privilege role bound to the pod's SA), the **AppRole
  out-of-cluster twin** (durable never-expiring secret_id → ephemeral token
  per run for a local runner; three-path precedence env→approle→k8s), and
  **diagnosing an expiring token** (look up its real TTL first; never stop
  expiry by pasting a root/never-expiring token into an agent cred file).
- `references/ui-surfaces.md` — building the *production* human UI: HTML
  served in-process by the store's API (one read model, two renderers), the
  honest-state rendering doctrine (grade badges, derived-URL-is-not-a-probe,
  unknown-not-green, empty≠all-green), the projection/walk "surfaces a subset,
  silently drops the rest" pitfall (read-side twin of the write silent-drop),
  and the local smoke-test workflow with its env-var and pkill traps.
