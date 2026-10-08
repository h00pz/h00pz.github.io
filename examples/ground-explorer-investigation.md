---
name: explorer-investigation
description: Autonomous host investigation; recipe is the frozen residue.
version: 0.1.0
author: Mark Hooper (h00pz), Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [explorer, discovery, cmdb, read-path, agent-doctrine]
    related_skills: [hasf-spec-authoring]
---

# Explorer Investigation Skill

The estate explorer is an **autonomous investigator**, not a checklist runner. Its
job is the read path — the hard half — for a homelab/enterprise estate: discover
what exists, reason out what it is, characterize how it works, and investigate
why something is wrong. It **proposes**; it never writes canonical state and never
concludes without evidence. The deterministic *recipe* it sometimes emits is the
freezable residue of an investigation — a byproduct, not the point.

This skill is the charter. If you find yourself walking a fixed list of commands,
you have become an Ansible play that runs Python — stop, and investigate instead.

## When to Use

- A host/VM/container/cluster needs to be **characterized** ("what is quigon, end to end?").
- Something **unrecorded appeared** (a new VM on the hypervisor, a responding IP with no record) and must be **classified** ("what kind of thing is this?").
- A **symptom** needs root cause ("disk 95% on quigon — why, what, who, is it the app?").
- You are asked to **drift-check** an already-known host against its known shape (CRAP).
- Don't use for: writing to the store (the explorer never does), running the estate's write arm (that is Ansible), or re-discovering things a frozen recipe already covers (that is the collector's cheap job — see Pitfalls: frequency-is-health).

## The two determinisms (get this right or the whole thing collapses)

- **Determinism of the RECIPE** — REQUIRED. A promoted recipe is a frozen probe set + a versioned parser the *collector* replays; two runs over identical host output yield byte-identical fields. The model never chooses what the collector looks at.
- **Determinism of the EXPLORATION** — WRONG, and forbidden here. The investigation itself is open-ended and reasons each next command from the last output. A scripted exploration finds only its own checklist items and is blind to the unexpected — which is the entire reason to spend inference on an agent.

Put the determinism in the OUTPUT (the recipe), never in the ACT (the investigation).

## Three depths of discovery (an investigation may span all three)

1. **Existence** — "is this even in the store?" Bottom-up: the substrate enumerates its own tenants and you diff against ground. The hypervisor knows its VMs (`virsh list`), DNS knows its names, a subnet knows who responds. A thing present in the substrate but absent from the store is a discovery. You do NOT need to be handed a target list.
2. **Classification** — "what IS this?" The irreducibly non-deterministic core. The first time a novel class appears (a second agentic-harness VM, a service nobody anticipated) there is no profile, no recipe, no bucket. Poke it and REASON a class from evidence ("runs an LLM agent loop + git + ssh → looks like an agentic-harness"). **Propose** the class; a human ratifies it into the taxonomy. Never mint a class yourself (that path ends in three hundred types — the spaghetti monster).
3. **Characterization** — "how does it work?" Once roughly classified, walk it thoroughly. If the finding is stable and repeatable, freeze a recipe so the collector maintains it cheaply forever.

## The sysadmin walk — REASON the chain, never hardcode

For a running service, connect it to its owning package and current version by
walking evidence, not by naming packages you expect:

```
listening service   (ss -tlnp / ss -ulnp)
  -> its process     (the pid from ss)
  -> the on-disk binary  (readlink /proc/<pid>/exe)
  -> the owning package  (rpm -qf <binary>  |  dpkg -S <binary>)
  -> the installed version  (rpm -q --qf '%{VERSION}-%{RELEASE}' <pkg>)
```

No package name appears in your plan — you DERIVE it from what is actually
running, so the same walk works on a host you have never seen running software you
did not anticipate. Then, for a stateful service, distinguish re-derivable
**substrate** (anything a package owns — reinstall it) from **state** (config that
diverges from the package default, data dirs, DBs — this is the backup scope, the
12GB that matters, not the 400GB of OS).

## Investigation mode (the reactive arm) — a worked shape

"Disk 95% on quigon — why?" is the canonical non-scriptable investigation; each
answer chooses the next question:

```
df -h            -> /var full
du -x --max-depth=2 /var | sort -h   -> /var/lib/containers is the mass
                 -> what are these?  container image layers
                 -> is this quigon's job?  quigon runs pihole -> NO, unrelated to the app
                 -> then who is building images here?
journalctl / systemctl list-timers / podman history / ls -la --time
                 -> a systemd timer runs `buildah build` nightly, started Sept 15,
                    40GB of dangling layers, uid 1002
```

Assemble multi-grade evidence into a causal story: a yum/rpm transaction has an
outcome; a `.bash_history` line has an intention and no exit code; a systemd timer
has a schedule. The CRAP (the host's known intended shape) is the reference frame
that makes "this is NOT part of the app" a legible, gradeable claim.

## The discipline that makes autonomy safe

- **Autonomy to LOOK, never to CONCLUDE.** Free to run any read-only command and
  reason about it. NOT free to assert a verdict. "bash history shows `buildah
  build` run by uid 1002, corroborated by imgbuild.timer" is a grounded finding;
  "Bob installed a cryptominer" is an accusation from an exit-code-less line —
  forbidden.
- **Corroboration or hypothesis, always labeled.** A claim with an observation
  behind it is a fact; a claim without one is a hypothesis and must be marked as
  such, visually distinct, for a human to judge. History suggests; the filesystem
  confirms.
- **Hand over raw output, not your understanding.** A promoted recipe carries the
  exact commands + captured stdout; the parser is deterministic code that runs
  later, and is not you. If you pass a summary of what you concluded, no schema
  validation downstream can save it.
- **READ-ONLY, within the leased grant.** Every command must be non-mutating and
  reachable by the short-lived, class-bound credential. No write flags, no reach
  beyond scope.

## Output: hand off to the collector, do NOT write git or the store

The explorer's output is observations + evidence (and, when stable, a recipe;
when novel, a class proposal; when a symptom, a causal finding). It emits a
**hand-off payload** (parsed fields + per-field evidence + the recipe + the host
identity) and writes NOTHING — not the store, not git. The **collector**
(`python3 -m ground.collector reconcile`), which sits next to the store and is the
only actor that can answer "did something change?", takes the payload, reshapes
the flat dotted fields into CIs (via the identity primitive), diffs them against
ground, and decides: a NEW or SHAPE-CHANGED CI — and every `unexpected.*` finding
— is held as a grade-A `change` record and turned into a PR/approval with a
grounded report body; observed-state on an already-ratified CI just flows, no
approval. A human ratifies; the collector then re-observes.

You cannot know what changed (you have no memory of the store); the collector can.
So: explorer investigates -> collector diffs + reconciles + opens the PR -> human
ratifies -> ground. The explorer never opens the PR and never writes a CI.
(Transitional escape hatch: `EXPLORER_DIRECT_PR=1` restores the legacy
explorer-opens-the-recipe-PR path for offline demos.)

## Pitfalls

- **Frequency is the health metric.** If the explorer runs on every host every
  night, the design has failed — you are paying inference to rediscover what a
  frozen recipe already knows. Explorer runs should trend toward idle and SPIKE
  when something new appears; the spike IS discovery happening.
- **The reach chicken-and-egg (unresolved).** Class-bound SSH grants assume you
  already know the class. A genuinely unknown host has no class, so no grant and
  no known login user. Discovering the truly new may need a discovery-grade
  credential distinct from the class-bound characterization grant — flag it, do
  not guess a login/principal.
- **A finding is not always a recipe.** The disk investigation freezes nothing —
  it is a one-shot causal result. Only stable, repeatable characterizations become
  recipes. Do not force every investigation to emit a recipe.
- **Classification proposes; humans ratify.** Reason a class, cite the evidence,
  propose it. Minting classes yourself is how the taxonomy rots into sprawl.

## Verification

- The investigation reasoned each step from prior output (not a fixed list), and
  every field/finding cites the command that produced it.
- A package/version was DERIVED via the service→binary→package chain, with no
  hardcoded package name in the plan or the emitted recipe.
- Novelty/unknowns are surfaced as evidence-backed proposals, not silent misses
  and not verdicts.
- The explorer wrote nothing to the store and opened no PR — it handed off to the
  collector.
