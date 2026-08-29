# h00pz Architecture Specification Framework v1.2.2

**Status:** Governing framework  
**Purpose:** Define how complex software products—especially AI-backed, stateful, operator-facing systems—are specified before implementation.  
**Intended use:** Future h00pz projects, including but not limited to Atlas, PortfolioOS, and subsequent systems.  
**Core principle:** Define the complete operator decision and operating system first. Decompose the AI application into explicit bounded subsystems before Features, pages, agents, prompts, pipelines, and services accumulate into an accidental architecture. Keep agent operating instructions short, stable, and behavioral; the repository's canonical artifacts—not the instruction prompt or conversation history—carry system truth. Remember missing capabilities deliberately. Weave accepted features into the architecture before coding. Build in narrow slices, track the connected delivery chain rather than isolated component completion, architect prompts and context as executable behavioral systems, run model-controlled agents inside governed OpenShell sandboxes, expose capabilities only through the governed MCP access plane, prove AI and workflow behavior through governed harnesses, preserve a canonical Git-tracked delivery record for every stage, and evolve the architecture explicitly.

**Version:** 1.2.2  
**Document revision:** 6  
**Parent version:** 1.2.2  
**Parent document revision:** 5  
**Release classification:** Compatible document revision  
**v1.2.2 r6 change:** Defines the **build-ready completeness gate** — the condition for baking an ideation item (weaving `captured → woven`). An FML item is build-ready only once it declares its **altitude** (`subsystem`, with all its features enumerated, or `feature`, with the single feature's needs stated) and all **impacts, dependencies, and edges** are mapped. Build-readiness is an **operator-satisfaction gate on completeness**, not a promotion tier: the harness mechanically checks the preconditions (and must refuse to weave — e.g. fail ledger regeneration — when they are unmet), while the operator owns the final judgement by asserting `woven`. Compatible refinement: it does not change FML identity, classification, canonical ownership, or the lifecycle state set — it defines what makes a state transition into the baked (buildable) set legitimate.  
**v1.2.2 r5 change:** Defines the **ideation hold** in the FML lifecycle. Recorded but pre-weave items (lifecycle `captured`, `triage_pending`, `analysis_active`, `dependency_blocked`, `ready_to_weave`) are held in ideation: tracked and edge-linked, but **not** placed in the buildable deployment order. An item enters the build order only once **woven** (or later — `delivery_active`, `accepted`); weaving is the deliberate bake that hands an idea to the order. The living deployment order (§AG.5.10) must surface pre-weave items in a distinct ideation section, separate from "buildable now." This closes the gap where a just-recorded idea could be selected for implementation before it was analyzed and woven. Compatible refinement: it does not change FML identity, classification, canonical ownership, or the lifecycle state set — it defines the buildability semantics of the existing states.  
**v1.2.2 r4 change:** Establishes the FML tiered deployment order as a living generated projection rather than a fixed upfront plan. After every successfully implemented FML item, the project must reconcile the item detail page and newly learned dependency edges, review affected incoming dependents, and regenerate the complete tiered deployment order before selecting the next FML for implementation. The recalculation must incorporate newly discovered implications, prerequisites, dependency changes, shared foundations, sequencing constraints, conflicts, supersessions, accepted limitations, and architecture or runtime discoveries. Tier assignments may move forward, backward, merge, split, or disappear as the architecture learns. The new order, generation time, material movements, and rationale must remain visible; an unchanged order still requires a recorded recalculation. This is a compatible document refinement and does not change FML identity, classification, lifecycle, or canonical-ownership rules.  
**v1.2.2 r3 change:** Establishes the governing separation between **how an implementation agent works** and **what the project currently says is true**. Repository-level agent operating instructions remain short, imperative, stable, and action-oriented; HASF governs method, architecture documents govern target design, ADRs govern accepted decisions, canonical FML detail pages govern capability memory and state, the Chain Delivery Register governs current delivery position, the Current As-Built Architecture governs deployed reality, specifications and plans govern scoped intended work, delivery reports preserve as-built and as-proven history, and Git and pull requests govern change. v1.2.2 r3 adds the Agent Operating Instructions and Repository Truth Contract, the required Current As-Built Architecture standing document, feature-versus-operational execution rules, Spec → Plan → Code discipline, bounded sub-agent delegation, serial operational mutation, same-change documentation requirements, stable repository pointers, stale embedded-truth controls, associated smells and forbidden outcomes, and review and acceptance gates. This is a compatible document refinement: it does not change product semantics, subsystem ownership, runtime, MCP, prompt, harness, FML, or delivery contracts; it clarifies where behavioral rules end and canonical project truth begins.  
**v1.2.2 r2 change:** Adds the mandatory ownership-bearing resource and component naming contract. Product-owned services, runtimes, stores, policies, gateways, namespaces, and observability resources use the product identity rather than a framework, vendor, library, or ambiguous shared name. The `platform-` identity is reserved for capabilities intentionally designed, governed, and operated as shared infrastructure. Implementation substrates such as OpenShell, LangGraph, or a gateway implementation remain deployment metadata rather than the primary architectural identity. Existing cluster resources must be classified as product-owned, shared platform, external, foreign-application, or historical before reuse; foreign or historical resources may not be rebound, renamed, scaled, migrated, or repurposed by convenience. Application-specific operational persistence remains non-canonical and subordinate to application-owned canonical records. These naming and ownership rules are woven through subsystem maps, runtime and deployment views, agent-runtime and MCP boundaries, FML, preflight, smells, delivery records, and acceptance.  
**v1.2.2 change:** Establishes the mandatory h00pz architecture for decomposing an AI application into explicit bounded application subsystems before Feature implementation expands. The release codifies lessons from the emergent Market Intelligence and Hunt architectures: a Feature collection, page family, model, agent, research pipeline, service, or database does not become a coherent subsystem by accumulation. v1.2.2 adds the Subsystem Architecture Map, canonical subsystem detail pages, subsystem identity tests, canonical ownership and shared-subject rules, internal ingress-to-operator architecture, subsystem-scoped AI and context contracts, cross-subsystem request/event/projection/source/candidate contracts, workflow coordination, logical-versus-physical decomposition, subsystem gates, migration guidance, harness requirements, smells, forbidden outcomes, FML placement, delivery traceability, and a new standing AI Application Subsystem Architecture document. This release clarifies and operationalizes the existing System Architecture requirement without changing the canonical semantics of prior applications; existing systems may adopt the contract incrementally through explicit mapping and migration rather than a forced rewrite.

---

## 1. Why This Framework Exists

Most architecture frameworks are good at describing systems after the architecture is largely understood.

They tend to emphasize:

- components;
- containers;
- deployment;
- runtime interactions;
- interfaces;
- technology choices.

Those are necessary, but they are not sufficient for complex products where correctness depends on more than whether services communicate successfully.

In AI-backed and workflow-heavy systems, the hardest failures are often semantic and operational:

- the system answers the wrong question correctly;
- a model-generated interpretation becomes more authoritative than the source;
- current state and historical state are mixed;
- two data stores each appear canonical;
- a retry creates duplicate derived work;
- the UI presents a stale or superseded conclusion;
- an operator cannot tell why a result exists;
- a background workflow terminates without producing an honest product outcome;
- a system silently fabricates confidence, freshness, completeness, or certainty;
- an implementation is locally correct but globally misleading;
- a fixture harness is green while the live model, retrieval, workflow, or operator path remains unproven;
- a model, prompt, policy, or retrieval change silently regresses semantic behavior because no replayable evaluation pack exists;
- prompt behavior depends on hidden composition, undocumented context selection, or production-only strings that cannot be reproduced;
- untrusted source content is allowed to behave like system instruction;
- a prompt is treated as the authorization boundary for tools, writes, or canonical state.
- an agent bypasses the governed connector path and invokes an arbitrary MCP server directly;
- a model-controlled tool loop runs as an ordinary application process with broad filesystem, credential, database, or network authority;
- the OpenShell Gateway and MCP Gateway are conflated into one ambiguous security boundary;
- an ephemeral sandbox session becomes the only durable record that consequential work exists;
- a parent agent silently transfers its full trust domain and capability envelope to a sub-agent;
- a gateway reports a successful tool call while the application mistakes a partial source result for complete canonical truth;
- newly discovered MCP capabilities become usable without application binding review;
- shared connector discovery or caches reveal another trust domain's systems, resources, or tools;
- a central gateway accumulates application business logic and becomes a competing canonical authority;
- related Features, pages, workers, prompts, and agents accumulate into a de facto subsystem with no accepted boundary, owner, or lifecycle;
- two parts of the same AI application independently own the same subject, evidence, workflow state, or current conclusion;
- a dashboard or navigation section becomes the only place where a cross-subsystem result has meaning;
- an application-wide model or agent receives context from every domain and is expected to infer ownership, authority, freshness, and trust boundaries dynamically;
- project architecture, component inventory, FML state, or deployment truth is copied into an agent instruction file and becomes stale or contradictory;
- an implementation agent is expected to carry the whole product architecture in prompt context instead of retrieving canonical repository truth;
- code, runtime state, FML status, and current-architecture documentation diverge because documentation is treated as follow-up work.

The h00pz Architecture Specification Framework exists to prevent those failures.

It is designed for software where:

- operators matter;
- semantics matter;
- state evolves;
- AI participates;
- evidence and provenance matter;
- user interfaces influence understanding;
- workflows span multiple services;
- a correct backend record is not automatically a correct product result.

The governing sequence is:

```text
Operator outcome
    ↓
Canonical semantics
    ↓
Workflow and information flow
    ↓
Operator surfaces
    ↓
System architecture
    ↓
Implementation slices
    ↓
Acceptance
```

Not:

```text
Services
    ↓
Schemas
    ↓
APIs
    ↓
UI later
```

---

# 2. Governing Philosophy

## 2.1 Operator-first

Every substantial feature begins with:

> What must the operator be able to understand, decide, or accomplish?

Architecture exists to serve that outcome.

The first question is not:

> Which database should we use?

It is:

> What exact operator question or workflow is this system responsible for?

## 2.2 Semantics before machinery

A deterministic implementation of an ambiguous concept is still wrong.

Before defining services, schemas, jobs, queues, or prompts, define:

- what the result means;
- which question it answers;
- which facts support it;
- which facts do not;
- how uncertainty is represented;
- which state is current;
- which state is historical;
- what is allowed to happen next.

## 2.3 One canonical truth per concern

Every mutable concern must have one declared canonical owner.

Examples:

- one canonical current revision;
- one canonical write store;
- one canonical identity record;
- one canonical lifecycle state;
- one canonical task;
- one canonical source artifact.

Other stores may exist as:

- projections;
- indexes;
- caches;
- read models;
- derived summaries;
- historical records.

But they must not silently become competing truth.

## 2.4 Preserve source, regenerate interpretation

Where practical:

```text
Source
  preserved

Derived interpretation
  regenerable

Operator correction
  durable and independent
```

This prevents future model changes, extraction improvements, or schema migrations from destroying the original evidence.

## 2.5 Honest incompleteness beats fabricated completeness

The framework prefers:

- unknown;
- incomplete;
- unavailable;
- stale;
- unresolved;
- exhausted;
- unsupported;

over:

- guessed values;
- silent defaults;
- false certainty;
- invented relationships;
- synthetic completeness;
- misleading success states.

## 2.6 KISS is a governing constraint

The framework is comprehensive in design, not maximalist in implementation.

Prefer:

- one state machine;
- one canonical read model;
- one authority ladder;
- one bounded retry;
- one clear terminal rule;
- one correction layer;
- one projection model;
- one honest unavailable state.

Avoid:

- duplicate concepts;
- generalized platforms before need;
- arbitrary configurability;
- model voting without proven value;
- invisible fallback behavior;
- architecture that exists only to compensate for unclear semantics.

## 2.7 How to work versus what is true

The framework separates behavioral instruction from project truth.

```text
Agent operating instructions
→ govern how work is performed

Canonical repository artifacts
→ govern what the project says is true
```

An implementation agent should not need a forty-page behavioral prompt containing copied project history, current component inventory, FML state, architecture decisions, and deployment facts.

The operating rules should remain small and enforceable. The repository should carry the complexity through canonical, versioned, linked artifacts.

Required principle:

> **Rules govern behavior. Repository artifacts govern truth.**

When a rule file and a canonical repository artifact disagree about project truth, the canonical owner for that concern wins and the stale rule-file assertion must be corrected in the same change.

---

# 3. Applicability

Use this framework for any substantial feature or system involving one or more of the following:

- AI or model-generated output;
- background workflows;
- operator decisions;
- stateful lifecycles;
- versioned knowledge;
- evidence or provenance;
- external connectors;
- multi-step automation;
- current-versus-history behavior;
- multiple stores or projections;
- task or commitment management;
- identity resolution;
- operator-facing surfaces;
- safety or trust implications;
- workflows that may continue, stop, fail, or exhaust;
- model-controlled tool selection, code execution, filesystem access, network access, or side effects;
- autonomous or semi-autonomous agents, sub-agents, or long-running agent attempts;
- multiple application subsystems, bounded contexts, or domain-owned workflows;
- Features that share canonical subjects, source material, models, operator surfaces, or cross-subsystem handoffs.

For small, isolated features, use a reduced form, but preserve the same governing order:

```text
Outcome
→ Semantics
→ Flow
→ Surface
→ Acceptance
```

---

# 4. Required Architecture Layers

Every substantial specification must define the following layers.

## 4.1 Intent layer

Defines:

- problem;
- operator outcome;
- decision or operating question;
- actor;
- as-of context;
- scope;
- non-goals;
- category errors to prevent.

## 4.2 AI application subsystem layer

Defines:

- the Subsystem Architecture Map;
- application subsystem identities and boundaries;
- subsystem operator outcomes;
- owned Features and FML items;
- canonical concepts and writes owned by each subsystem;
- shared-subject and identity ownership;
- internal ingress-to-operator architecture;
- subsystem-scoped AI roles, prompts, context, agents, and harnesses;
- cross-subsystem contracts and workflow coordinators;
- logical versus physical decomposition;
- ownership-bearing subsystem, namespace, resource, runtime, store, gateway, policy, and observability names;
- implementation-substrate metadata and excluded foreign or historical resources;
- subsystem failure, degradation, migration, and acceptance.

## 4.3 Canonical semantics layer

Defines:

- canonical objects;
- authoritative fields;
- lifecycle meanings;
- current truth;
- history;
- revision semantics;
- identity semantics;
- relationships;
- operator corrections;
- uncertainty;
- derived versus canonical state.

## 4.4 Workflow layer

Defines:

- states;
- transitions;
- triggers;
- owners;
- retry;
- restart;
- continuation;
- exhaustion;
- stale work;
- terminal outcomes;
- next-stage routing.

## 4.5 Information layer

Defines:

- records;
- stores;
- write ownership;
- source-of-truth rules;
- projections;
- indexes;
- caches;
- event flow;
- read models;
- backup and rebuild behavior.

## 4.6 Operator experience layer

Defines:

- operator questions;
- surfaces;
- entry points;
- actions;
- write effects;
- empty/loading/error/stale states;
- current versus history;
- mobile behavior;
- live acceptance.

## 4.7 Intelligence layer

Defines:

- model roles and compatibility;
- prompt packages, canonical prompt identity, and lifecycle;
- instruction hierarchy and prompt composition;
- context assembly, trust-domain boundaries, token allocation, truncation, and omission reporting;
- retrieval;
- structured output;
- repair and bounded retry;
- tool use and deterministic authority boundaries;
- external reasoning;
- evidence assembly;
- freshness requirements;
- prompt, model, policy, and context provenance;
- rollout, rollback, replay, and semantic calibration;
- model and prompt limitations.

## 4.8 Harness and evaluation layer

Defines:

- harness purpose and authority;
- production-path fidelity;
- fixture, recorded-replay, live-isolated, and production-smoke modes;
- case packs and stable fixture identity;
- deterministic invariants and semantic evaluation rubrics;
- model, prompt, policy, retrieval, schema, and configuration replay;
- workflow, handoff, failure, recovery, migration, and operator-acceptance harnesses;
- run manifests and evidence packages;
- environment isolation, cleanup, and production safety;
- regression baselines, budgets, and promotion rules;
- harness documentation, ownership, and lifecycle.

## 4.9 Agent runtime and sandbox layer

Defines:

- whether the AI behavior is bounded non-agentic inference or model-controlled agentic execution;
- application control-plane ownership;
- agent-harness ownership and lifecycle;
- `AgentRun`, `AgentAttempt`, and execution-profile semantics;
- OpenShell Gateway and Supervisor responsibilities;
- sandbox creation, policy revision, checkpointing, cancellation, teardown, and cleanup;
- process, filesystem, network, credential, and inference boundaries;
- trust-domain identity and sub-agent attenuation;
- MCP capability access from inside the sandbox;
- prohibition of direct database, arbitrary internet, Kubernetes API, and direct MCP-server access;
- result envelopes, application validation, promotion, and canonical-write boundaries;
- execution manifests, audit correlation, operator surfaces, replay, and live acceptance.

## 4.10 Platform layer

Defines:

- components;
- services;
- deployment;
- namespaces;
- runtime topology;
- resource ownership classification and ownership-bearing names;
- product-owned versus intentionally shared platform identities;
- implementation technology recorded as metadata rather than primary service identity;
- runtime configuration ownership and injection;
- Kubernetes environment variables, Secrets, and ConfigMaps;
- configuration validation and rollout behavior;
- build graph and parallelism;
- dependency and container-layer reuse;
- build, test, image, push, rollout, and readiness budgets;
- immutable artifact and deployed-digest verification;
- security;
- observability;
- performance;
- infrastructure dependencies.

## 4.11 Governance layer

Defines:

- authority ladder;
- invariants;
- forbidden outcomes;
- replay;
- acceptance;
- stop rule;
- migration;
- deprecation;
- unresolved risks.

---

# 5. The Required Specification Structure

Every substantial specification should use the following sections.

## A. Executive Summary

State:

- what is being built;
- why it exists;
- who uses it;
- what outcome it enables;
- what is explicitly not included;
- why this architecture is the smallest safe design.

## B. Operator Outcome and Governing Question

Define the exact operator outcome.

For decision features:

- What exact question is answered?
- Who owns the decision?
- As of what time?
- For which subject?
- Under which assumptions?
- Which dispositions are allowed?
- Which adjacent questions are excluded?

For operating features:

- What is the operator trying to accomplish?
- What information must be visible?
- What actions must be possible?
- What must happen automatically?
- What must remain under operator control?

Required operator questions include:

- What happened?
- What does it mean?
- What supports it?
- What contradicts it?
- Is it current?
- Is it complete?
- What remains unresolved?
- What can I do next?
- Why did the process stop?
- What would change the outcome?

## C. Category Errors and Misinterpretations to Prevent

Every specification must identify the strongest plausible category errors.

Examples:

```text
Observed mention
≠ confirmed identity

Model suggestion
≠ canonical task

Workspace
≠ knowledge owner

Projection
≠ source of truth

Historical state
≠ current state

Source absence
≠ negative evidence

Conversation summary
≠ original conversation

External claim
≠ verified fact

Current employer
≠ only employer ever held

Operator correction
≠ source rewrite

Successful worker
≠ successful product outcome
```

These errors must become deterministic tests or operator-surface guards.

## D. Definition of Complete

Define separately:

### Workflow termination

Examples:

- job finished;
- queue empty;
- retry cap reached;
- model returned;
- worker stopped;
- connector failed;
- operator canceled.

### Product completion

Examples:

- required information exists or is honestly unavailable;
- canonical state is coherent;
- current state is visible;
- history is preserved;
- operator can understand the result;
- downstream routing is complete;
- no unresolved contradiction remains hidden.

A workflow may terminate while the product outcome remains incomplete.

The specification must say which is which.

## E. Conceptual Model

Define the smallest set of durable concepts.

For each concept:

- purpose;
- identity;
- owner;
- lifecycle;
- relationships;
- canonical fields;
- derived fields;
- operator-owned fields;
- historical behavior.

Do not create separate object types merely because the UI uses different words.

Use the test:

> Does this concept have a distinct identity and lifecycle, or is it a view, classification, or projection?

Examples:

- Workspace may be a view.
- Current summary may be a projection.
- A person mention may not be a canonical person.
- A task candidate may not be a canonical task.
- A project and initiative may be one concept.

## F. Canonical Ownership and Authority Ladder

Define who wins when information conflicts.

A common authority order:

1. Preserved source evidence and operator-owned source content.
2. Explicit operator assertions or corrections.
3. Canonical deterministic records and lifecycle rules.
4. Current ready derived revision.
5. Projections and indexes.
6. Model-generated summaries.
7. UI display text.

This order may vary by domain, but it must be explicit.

Also define field-level ownership.

## G. Current Truth and History

Every versioned feature must define:

- one current revision pointer;
- one canonical current read model;
- one history model;
- one rule preventing old data from filling current gaps.

Required rule:

```text
Current field missing
→ display unavailable

Never:
search historical revisions for replacement current text
```

Use distinct naming:

- `contentRevision`
- `derivedRevisionId`
- `projectionRevision`
- `schemaVersion`

Do not overload `revision`.

## H. State Machines

Define all independent state axes.

Typical axes:

### Workflow state

```text
pending
queued
processing
waiting
ready
failed
canceled
exhausted
superseded
```

### Evidence state

```text
supported
weakened
conflicted
incomplete
unsupported
unavailable
```

### Routing state

```text
continue
stop
promote
publish
retry
review
no_action
```

### Projection state

```text
current
lagging
failed
rebuilding
unavailable
```

Do not overload one field with multiple meanings.

For every transition define:

- current state;
- trigger;
- owner;
- predicate;
- records read;
- records written;
- idempotency key;
- next state;
- terminal behavior;
- operator-visible result.

## I. Canonical Record Model

For every canonical record define:

- unique identity;
- required fields;
- mutable fields;
- operator-owned fields;
- model-derived fields;
- source references;
- revision behavior;
- deletion semantics;
- relationship behavior;
- indexes;
- read model.

Also state what is not canonical.

## J. Projection and Consistency Model

If multiple stores are used, define:

- canonical write store;
- transaction boundary;
- outbox/event contract;
- ordering;
- idempotency;
- retry;
- lag;
- rebuild;
- restore;
- revision alignment.

Required principle:

> Cross-store consistency is achieved through one canonical store and rebuildable projections, not independent canonical writes.

## K. Operator Correction Model

If derived intelligence can be regenerated, operator corrections require an independent durable layer.

Define:

- correction record;
- target;
- action;
- precedence;
- supersession;
- withdrawal;
- reprocessing behavior;
- history;
- operator surface.

Direct edits to operator-owned content should remain normal revisions.

## L. Identity Resolution

For systems involving people, organizations, products, or other identity-bearing entities, define:

- mention versus canonical entity;
- strong identifiers;
- weak identifiers;
- automatic resolution;
- probable matches;
- ambiguous cases;
- merge;
- split;
- aliases;
- temporal identity;
- operator confirmation;
- undo.

Safety principle:

> Auto-resolve mentions when strong evidence exists. Never auto-merge canonical entities unless the domain explicitly proves that is safe.

## M. Task and Commitment Semantics

If tasks exist, define:

- candidate versus canonical task;
- promotion;
- owner;
- status;
- priority;
- due date;
- person links;
- organization links;
- initiative links;
- source provenance;
- completion;
- cancellation;
- waiting-on state;
- recurrence;
- history.

Suggested task lifecycle:

```text
Observation
    ↓
TaskCandidate
    ↓
Operator promotion
    ↓
Canonical Task
```

Every task should answer:

> Why does this exist?

through source relationships.

## N. Workflow Continuation and Exhaustion

If the system may continue work:

Define:

- unresolved gap;
- why it matters;
- exact next work;
- acceptance condition;
- bounded retry;
- cycle cap;
- honest terminal state.

Required rule:

```text
Gap remains
+ no credible path or budget exhausted
→ honest terminal outcome
```

## O. Model, Prompt, and AI Contract

For every AI task define:

- owning application subsystem and bounded model role;
- model and supported model family;
- role;
- operating mode;
- execution classification: bounded non-agentic inference or model-controlled agentic execution;
- agent execution profile, sandbox mode, and application control-plane owner where applicable;
- canonical prompt package ID, version, and content hash;
- prompt composition layers and precedence;
- context-assembly policy, source precedence, trust domains, token budgets, truncation, and omission behavior;
- input schema;
- output schema;
- exhaustive requirements;
- evidence and citation requirements;
- repair and bounded retry;
- allowed reasoning;
- prohibited reasoning;
- numeric restrictions;
- tool contract and deterministic permission boundary;
- provenance;
- applicable harness classes and case packs;
- deterministic versus semantic evaluation gates;
- replay triggers;
- rollout and rollback behavior;
- `AgentRun`, `AgentAttempt`, sandbox-policy, capability-grant, checkpoint, and teardown behavior where applicable;
- latency and context-budget expectations.

A prompt may guide model behavior. It may not become the sole authority for canonical writes, destructive actions, security boundaries, lifecycle transitions, or external egress.

## P. Retrieval and Freshness Contract

Define intent classes.

### Live-required

Must query a live source.

### Memory-preferred

Uses canonical internal memory first.

### Hybrid

Requires both memory and live sources.

The model may upgrade retrieval depth.

The model may not downgrade a live-required intent to memory-only.

## Q. External Provider and Data Egress Contract

If external AI or services are optional:

Define:

- operator choice;
- default mode;
- per-thread or per-request scope;
- egress package;
- consent;
- history inheritance;
- logging;
- redaction;
- secrets;
- provider boundary.

Required rule:

> Sovereign context must never be transmitted externally by implication.

## R. Operator Information Architecture

Define:

- primary surfaces;
- global navigation;
- search;
- command palette;
- workspaces;
- context panels;
- responsive behavior;
- mobile behavior;
- direct editing;
- history access;
- settings boundary.

Use the principle:

> Context over navigation.

## S. Operator Surface Definition

Every substantial surface must define:

- purpose;
- operator question;
- entry point;
- canonical read model;
- required fields;
- actions;
- write effects;
- state-specific behavior;
- empty state;
- loading state;
- error state;
- stale state;
- current-versus-history behavior;
- evidence drilldown;
- navigation;
- mobile behavior;
- forbidden UI states;
- live acceptance criteria.

This is mandatory.

## T. Interaction and Editing Contract

Define:

- direct-edit behavior;
- auto-save;
- explicit save, if any;
- optimistic concurrency;
- conflict resolution;
- session identity;
- revision history;
- disconnected state;
- offline support or non-support.

Never imply a save succeeded until the canonical write commits.

## U. Security and Privacy

Define:

- authentication;
- authorization;
- session lifetime;
- device revocation;
- secrets;
- connector tokens;
- encryption;
- audit;
- reauthentication;
- external egress;
- deletion;
- export;
- least privilege;
- sandbox execution policy;
- process and binary identity;
- filesystem read/write boundaries;
- direct-network and direct-service denial;
- agent and sub-agent trust-domain identity;
- credential mediation and secret non-disclosure;
- separation of OpenShell runtime authorization from MCP capability authorization.

Single-user does not mean security-free.

## V. Runtime and Deployment Views

Borrow from arc42 and C4 here.

Provide:

- system context;
- container view;
- component view;
- runtime view;
- deployment view;
- resource inventory with ownership classification;
- canonical product, subsystem, namespace, service, runtime, gateway, policy, store, and observability names;
- implementation-substrate labels, image provenance, and deployment metadata;
- explicit foreign-application and historical-resource exclusions;
- application control plane, OpenShell runtime plane, MCP capability access plane, model-serving plane, and domain-service boundaries;
- namespace or tenancy boundaries;
- required environment variables and their owners;
- Secret and ConfigMap references;
- mounted prompt, policy, and configuration assets;
- agent execution profiles and sandbox-policy revisions;
- OpenShell Gateway and sandbox deployment topology;
- configuration-change rollout behavior.

Required one-way rule where applicable:

```text
Application
→ shared platform

Shared platform
↛ application
```

Share capabilities, never application knowledge.

Resource names must follow **AI.3 Resource, Component, Namespace, and Runtime Naming**.

## W. Architecture Decision Records

Every major, difficult-to-reverse decision should have an ADR.

ADR structure:

```text
Title
Status
Context
Decision
Consequences
Alternatives considered
Why rejected
Revisit trigger
```

## X. C4 and Diagram Requirements

Recommended diagrams:

1. System context.
2. Container architecture.
3. Canonical data and projection flow.
4. Major runtime sequence.
5. State machine.
6. Operator flow.
7. Identity/relationship model.
8. Deployment and namespace boundaries.
9. Agent execution sequence and the separation between application control, OpenShell runtime, MCP access, model serving, and domain services.

Diagrams must agree with text.

## Y. Evidence and Provenance

For any load-bearing claim, relationship, task candidate, or identity observation, define:

- source artifact;
- source type;
- source identifier;
- source span;
- observed time;
- extraction revision;
- model identity;
- operator correction;
- confidence;
- current resolution state.

Confidence does not replace provenance.

## Z. Idempotency, Retry, and Stale Work

Every asynchronous write must define:

- idempotency key;
- retry;
- duplicate prevention;
- late result behavior;
- stale revision behavior;
- terminal-state protection;
- restart;
- cancellation;
- reconciliation;
- logical `AgentRun` identity versus physical `AgentAttempt` identity where applicable;
- sandbox loss, retry, cancellation, and late-attempt behavior.

Required default:

```text
Late old work
→ preserved diagnostically
→ cannot replace newer canonical truth
```

## AA. Replay and Observability

For model or workflow features define replay seams.

Capture:

- request hash;
- model identity;
- prompt version;
- schema version;
- policy version;
- source references;
- retrieval package;
- connector results;
- agent run, attempt, execution profile, sandbox ID, sandbox-policy revision, and capability-grant set where applicable;
- operator inputs;
- canonical output.

Observability should include:

- end-to-end latency;
- queue time;
- phase timing;
- model calls;
- tokens;
- retries;
- cache;
- projection lag;
- connector latency;
- sandbox provisioning, policy, startup, checkpoint, teardown, and cleanup latency;
- cold versus warm behavior;
- failure classification.

Instrument before optimizing.

## AB. Forbidden Outcomes

Every specification must contain a `Forbidden Outcomes` section.

Examples:

```text
Projection stale
+ displayed as current

Operator correction exists
+ reprocessing removes it

Same retry
+ duplicate canonical task

Name match only
+ automatic destructive merge

Current surface
+ superseded revision content

Disconnected edit
+ UI claims saved

External provider selected
+ sovereign history silently transmitted

Live-required question
+ memory-only answer

Failed derived revision
+ replaces current ready revision

Missing source
+ model fabricates a fact

Runtime endpoint, database name, feature flag, retry budget, model identity, or prompt
+ hard-coded into production application logic

Secret value
+ stored as a plain Deployment value or ConfigMap entry

ConfigMap or Secret changes
+ running workload continues with an unidentified old configuration

Model-controlled tool loop
+ executes outside a governed sandbox without an approved exception

OpenShell Gateway authorization
+ represented as MCP tool authorization

MCP Gateway authorization
+ represented as permission to change canonical application truth

Sandbox session disappears
+ durable work identity, state, or recovery path disappears

Sandbox has direct database, Kubernetes API, arbitrary internet, or direct MCP-server access
+ ordinary production operation continues
```

Each forbidden outcome should have a deterministic fixture.

## AC. Acceptance Plan

Report separately:

- deterministic contract acceptance;
- component acceptance;
- lifecycle acceptance;
- semantic calibration acceptance;
- retrieval and evidence acceptance;
- fixture-chain acceptance;
- live-chain acceptance;
- operator acceptance;
- recovery acceptance;
- performance and capacity acceptance;
- security acceptance;
- agent-runtime and sandbox-policy acceptance;
- trust-domain and sub-agent attenuation acceptance.

Name the harness cases, execution modes, gates, and evidence packages that prove each acceptance class.

At least one realistic end-to-end subject or workflow must traverse the production path.

## AD. Capability and Data Preflight

Before implementation, identify each load-bearing capability.

For each:

- canonical resource or capability name;
- ownership classification: product-owned, application-foundation, shared-platform, external dependency, foreign-application, or historical artifact;
- current physical location and namespace;
- whether reuse is allowed, prohibited, or requires explicit transfer or migration;
- implementation substrate and image provenance;
- required fact or capability;
- current source;
- availability;
- freshness;
- precision;
- provenance;
- fallback;
- failure behavior;
- operator visibility.

Do not design around assumed capabilities.

An existing Deployment, Service, StatefulSet, database, queue, gateway, store, namespace, or image is not available to a new application merely because it is present in the cluster. Ownership and architectural fitness must be proven before binding or reuse.

## AE. Non-Goals

Explicitly define what will not be built.

Non-goals prevent architecture drift.

## AF. Stop Rule

Define the exact condition that ends the slice.

The stop rule must not require a positive or exciting outcome.

Before invoking the stop rule:

- run the required Feature Recall pass;
- classify newly remembered capabilities in the Feature Memory Ledger;
- weave every `required_now` capability through the affected architecture layers;
- confirm that deferred capabilities do not require preservation of additional source, identity, provenance, or migration data now;
- record the architecture version impact of the completed slice;
- review the Architecture Smells Seed and disposition any smells introduced or exposed by the slice;
- confirm that production endpoints, credentials, prompts, policies, and tunable runtime parameters are externalized through the declared Kubernetes configuration contract;
- verify that the active configuration revision is observable and that configuration changes follow the declared rollout or reload path;
- confirm that the slice remains within its build and delivery budget or records a named regression with evidence, owner, and removal trigger;
- verify that the intended immutable image digest is active before declaring live acceptance;
- verify that deployed resource names identify the true product or accepted shared-platform owner, implementation substrates remain metadata, and no foreign-application or historical resources were adopted by convenience;
- when the slice successfully implements an FML item, reconcile its canonical detail page and dependency edges, review affected dependents, and regenerate the complete FML tiered deployment order before selecting or beginning the next FML implementation;
- for agentic work, verify that a realistic `AgentAttempt` traversed the declared OpenShell sandbox path with the exact execution profile, sandbox-policy revision, MCP grant set, model route, teardown result, and durable application provenance.

Once the declared outcome works honestly, the recall gate is satisfied, and no applicable smell lacks a disposition:

> stop building.

## AG. Feature Recall and Architecture Weaving

### AG.1 Governing Principle

No project remembers every required capability during its first architecture pass.

The framework must therefore treat feature discovery as a recurring governed activity rather than assuming that the initial feature list is complete.

The purpose of Feature Recall is to uncover:

- missing operator workflows;
- forgotten lifecycle stages;
- absent administrative capabilities;
- missing failure and recovery behavior;
- import, export, migration, retention, and deletion requirements;
- downstream consequences;
- capabilities implied by existing features;
- features that belong in a later release;
- architectural decisions that would make a foreseeable later capability unnecessarily difficult.

The objective is not to include every imaginable feature in the current release.

The objective is to ensure that:

1. important capabilities are remembered;
2. accepted capabilities are woven into the architecture before coding;
3. deferred capabilities are recorded deliberately;
4. the current architecture does not accidentally prohibit a foreseeable future requirement;
5. scope decisions remain visible and reversible.

Feature Recall is a memory and omission control, not authorization for uncontrolled scope expansion.

### AG.2 Required Recall Gates

A Feature Recall pass must occur:

1. before accepting the project foundation documents;
2. before accepting each substantial feature specification;
3. before declaring architecture `1.0`;
4. before every minor or major architecture release;
5. after the first realistic end-to-end acceptance workflow;
6. after meaningful operator use reveals an unmodeled workflow;
7. before invoking the stop rule for a substantial implementation slice.

Feature Recall is not a brainstorming session without consequences.

Every discovered capability must be classified and recorded.

### AG.3 Feature Recall Questions

The following questions are mandatory prompts. Not every question will produce a feature, but each relevant category must be considered explicitly.

#### Operator and actor questions

- Who else may need to use, inspect, administer, approve, correct, or consume this capability?
- Is there a difference between the person who initiates the work and the person who owns the outcome?
- What does the operator need before beginning the workflow?
- What does the operator need immediately after completing it?
- What obvious next action will the operator expect?
- What work currently happens outside the product because the product has no surface for it?
- What would force the operator to leave the system and use another tool?
- What information will a new operator need that the original designer already knows implicitly?

#### Lifecycle questions

- What happens before the primary workflow begins?
- What happens after its apparent completion?
- Can the result be reopened, revised, superseded, canceled, archived, restored, or deleted?
- Is there a draft state?
- Is there an approval or review state?
- Can work wait on another person, system, event, or date?
- Can the same subject pass through the workflow more than once?
- What is current, and what must remain historical?
- What happens when the subject changes after the workflow completes?
- What future event could invalidate the current result?

#### Adjacent-feature questions

For every action or surface, ask:

- What comes immediately before this?
- What comes immediately after this?
- What does this create?
- What consumes its output?
- What happens if no output is produced?
- What happens if the output is wrong?
- How is it corrected?
- How is the correction preserved?
- Can it be undone?
- Can it be repeated?
- Can it be compared with a prior result?
- Can it be searched, filtered, sorted, linked, exported, or shared?
- Does it create a notification, task, commitment, or follow-up?
- Does another workflow need to know that this happened?

#### State and exception questions

- What are the non-happy-path states?
- What happens if the operator abandons the workflow?
- What happens if a worker stops halfway through?
- What happens if an external source disappears?
- What happens if a model returns an invalid or incomplete result?
- What happens if a result arrives after newer work has completed?
- What happens when two actions occur concurrently?
- What happens when a retry succeeds twice?
- What happens when a projection is stale?
- What happens when the canonical write succeeds but a downstream update fails?
- What must the operator be able to repair manually?
- What must never require manual repair?

#### Data and knowledge questions

- How does information enter the system?
- Must the system support manual entry, paste, upload, URL ingestion, API ingestion, synchronization, or bulk import?
- Must existing data be migrated?
- Must data be exported in a portable form?
- What source evidence must be preserved?
- What derived information must be regenerable?
- What information belongs to the operator rather than the model?
- What information may be corrected?
- What information may be deleted?
- What relationships are implied but not yet represented?
- Does this capability introduce a new canonical object or only a new view?
- What happens when two sources disagree?
- What happens when the same entity appears under multiple names?
- What information will be needed later that is cheap to preserve now but expensive to reconstruct later?

#### Operator surface questions

- Where does the operator discover this capability?
- Where does unfinished work appear?
- Where do failures appear?
- Where do stale results appear?
- Where does history appear?
- Where are corrections made?
- Where can the operator see why a result exists?
- Is an administrative or settings surface required?
- Is a queue, inbox, dashboard, detail page, drawer, report, or notification required?
- What empty state teaches the operator what to do?
- What surface is needed for bulk or repeated work?
- What mobile or reduced-width behavior matters?
- What information must remain visible across multiple stages?

#### Integration and platform questions

- Which external systems will eventually need to provide or consume this information?
- Does the feature require notifications, scheduling, webhooks, connectors, or background work?
- What happens when an integration is unavailable?
- Is an integration optional, required, replaceable, or operator-selected?
- Which platform capabilities should be shared?
- Which application knowledge must not leak into the shared platform?
- Which existing resources are owned by this product, another application, the shared platform, an external provider, or no current architecture?
- Are any historical experiments or foreign-application services being treated as candidates merely because they already exist?
- Does every material resource name identify its actual owner and capability?
- Is any implementation framework or database name masquerading as the product capability?
- Will this feature require import, synchronization, reconciliation, or conflict resolution?
- Will another project need the same capability with different semantics?
- Which endpoints, identities, limits, prompts, policies, credentials, or paths vary by environment and therefore require Kubernetes-owned configuration?
- Would moving to another namespace, cluster, database, or model endpoint require application-code changes?
- Is this genuinely reusable infrastructure or only apparently similar application logic?
- Which plane owns this behavior: application control, OpenShell runtime, MCP capability access, model serving, or domain execution?
- Does gateway sharing preserve trust-domain, credential, policy, model-route, and failure isolation, or is a separate OpenShell or MCP gateway instance required?

#### Security and governance questions

- Who is authorized to see, change, approve, export, or delete the information?
- Does the action require reauthentication?
- Does it transmit sovereign or sensitive context externally?
- Is consent required?
- What must be audited?
- What correction or override authority does the operator have?
- What action would be destructive or difficult to reverse?
- What retention rule applies?
- What information must survive deletion of derived state?

#### Scale and operations questions

- What changes when there are ten records, ten thousand records, or ten million records?
- What happens when a workflow takes seconds, hours, or days?
- What happens when a connector or model is rate-limited?
- What must be observable?
- What must be replayable?
- What must be rebuildable?
- What operational capability is needed for backup, restore, migration, or reconciliation?
- How long does a narrow change take to build, test, package, deploy, and prove live?
- Which build stages can run independently, and is available compute being used?
- Which dependency, build, and image layers can be reused safely from complete input identity?
- What changes require a full clean build, and what changes should avoid an application rebuild entirely?
- How is the intended image digest verified on the active workload?
- What maintenance work will an operator or administrator eventually need to perform?
- What happens after a schema, prompt, model, or policy changes?

#### AI and intelligence questions

- Is the model answering the correct question or only an adjacent question?
- What important information is absent from the model context?
- What must be exhaustive rather than representative?
- What must the model never infer?
- What requires live retrieval?
- What requires internal canonical memory?
- What happens when evidence is insufficient?
- How can the result be challenged or regenerated?
- What happens when the model changes?
- Does the operator need to compare model revisions?
- What part of the output may become canonical, and through which deterministic gate?
- Is this bounded inference or model-controlled agentic execution?
- If agentic, which application-owned harness runs inside which OpenShell execution profile?
- What direct filesystem, network, database, Kubernetes, MCP-server, or credential access must be impossible?
- What durable `AgentRun` and `AgentAttempt` state survives sandbox loss?
- What follow-up research or work should be created when the model cannot complete the assignment?

#### Subsystem-boundary questions

- Which application subsystem owns this capability and its operator outcome?
- Does the capability fit an accepted subsystem boundary, or does it reveal a missing subsystem?
- Which canonical concepts and writes belong to the owning subsystem?
- Which subjects, records, or projections are owned elsewhere?
- Does this capability duplicate an ingress, research, evidence, identity, lifecycle, or surface already owned by another subsystem?
- Which cross-subsystem request, event, read-model, source, or candidate contracts are required?
- Who coordinates the complete workflow when more than one subsystem participates?
- Could the Feature be implemented only by directly reading or writing another subsystem's store?
- Does a shared model, agent, or context assembler risk becoming an application-wide semantic owner?
- Is a proposed shared platform component actually carrying application-specific subsystem meaning?
- Does the subsystem have a coherent operator surface family, or are pages defining the architecture independently?
- Which subsystem harness and case pack will prove the complete ingress-to-operator outcome?
- Is the proposed physical service boundary justified, or would a logical module be simpler and safer?
- What migration is required if the capability currently exists as an emergent feature pile?

#### Product-boundary questions

- Is this a feature of the current product or a different product?
- Is it an extension of the current operator outcome or a different operator outcome?
- Does it require a new canonical concept, authority model, or trust boundary?
- Does it belong in the current architecture release, a later compatible release, a major release, or a separate architectural fork?
- Would including it now complicate the current outcome without preserving meaningful future optionality?
- Would excluding it now make the future feature prohibitively expensive or force canonical data loss?

### AG.4 Counterfactual Walkthroughs

At least five counterfactual walkthroughs must be performed before architecture acceptance:

1. The operator completes the happy path.
2. The operator changes their mind.
3. The system produces the wrong result.
4. A dependency fails halfway through.
5. The operator returns six months later after the system and source data have changed.

Additional walkthroughs should cover, where relevant:

- import of existing data;
- bulk operation;
- duplicate input;
- concurrent work;
- stale work;
- migration from a prior architecture;
- external-provider failure;
- deletion and restoration;
- a new operator with no conversational history.

### AG.5 Feature Memory Ledger

Every project must maintain a Feature Memory Ledger as a durable architecture artifact.

The Feature Memory Ledger is a two-level system:

```text
Feature Memory Ledger index
    ↓
Canonical FML item detail page
    ↓
Typed dependency relationships, decisions, weaving, delivery, and acceptance evidence
```

The index exists for scanning, prioritization, and project-wide status.

The detail page exists to preserve the complete architectural memory of one capability.

A single ledger row is not sufficient once an item has been remembered. Every FML item must have its own canonical detail page, including items that are deferred, rejected, duplicated, superseded, or unresolved.

The ledger is not a product backlog. It records architectural memory, classification, impact, relationships, and revisit conditions. Delivery planning may reference it but must not replace it.

#### AG.5.1 Canonical Ownership

Each FML item has one canonical record.

For the default Git-governed architecture model:

- the FML item detail page is the canonical item record;
- the FML index is a current projection of those detail pages;
- dependency lists and graph views are projections of canonical typed dependency edges;
- Epic, Feature, Chain Delivery, specification, and delivery-report records link to the FML item but do not redefine it.

Required rule:

```text
FML index summary conflicts with item detail page
→ item detail page wins
→ index must be reconciled
```

A project using an application database as the canonical FML store must explicitly declare that owner and treat Git documents as versioned exports or release snapshots. It must not maintain two independently editable canonical FML stores.

#### AG.5.2 FML Index

The FML index must contain one row or compact record per FML item with at least:

```text
Canonical FML ID
Descriptive capability name
Classification
Lifecycle status
Dependency health
Current generated deployment tier
Current generated order position
Tiered-order generation time
Target architecture release
Target product release, if known
Owner
Last reviewed time
Canonical detail-page link
```

Allowed dependency-health values are:

```text
clear
soft_dependency_open
hard_dependency_blocked
decision_blocked
conflict_open
cycle_detected
unknown
```

The index must support answering:

- What capabilities have we remembered?
- Which items require action now?
- Which items are blocked, and by what?
- Which deferred items have reached their revisit trigger?
- Which items share a foundation and should be designed together?
- Which items conflict with another architectural direction?
- Which items have been promoted into a Feature or implementation Slice?
- Which items are delivered but not yet accepted?
- What is the current generated tiered deployment order?
- Which FML item is next under the latest reconciled architecture and dependency graph?

The index must not compress all dependency information into an unstructured text cell.

#### AG.5.3 FML Item Naming

Every FML item must use an outcome-bearing descriptive name and canonical ID.

Recommended ID form:

```text
fml-<descriptive-capability-slug>
```

Examples:

```text
fml-governed-logseq-project-import
fml-cross-domain-context-promotion
fml-project-memory-conflict-resolution
```

Forbidden identities include:

```text
FML-1
FML-023
Feature 7
Future Item B
Miscellaneous import work
```

A sequence number may be recorded as metadata. It must not be the identity of the remembered capability.

#### AG.5.4 Canonical FML Item Detail Page

Every FML item detail page must contain, as applicable:

```text
Canonical FML title
Canonical FML ID
Architecture version
Document revision
Discovery source
Discovered time
Discovered by
Operator need
Governing question
Capability summary
Why it matters
Current classification
Lifecycle status
Target architecture release
Target product release, if known
Parent Epic or Feature, if promoted
Owning application subsystem or subsystem-candidate decision
Affected subsystem contracts and detail pages
Scope
Explicit non-goals
Operator workflow impact
Canonical-model impact
Authority and ownership impact
Lifecycle and state-machine impact
Information and projection impact
Operator-surface impact
AI, retrieval, prompt, or harness impact
Runtime and deployment impact
Resource ownership classification and canonical naming
Owned namespace, service, runtime, store, gateway, policy, and observability names
Implementation substrate metadata
Foreign-application and historical-resource exclusions
Security, privacy, and trust-domain impact
Migration and compatibility impact
Evidence and provenance requirements
Acceptance evidence required
Typed outgoing dependencies
Typed incoming dependents
Dependency health
Conflicts and alternatives
Architecture-weaving state
Delivery-chain effect
Deployment-sequencing implications and constraints
Deferral, rejection, duplicate, or supersession rationale
Revisit trigger
Revisit date, if time-bound
Accountable owner
Decision and classification history
Linked specifications
Linked ADRs
Linked Architecture Smells
Linked Epics, Features, and Slices
Linked Chain Delivery nodes and handoffs
Linked delivery reports and acceptance evidence
Open questions
Last reviewed time
End-state or next required action
```

Fields that do not apply should be marked `not_applicable` with a short reason when omission would create ambiguity.

The detail page must preserve decision history. Current fields may be updated, but prior classification changes, dependency changes, promotion, rejection, or supersession decisions must remain inspectable.

#### AG.5.5 FML Classification and Lifecycle Status

Classification and lifecycle status are independent axes.

Allowed classifications are:

```text
required_now
planned_compatible
planned_breaking
fork_candidate
rejected
duplicate
unresolved
```

Recommended lifecycle states are:

```text
captured
triage_pending
analysis_active
dependency_blocked
ready_to_weave
woven
promoted_to_feature
delivery_active
delivered_pending_acceptance
accepted
deferred
rejected
superseded
```

Do not overload classification to represent delivery progress.

Lifecycle status also governs **buildability** — whether an item may be selected for implementation:

- **Ideation (pre-weave):** `captured`, `triage_pending`, `analysis_active`, `dependency_blocked`, and `ready_to_weave` are *recorded* ideas. They are tracked, classified, and edge-linked, but are **not** placed in the buildable deployment order. An idea that has not been analyzed and woven into the architecture is not eligible for coding, regardless of whether its prerequisites are met.
- **Baked (weave onward):** an item becomes buildable only once **`woven`** — woven into the architecture (or later: `delivery_active`, `accepted`). Weaving is the deliberate **bake**: the operator-controlled hand-off that moves an idea out of ideation and into the build order.
- **Terminal:** `deferred`, `rejected`, and `superseded` are neither ideation nor buildable; they remain in the ledger as memory.

The living deployment order (§AG.5.10) must surface pre-weave items in a distinct **ideation** section, separate from the buildable set, so that recorded ideas stay visible without being mistaken for available work. Recording an idea (capture) and committing to build it (weave) are separate acts; the ledger must not collapse them.

**Build-ready completeness gate.** Weaving an item (`captured → woven`) is legitimate only when the item is build-ready. Build-readiness is an operator-satisfaction gate on completeness, not a promotion tier. An item is build-ready once:

- it declares its **altitude** — either **`subsystem`**, with all of the subsystem's features enumerated, or **`feature`**, with the single feature's needs stated;
- its **impacts** are mapped;
- its **dependencies and edges** are mapped (no unknown dependency health, no unexplained edge).

The harness must **check these preconditions mechanically** and refuse to weave an item that fails them (for example, by failing ledger regeneration while a `woven`/`accepted` item is under-mapped). The **operator asserts satisfaction** by promoting the item to `woven`; the machine verifies completeness, the operator owns the judgement. An item that cannot yet meet the gate stays in ideation.

#### AG.5.6 Typed FML Interdependencies

FML interdependencies must be represented as typed relationships between canonical FML IDs.

The minimum relationship vocabulary is:

```text
requires
    The source item cannot be honestly completed without the target item.

depends_on_decision
    The source item cannot be classified or woven until a named decision represented by the target item is resolved.

conflicts_with
    The two items cannot coexist as currently defined without an explicit architectural resolution.

shares_foundation_with
    The items are independently valid but should reuse or coordinate around a common canonical concept, workflow, platform capability, or operator surface.

supersedes
    The source item replaces the target item and must define migration, archival, and downstream effects.

duplicates
    The source item represents the same underlying capability as the target and should be reconciled into one canonical item.
```

The following relationships are derived rather than stored independently:

```text
A requires B
→ B enables A

A supersedes B
→ B is superseded_by A

A duplicates B
→ B duplicates A
```

Do not maintain separate hand-edited inverse edges that can drift.

A canonical dependency edge is recorded exactly once.

- directional relationships are owned by the source FML item;
- incoming-dependent lists are derived projections;
- symmetric relationships are stored once with an explicit edge owner and projected onto both item pages;
- visual graphs are derived from the same canonical edge records.

Each dependency edge must contain:

```text
Canonical dependency edge ID
Source FML ID
Relationship type
Target FML ID
Rationale
Hard or soft criticality
Current edge state
Resolution or satisfaction condition
Owner
Introduced by decision, report, or discovery source
Last reviewed time
```

Allowed edge states are:

```text
proposed
confirmed
satisfied
accepted_risk
removed
superseded
```

#### AG.5.7 Hard and Soft Dependencies

A hard dependency means the source item cannot reach `woven`, `delivered_pending_acceptance`, or `accepted` honestly until the dependency is satisfied or the architecture is explicitly changed.

A soft dependency means coordinated delivery is beneficial, but the source item may proceed with a documented limitation, accepted risk, or future reconciliation requirement.

Required rule:

```text
required_now FML item
+ unresolved hard dependency
→ item is dependency_blocked
→ architecture weaving or closure prohibited
```

An accepted risk must identify:

- the accountable owner;
- the limitation being accepted;
- the affected operator or system outcome;
- the expiration or revisit trigger;
- the rollback or remediation path.

`accepted_risk` must not be used as a permanent substitute for resolving a foundational dependency.

#### AG.5.8 Dependency Cycles

The FML dependency model must detect cycles among hard directional relationships.

Required rule:

```text
A requires B
+ B requires A
→ cycle_detected
→ neither item may be represented as independently ready
```

A hard cycle must be resolved by one of the following:

- merge the items because they are one capability;
- extract a shared foundational FML item required by both;
- change one dependency to soft with an explicit accepted limitation;
- sequence a minimal bootstrap capability that breaks the cycle;
- reject or redesign one direction.

Symmetric relationships such as `conflicts_with`, `shares_foundation_with`, and `duplicates` are not hard prerequisite cycles, but they still require disposition.

#### AG.5.9 Dependency Propagation and Reconciliation

A material change to an FML item must trigger review of its incoming dependents.

Review is required when an item is:

- reclassified;
- deferred;
- rejected;
- superseded;
- promoted into a Feature;
- moved to another architecture release;
- changed from compatible to breaking;
- assigned to a fork;
- accepted with a limitation;
- declared delivered or removed.

Required test:

```text
Dependency target changes materially
+ dependent items not reviewed
→ FML dependency graph stale
```

Architecture release, branch, fork, and migration planning must include dependency reconciliation.

#### AG.5.10 Living Tiered Deployment Order

The FML tiered deployment order is a generated planning projection derived from the complete current set of canonical FML item records, typed dependency edges, dependency health, architecture readiness, accepted constraints, and delivery evidence.

It is not a fixed plan established once at the beginning of a program.

Every successfully implemented FML item creates new architectural knowledge. Implementation may reveal:

- previously unknown prerequisites;
- new incoming or outgoing dependencies;
- shared foundations that should be extracted or completed first;
- sequencing constraints;
- conflicts or incompatibilities;
- accepted limitations and their downstream effects;
- superseded or duplicated capabilities;
- migration, runtime, security, operator-surface, or harness implications;
- work that can now move earlier because a foundation exists;
- work that must move later because an assumption proved false.

After each FML item is successfully implemented, and before the next FML implementation is selected or begun, the project must:

1. update the implemented item's canonical detail page with the as-built outcome and learned implications;
2. reconcile all changed or newly discovered typed dependency edges;
3. review affected incoming dependents under AG.5.9;
4. recompute tier membership and ordering across the complete active FML graph;
5. regenerate the tiered deployment-order projection from canonical records;
6. record the generation time, material movements, and rationale;
7. use the regenerated projection—not the prior plan—to select the next FML work.

Required rule:

```text
FML item successfully implemented
→ canonical item truth and dependency graph reconciled
→ affected dependents reviewed
→ complete tiered deployment order regenerated
→ next FML selected from the new projection
```

Tier assignments may move forward, move backward, merge, split, or disappear. An FML item may not retain its old tier merely because the prior order was approved or communicated.

Required principle:

> **The FML tiered deployment order is a living derived projection of current architectural knowledge, not a commitment to the original sequence.**

If recalculation produces no change, the project must still record that the order was regenerated and found unchanged. Hand-editing the generated order without changing its canonical FML records or dependency edges is forbidden.

#### AG.5.11 Promotion into Delivery

Promotion of an FML item into an Epic, Feature, or Slice does not erase the FML record.

The item detail page must record:

- the promoted Epic or Feature ID;
- the governing specification;
- the Chain Delivery nodes and handoffs;
- delivery status;
- acceptance evidence;
- any residual capability not covered by the promoted work.

Required rule:

```text
FML item promoted to Feature
→ FML detail page remains canonical architectural memory
→ Feature specification governs implementation
→ Chain Delivery Register governs current delivery state
```

The FML item may reach `accepted` only when its declared operator outcome and acceptance evidence are complete. A merged PR or closed Feature does not automatically close the FML item.

#### AG.5.12 FML Operator Surfaces

When a project exposes the FML through an operator interface, it must provide:

1. an FML index surface;
2. one dedicated detail subpage per FML item;
3. incoming and outgoing dependency lists;
4. visible blocking state and the first unresolved hard dependency;
5. links to related specifications, Epics, Features, Chain Delivery nodes, ADRs, Smells, and delivery evidence;
6. classification and status history;
7. revisit triggers and overdue review state;
8. the current generated deployment tier and relative order;
9. the tiered-order generation time, material movement since the prior generation, and movement rationale.

A visual dependency graph is optional.

A complete typed dependency list is mandatory.

The UI must not imply that an item is ready merely because its own detail fields are complete while a hard dependency remains unresolved.

#### AG.5.13 Deferred and Closed Items

A feature may not disappear from architecture discussion merely because it is not included in the current implementation slice.

Deferred work must remain explicit on its detail page and in the index.

Rejected, duplicate, superseded, and accepted items remain preserved as architecture history. They may move out of the default active view, but they must remain searchable and linkable.

Required rule:

```text
FML item no longer active
→ preserve detail page, decision history, and relationships
→ never silently delete architectural memory
```

### AG.6 Architecture Weaving Gate

Before coding begins, every `required_now` capability must have a canonical FML detail page, reconciled typed dependencies, and be mapped to:

- an operator outcome;
- an owning application subsystem or explicit subsystem-creation decision;
- affected subsystem contracts and shared-subject ownership;
- a canonical concept or declared projection;
- an authority owner;
- lifecycle states;
- information flow;
- workflow transitions;
- operator surfaces;
- failure behavior;
- evidence or provenance requirements;
- security behavior;
- acceptance criteria;
- an implementation slice;
- satisfied, accepted, or explicitly resolved hard dependencies;
- reviewed incoming dependents that may be affected by the weaving decision.

A feature is not architecturally included merely because it appears in prose.

It must be woven through every affected layer.

Required test:

```text
Feature named
+ no canonical, workflow, surface, or acceptance mapping
→ feature not architecturally included
```

Coding must not begin while a `required_now` capability remains unmapped.

### AG.7 Omission Versus Scope Creep

The Feature Recall process must distinguish between:

#### Omission

A capability necessary for the declared operator outcome to work honestly.

#### Future extension

A useful capability that can be added without invalidating the current outcome.

#### Scope expansion

A new operator outcome or product responsibility not required for the declared release.

#### Architecture fork candidate

A capability requiring incompatible semantics, trust boundaries, ownership, or product behavior that may need an independent architecture lineage.

The existence of a remembered feature does not automatically authorize its implementation.

## AH. Architecture Evolution, Versioning, and Forking

### AH.1 Governing Principle

Architecture versions describe changes to the governed meaning and operating model of the system.

They must not be determined by:

- document length;
- number of features;
- implementation effort;
- marketing preference;
- elapsed time;
- repository tags alone.

Architecture versioning answers:

> Can a system, operator, and contributor that understand the prior architecture continue to operate correctly under the new architecture without reinterpreting canonical meaning?

### AH.2 Separate Version Axes

Every project must distinguish:

```text
architectureVersion
productRelease
documentRevision
schemaVersion
```

These values may move independently.

#### `architectureVersion`

Version of the governed operator, semantic, workflow, ownership, and trust model.

#### `productRelease`

Version of the shipped product or implementation.

#### `documentRevision`

Editorial revision of an architecture document.

#### `schemaVersion`

Machine-readable contract version for a particular record, API, event, or payload.

Changing wording does not necessarily change the architecture version.

Shipping code does not necessarily change the architecture version.

Changing a schema does not necessarily change the architecture version if the governed semantics remain compatible.

### AH.3 Pre-1.0 Architecture

Use `0.x` while the project is still establishing its first coherent architecture baseline.

Examples:

```text
0.1 — initial operator and conceptual model
0.2 — canonical ownership and workflow added
0.3 — operator surfaces and acceptance model added
0.9 — release-candidate architecture
```

A `0.x` architecture may still be implemented and tested.

However, it remains explicitly open to foundational change.

### AH.4 Architecture 1.0

Architecture `1.0` means:

- the primary operator outcome is explicit;
- the principal conceptual model is coherent;
- canonical ownership is declared;
- current truth and history are separated;
- the complete primary lifecycle is specified;
- the primary operator surfaces are defined;
- failure and recovery behavior are honest;
- the first realistic end-to-end workflow is accepted;
- known omissions have been classified in the Feature Memory Ledger;
- the architecture can support real use without relying on undocumented conversation history.

Architecture `1.0` does not mean:

- every possible feature exists;
- the product is permanently complete;
- no future migration will occur;
- the architecture is perfect;
- the backlog is empty.

The correct interpretation is:

> `1.0` is the first complete, coherent, and operable architectural contract for the declared product outcome.

### AH.5 Compatible Minor Architecture Releases

Use `1.1`, `1.2`, and subsequent minor versions when capabilities are added without breaking the governing meaning of `1.0`.

A minor release may add:

- new operator surfaces;
- new optional workflows;
- new integrations;
- new derived fields;
- new projections;
- new evidence sources;
- new compatible lifecycle states;
- new reports;
- new import or export paths;
- new administrative capabilities;
- new model roles operating within existing authority boundaries.

A minor release must preserve:

- canonical identity;
- canonical ownership;
- authority precedence;
- meaning of existing lifecycle states;
- current-versus-history rules;
- existing operator-owned data;
- existing evidence and provenance;
- safe interpretation of prior canonical records;
- prior trust and egress guarantees.

A minor release may require a technical migration.

It must not require reinterpretation of what existing canonical truth means.

Required test:

```text
Old canonical truth
+ new architecture
→ remains valid and correctly interpretable
```

If that test fails, the change is not minor.

### AH.6 Patch Architecture Revisions

Use patch versions such as `1.0.1` when correcting or clarifying the architecture without adding a new governed capability.

Examples:

- resolving contradictory wording;
- correcting a diagram;
- clarifying an invariant;
- adding a missing deterministic fixture for an already-governed rule;
- correcting an accidental omission in field documentation;
- improving examples without changing behavior.

A patch must not introduce a new operator outcome, canonical concept, lifecycle, authority rule, or trust boundary.

### AH.7 Major Architecture Releases

Use `2.0`, `3.0`, and subsequent major versions when the governed product meaning changes incompatibly.

A major version is required when one or more of the following changes:

- the primary operator question;
- the product's responsibility or boundary;
- canonical ownership;
- canonical identity semantics;
- authority precedence;
- current-versus-history behavior;
- correction precedence;
- lifecycle meanings in a way that invalidates old interpretation;
- evidence or provenance requirements;
- task or commitment semantics;
- external-provider trust or egress rules;
- destructive merge or resolution behavior;
- the meaning of an accepted operator action;
- the source-preservation model;
- a foundational invariant;
- the required migration makes old canonical records unsafe or ambiguous without transformation.

Required test:

```text
Existing operator or system
+ prior architectural understanding
+ new architecture
→ could reach a materially wrong conclusion
```

If true, the architecture requires a major version.

A major version must define:

- migration;
- compatibility;
- coexistence period;
- rollback;
- data transformation;
- projection rebuilding;
- operator communication;
- old-client behavior;
- archival treatment;
- deprecation and removal rules.

### AH.8 Architecture Release Decision Table

```text
Editorial clarification only
→ patch

New compatible capability
→ minor

Existing canonical meaning changes
→ major

Existing lifecycle meaning changes incompatibly
→ major

New optional projection or report
→ minor

New canonical entity with no impact on prior meaning
→ usually minor

Canonical ownership moves between systems
→ major

Current and history semantics change
→ major

Trust boundary or external-egress guarantee changes
→ major

Temporary exploration of a possible design
→ branch

Long-lived incompatible product or architecture direction
→ fork
```

### AH.9 Architecture Branches

An architecture branch is a temporary proposal used to evaluate a possible change.

A branch:

- inherits the current architecture;
- is not independently canonical;
- has a defined question;
- has an owner;
- has an evaluation period or decision trigger;
- ends in merge, rejection, or conversion into a fork.

Branches should be used for:

- design experiments;
- alternative workflows;
- model evaluations;
- UI explorations;
- migration proposals;
- possible major-version changes.

Do not create a fork merely to avoid making a decision.

### AH.10 Architecture Forks

An architecture fork is justified only when two incompatible but valid architectural directions must coexist for a meaningful period.

Possible reasons include:

- different primary operators;
- different product outcomes;
- incompatible canonical semantics;
- incompatible privacy or sovereignty requirements;
- incompatible deployment models;
- incompatible authority structures;
- distinct regulatory boundaries;
- different source-of-truth ownership;
- a major product specialization that would make the shared architecture misleading.

A fork is not justified by:

- a different UI theme;
- one optional feature;
- an experimental model;
- a temporary deployment difference;
- a customer-specific configuration;
- reluctance to perform a migration;
- disagreement that can be resolved through an ADR.

### AH.11 Required Fork Record

Every architecture fork must define:

```text
Fork name
Parent architecture and version
Fork point
Reason for divergence
Operator outcome
Inherited principles
Overridden principles
Canonical-model differences
Workflow differences
Trust-boundary differences
Data compatibility
Migration paths
Shared platform boundary
Shared code boundary
Independent code boundary
Merge-back conditions
Permanent-divergence conditions
Retirement conditions
Owner
```

The fork must identify which parent sections are:

```text
inherited
extended
replaced
not_applicable
```

Unstated inheritance is not sufficient.

### AH.12 Shared Capability Rule for Forks

Forked architectures may share platform capabilities.

They must not share ambiguous canonical ownership.

Required rule:

```text
Shared capability
→ generic contract

Fork-specific meaning
→ owned by the fork
```

Do not place product-specific semantic knowledge into a shared platform merely to reduce code duplication.

### AH.13 Merge, Rebase, and Retirement

Every branch or fork must have a declared end condition.

Possible outcomes:

- merge into the parent;
- become the next major parent version;
- remain a permanent independent lineage;
- be retired;
- be archived as a rejected experiment.

When merging or rebasing:

- conflicting invariants must be resolved explicitly;
- canonical ownership must have one winner;
- migration must be defined;
- duplicate concepts must be reconciled;
- inherited and replaced sections must be recorded;
- acceptance must be rerun against the resulting architecture.

### AH.14 Architecture Release Packet

Every architecture release must include:

1. Version number.
2. Parent version.
3. Release classification: patch, minor, major, or fork.
4. Summary of changes.
5. Feature Memory Ledger item, classification, and dependency-graph changes.
6. New capabilities.
7. Deferred capabilities.
8. Changed canonical concepts.
9. Changed lifecycle behavior.
10. Changed operator surfaces.
11. Changed invariants.
12. Changed forbidden outcomes.
13. Migration requirements.
14. Compatibility statement.
15. Acceptance evidence.
16. Delivery Record Index changes and the canonical slice, TDD-stage, and pull request reports included in the release.
17. Known risks.
18. Revisit triggers.
19. Updated diagrams.
20. Superseded documents.
21. Effective date.

### AH.15 Release Questions

Before assigning an architecture version, ask:

```text
Does the new architecture change what the operator believes to be true?

Does it change who owns truth?

Does it change what an existing state means?

Can prior canonical records still be interpreted safely?

Can prior operator corrections still be honored?

Can the old and new architecture operate against the same canonical store?

Is migration mechanical, or does it require semantic reinterpretation?

Can both directions coexist without creating competing truth?

Is this an extension of the same product or a different product?

Are we creating a fork because coexistence is necessary, or because a difficult decision is being avoided?
```

### AH.16 Final Versioning Rules

1. `1.0` means coherent and operable, not feature-complete.
2. Minor versions add compatible capability.
3. Patch versions clarify or correct without adding governed behavior.
4. Major versions change canonical meaning or architectural guarantees.
5. Technical difficulty alone does not make a release major.
6. A database migration alone does not make a release major.
7. A semantic migration generally does.
8. Branches are temporary.
9. Forks represent long-lived incompatible architectural truth.
10. Every deferred feature remains visible in the Feature Memory Ledger.
11. Every accepted feature must be woven through all affected architecture layers.
12. Architecture history must remain inspectable.


## AI. Specification and Pull Request Naming Contract

### AI.1 Governing Principle

Specification names and pull request names are durable architecture metadata.

A name must tell a future engineer what capability is governed or changed without requiring the issue tracker, implementation sequence, branch history, or original conversation.

Required rule:

```text
Sequence
→ metadata

Capability and outcome
→ identity
```

Names such as `PR1`, `PR 1`, `Spec 2`, `Phase 3`, or `final-v2` are not acceptable identities.

A sequence number may describe build order, but it may not be the primary name of a specification, pull request, branch, release packet, or implementation slice.

### AI.2 Specification Naming

Every substantial specification must define:

```text
Display title
Canonical specification ID
Canonical filename
Architecture version
Document revision
Status
```

#### Display title

Use:

```text
<Product or domain> — <Specific capability or operator outcome> Specification
```

The title must identify the governed capability or operator outcome.

Good examples:

```text
Atlas — Logseq Knowledge Import Specification
Atlas — Project Intelligence Extraction Specification
PortfolioOS — Governed News Evidence Candidate Ingestion Specification
PortfolioOS — Investment Lead Qualification Specification
```

Weak or forbidden examples:

```text
Import Spec
Feature Spec
Phase 2 Spec
Spec 3
Backend Spec
Architecture Updates
New Workflow v2
Final Spec
Final Spec Revised
```

#### Canonical specification ID

Use stable lowercase kebab-case:

```text
<product-or-domain>-<specific-capability>
```

Examples:

```text
atlas-logseq-knowledge-import
atlas-project-intelligence-extraction
portfolioos-news-evidence-candidate-ingestion
portfolioos-investment-lead-qualification
```

The canonical ID must remain stable across document revisions unless the governed capability itself changes identity.

#### Canonical filename

Use:

```text
<canonical-specification-id>-spec.md
```

Examples:

```text
atlas-logseq-knowledge-import-spec.md
portfolioos-investment-lead-qualification-spec.md
```

Repository ordering prefixes are permitted only when useful:

```text
03-atlas-logseq-knowledge-import-spec.md
```

The descriptive name remains mandatory. A numeric prefix alone is never sufficient.

Architecture version and document revision belong in the specification metadata unless the repository's accepted release process requires immutable versioned copies.

### AI.3 Resource, Component, Namespace, and Runtime Naming

#### AI.3.1 Governing principle

Runtime and infrastructure names are durable ownership metadata.

A resource name must identify the architectural owner and the capability it provides. It must not primarily identify the framework, vendor implementation, library, protocol, or accidental namespace in which it happens to run.

Required rule:

```text
Architectural owner + product capability
→ primary identity

Implementation framework, vendor, image, protocol, and operator
→ metadata
```

For example, an application-owned agent runtime implemented with OpenShell is the **<Product> Agent Runtime**, not the “OpenShell service.” OpenShell remains visible through image provenance, labels, annotations, execution manifests, deployment documentation, and support runbooks.

#### AI.3.2 Ownership classification before naming

Every material runtime resource must be classified before it is named, reused, migrated, or bound into an application:

```text
product_owned
application_foundation
shared_platform
external_dependency
foreign_application
historical_artifact
```

**product_owned** means the product owns the capability, authorization boundary, lifecycle, state, operating contract, and application integration.

**application_foundation** means the resource serves several subsystems inside one product while retaining product-specific semantics or state.

**shared_platform** means the capability was intentionally designed, governed, funded, secured, operated, and accepted for multiple applications without owning any one application's semantics or canonical state.

**external_dependency** means the capability is outside the product and platform ownership boundary and is consumed through an explicit contract.

**foreign_application** means another application owns the resource. Physical proximity, common technology, spare capacity, or a shared namespace does not make it reusable.

**historical_artifact** means the resource remains from an experiment, retired architecture, migration, or abandoned implementation and has no current architectural authority.

Required rule:

```text
Ownership unknown
→ resource unavailable for binding or reuse
```

#### AI.3.3 Product-owned names

Product-owned resources use the canonical product prefix:

```text
<product>-<capability>
```

Examples:

```text
atlas-agent-runtime
atlas-agent-control-plane
atlas-agent-runtime-store
atlas-mcp-gateway
atlas-agent-policy
atlas-agent-observability

portfolioos-research-runtime
portfolioos-evidence-compiler
portfolioos-agent-runtime-store
```

The rule applies, where practical, to:

- Kubernetes namespaces;
- Deployments, StatefulSets, DaemonSets, Jobs, and CronJobs;
- Services, Routes, Ingresses, and gateway instances;
- service accounts, roles, policies, and capability grants;
- databases, schemas, queues, topics, collections, and operational stores;
- PVCs, Secrets, ConfigMaps, and mounted policy or prompt assets;
- dashboards, alerts, traces, and operational views;
- runtime, harness, and delivery records.

A subsystem-specific name may extend the product prefix:

```text
<product>-<subsystem>-<capability>
```

Use the shortest name that remains unambiguous about product ownership and capability.

#### AI.3.4 Shared platform names

A genuinely shared central capability uses:

```text
platform-<capability>
```

Examples:

```text
platform-model-serving
platform-research-egress
platform-observability
platform-mcp-gateway
```

A component must not receive a `platform-` name merely because:

- it runs in a shared cluster or namespace;
- a platform team deploys or patches it;
- several applications could theoretically use it;
- its underlying software is generic;
- reusing an existing service is convenient.

The `platform-` identity requires an accepted platform architecture defining multi-application ownership, isolation, authorization, lifecycle, quotas, observability, support, failure blast radius, upgrade policy, and explicit non-ownership of application semantics and canonical state.

Required rule:

```text
Runs on the platform
≠ platform-owned capability
```

#### AI.3.5 Capability identity versus implementation substrate

The primary architectural name identifies what the product owns and operates.

Implementation details belong in:

- `app.kubernetes.io/managed-by` and equivalent labels;
- image name and immutable digest;
- annotations;
- runtime and execution manifests;
- architecture and deployment documentation;
- ADRs;
- operator diagnostics;
- support and upgrade runbooks.

Avoid primary names such as:

```text
openshell
langgraph-server
agent-server
mongo
neo4j
qdrant
shared-runtime
common-agent
```

when those names hide the owning product and capability.

Prefer:

```text
atlas-agent-runtime
portfolioos-agent-runtime
atlas-knowledge-graph
portfolioos-evidence-vector-index
```

The technology may change without changing the product capability's canonical identity.

#### AI.3.6 Namespace and store naming

A namespace should identify the owning product or platform boundary.

Examples:

```text
atlas
atlas-agent-runtime
portfolioos
portfolioos-agent-runtime
platform-model-serving
```

A separate namespace may be used for isolation, operational ownership, or blast-radius control. Namespace separation does not transfer product ownership to a framework or platform.

Application-specific operational persistence must remain visibly subordinate to the owned capability:

```text
<product>-<capability>-store
```

Its specification and metadata must state whether it is:

```text
canonical
operational_noncanonical
projection
cache
index
checkpoint
```

For agent runtimes, internal framework state, sandbox state, session state, and runtime bookkeeping are normally `operational_noncanonical` and subordinate to the application-owned `AgentRun`, `AgentAttempt`, workflow, and canonical result records.

#### AI.3.7 Existing-resource and foreign-ownership rule

Before selecting an existing cluster resource, record:

```text
Current name
Current owner
Current purpose
Architecture lineage
Canonical or non-canonical state
Current consumers
Trust domains
Credentials and authorization boundary
Persistence and retention
Reuse eligibility
Required migration or transfer decision
```

A product must not bind to, reuse, scale, rename, migrate, or repurpose a `foreign_application` or `historical_artifact` resource without an explicit accepted architecture decision.

The default is exclusion.

Required rule:

```text
Existing resource belongs to another application or obsolete experiment
→ exclude from the new product architecture
→ do not rehabilitate it by renaming

portfolioos-agent-runtime
→ cannot become atlas-agent-runtime through scale-up or rename
```

A deliberate ownership transfer requires:

- consent of the current owner;
- canonical-state and data-custody analysis;
- consumer migration;
- trust and credential re-issuance;
- downtime and rollback planning;
- rename or replacement strategy;
- updated FML, ADR, Subsystem Architecture Map, deployment records, and acceptance evidence.

#### AI.3.8 Naming review gate

Before implementation, reviewers must be able to answer:

```text
Which product or platform owns every material resource?

Does the primary name describe the owned capability rather than its implementation framework?

Why is any `platform-` resource genuinely shared?

Are any resources being reused from another application or historical experiment?

Which stores are canonical, and which are subordinate operational state, projections, caches, indexes, or checkpoints?

Would a future engineer understand ownership after the implementation technology changes?
```

If not, the runtime and resource naming plan is not ready.

### AI.4 Pull Request Naming

Every pull request title must describe the specific governed capability and the result of the change.

Preferred grammar:

```text
<Strong verb> <specific capability> <observable or governed outcome>
```

Useful verbs include:

```text
Establish
Implement
Preserve
Materialize
Expose
Integrate
Enforce
Reconcile
Migrate
Retire
Harden
Instrument
```

Good examples:

```text
Establish canonical Logseq source records and import invariants
Implement idempotent Logseq page and block ingestion
Preserve source provenance across Atlas knowledge extraction
Materialize the current project intelligence read model
Expose import conflicts for operator reconciliation
Enforce stale-work protection during project re-extraction
Instrument Atlas import replay and recovery
```

Weak or forbidden examples:

```text
PR1
PR 1
PR-01
Phase 1
Backend changes
Frontend work
Schema updates
Fixes
Misc fixes
Updates
Cleanup
Final changes
```

A technically precise but context-free title is also insufficient.

For example:

```text
Add collection
Update endpoint
Create component
```

must instead identify the domain object, workflow, or operator outcome being changed.

### AI.5 Slice Order Is Metadata

The implementation plan may record:

```text
Slice 1 of 6
Depends on: <named prior pull request>
Parent specification: <canonical specification ID>
```

This information belongs in the pull request description, implementation ledger, or project plan.

It does not replace an outcome-bearing title.

Required test:

```text
PR title removed from implementation sequence
+ viewed six months later
→ purpose remains understandable
```

### AI.6 Required Pull Request Metadata

Every architecture-bearing pull request must identify:

```text
Pull request title
Parent specification title and canonical ID
Architecture version
Implementation slice position, if relevant
Operator outcome advanced
Canonical records or invariants changed
Workflow states or transitions changed
Operator surfaces changed
Explicit non-goals
Acceptance evidence
Stop rule
Migration or compatibility impact
```

The pull request description must state what the change makes true, not merely list files modified.

### AI.7 Naming the Planned Build Before Coding

The specification build order must include the proposed name of every planned pull request before coding begins.

Each proposed name must map to:

- one bounded capability;
- one architectural layer or coherent cross-layer slice;
- one acceptance outcome;
- one stop rule.

If the scope changes materially during implementation, rename the pull request before merge so the final name describes the actual accepted change.

A misleading historic title must not be preserved merely because it was accurate when coding began.

### AI.8 Branch Naming

Where branch names are used, prefer:

```text
<canonical-specification-id>/<specific-slice>
```

Examples:

```text
atlas-logseq-knowledge-import/canonical-source-records
atlas-logseq-knowledge-import/operator-reconciliation
portfolioos-investment-lead-qualification/current-read-model
```

Avoid:

```text
pr1
phase-2
new-work
fixes
final
mark-test
```

Branch names are operational aids, but they should still preserve capability context.

### AI.9 Naming Review Gate

Before implementation begins, reviewers must be able to answer:

```text
What capability does this specification govern?

What exact outcome does each planned pull request produce?

Can the specification and pull request names be understood without sequence numbers?

Would the names remain meaningful after repository history, tickets, and conversation context are gone?

Do deployed resource names identify the owning product or intentionally shared platform capability?

Does any primary name expose only a framework, vendor, database, or ambiguous shared implementation?
```

If not, the naming plan is not ready.

### AI.10 Forbidden Naming Outcomes

```text
Sequence number only
+ used as specification identity

Generic technical noun
+ no governed capability or outcome

Pull request title
+ describes files changed rather than behavior made true

Scope changes materially
+ pull request retains a misleading title

Specification fork
+ parent capability and divergence absent from the name or metadata

Document revision
+ mislabeled as a new architecture version

Application-owned component
+ named primarily after OpenShell, LangGraph, a database, gateway implementation, or other substrate

Resource runs in a shared cluster
+ receives a `platform-` identity without an accepted shared-platform architecture

Foreign-application or historical resource exists
+ rebound, renamed, scaled, migrated, or repurposed without an explicit ownership-transfer decision

Operational runtime store
+ named or presented as canonical application truth

Ambiguous name such as `agent-server`, `shared-runtime`, or `common-service`
+ ownership cannot be determined from architecture metadata
```

Each project should enforce these outcomes through review templates and repository conventions where practical.

---

## AJ. Architecture Smells Seed

### AJ.1 Governing Principle

Architecture defects rarely arrive already labeled as invariant violations. They usually appear first as recurring suspicious patterns: a second source of truth, an overloaded state, a hidden fallback, a prompt carrying policy that should be deterministic, or a surface that cannot identify its canonical revision.

The Architecture Smells Seed exists to make those warning patterns explicit before they become normalized implementation.

A smell is not automatically a defect. It is a named review trigger that requires evidence, disposition, and an owner.

Required distinctions:

```text
Architecture smell
→ suspicious pattern requiring review

Invariant
→ truth that must always hold

Forbidden outcome
→ invalid product or system state that must be prevented and tested

Defect
→ observed violation requiring correction

Feature Memory Ledger entry
→ remembered or discovered capability requiring scope classification
```

The Smells Seed complements these controls. It does not replace them.

### AJ.2 Required Project Artifact

Every substantial project must maintain:

```text
05-architecture-smells-seed.md
```

The artifact begins with the inherited h00pz smell seed and adds project-specific smells discovered during design, implementation, acceptance, operations, and architecture evolution.

It is called a seed because it is intentionally incomplete at project start. It must grow when a new recurring failure pattern is discovered.

It must not become an unbounded list of vague preferences. A smell belongs in the seed only when it identifies:

- an observable pattern;
- a credible architectural or product failure mode;
- a review question or detection method;
- a disposition path.

### AJ.3 Smell Naming

Every smell must have:

```text
Descriptive display name
Stable canonical smell ID
Category
```

Use a descriptive identity such as:

```text
Competing Canonical Owners
smell-competing-canonical-owners

Current Truth from Multiple Revision Roots
smell-current-truth-multiple-revision-roots

Prompt-Only Governance
smell-prompt-only-governance

Sequence as Identity
smell-sequence-as-identity
```

Avoid:

```text
Smell 1
SMELL-001
Data Smell
Architecture Issue
Bad Pattern
Miscellaneous Concern
```

A sequence number may be recorded for ordering or reporting, but it may not be the smell's identity.

Required rule:

```text
Sequence
→ metadata

Failure pattern
→ smell identity
```

### AJ.4 Smell Record Contract

Every smell record must define:

```text
Display name
Canonical smell ID
Category
Observable symptom
Failure mode
Why it matters
Detection questions or checks
Affected architecture layers
Evidence or examples
Current disposition
Required remediation or accepted rationale
Related invariant, forbidden outcome, ADR, or specification
Owner
Revisit trigger
Status
```

Allowed dispositions are:

```text
not_present
watch
present_requires_action
present_accepted_by_adr
resolved
not_applicable
```

`present_accepted_by_adr` requires an explicit ADR that explains why the smell is acceptable, the bounded consequences, and the revisit trigger.

A smell may not be dismissed with `expected`, `temporary`, or `fine for now` without a recorded rationale and exit condition.

### AJ.5 Inherited h00pz Smell Seed

Every project begins by evaluating at least the following smells.

#### Operator and semantic smells

- **Wrong Question, Correct Answer** — the system produces a technically valid result for an adjacent or ambiguous operator question.
- **UI Certainty Exceeds Governed Evidence** — the surface implies confidence, completeness, freshness, or authority that the underlying record does not support.
- **Feature Named but Not Woven** — a capability appears in prose or backlog text but is absent from canonical semantics, workflow, surfaces, or acceptance.
- **Worker Completion Masquerades as Product Completion** — a successful job or model response is treated as proof that the operator outcome is complete.
- **No Honest Terminal State** — the workflow can stop only through success, failure, or endless retry, with no supported exhausted, unavailable, or unresolved outcome.

#### Canonical truth and state smells

- **Competing Canonical Owners** — two records, stores, services, or surfaces can independently claim authoritative truth for the same concern.
- **Current Truth from Multiple Revision Roots** — one current operator view assembles fields from different or superseded revisions.
- **Historical Backfill Masquerades as Current** — missing current data is silently filled from older history.
- **Projection Becomes Truth** — a cache, index, graph, vector store, or read model begins accepting canonical writes or governing behavior.
- **Generic Catch-All State** — one status field carries workflow, evidence, routing, projection, and operator-review meaning.
- **Retry Creates Identity** — replay or retry can create a new canonical object, duplicate task, or competing derived result.
- **Operator Correction Rewrites Source** — correcting derived interpretation mutates or destroys preserved source evidence.

#### AI and evidence smells

- **Prompt-Only Governance** — a load-bearing invariant, authority rule, numeric restriction, or lifecycle gate exists only in prompt wording.
- **Confidence Without Custody** — a high-confidence claim lacks a valid source artifact and exact evidence reference.
- **More Research Repairs Evaluation Defects** — missing model output, broken assembly, or bad adjudication triggers unnecessary external research.
- **Model Output Promoted by Implication** — generated text becomes canonical because no explicit promotion boundary was defined.
- **Hidden Retrieval Downgrade** — a live-required question is answered from memory, stale cache, or incomplete internal context without visible degradation.
- **Harness Green, Semantics Unknown** — schema, process, or fixture checks pass while the meaning, evidence quality, or operator usefulness of the result remains unevaluated.
- **Exact Prose Golden** — semantic evaluation compares generated wording byte-for-byte instead of testing governed claims, dispositions, evidence, omissions, and allowed variation.
- **Model Change Without Replay** — a model, prompt, policy, retrieval, or context-assembly change reaches the live system without replay against the affected calibration and regression packs.
- **Failure Found but Not Captured** — a production defect or flyswatting lesson is fixed without adding a durable harness case that can prove the failure does not return.

#### AI application subsystem smells

- **Feature Pile Becomes Subsystem** — related Features accumulate without an accepted subsystem charter, canonical model, internal lifecycle, or operator contract.
- **Page Defines the Domain** — a surface introduces subjects, statuses, or decisions that no subsystem owns canonically.
- **Agent Becomes the Architecture** — an agent loop implicitly owns workflow, continuation, and truth because no subsystem architecture does.
- **Shared Database as Integration** — subsystems coordinate by directly reading and writing each other's records.
- **Cross-Subsystem Canonical Mutation** — one subsystem changes another subsystem's canonical truth without a governed contract.
- **One Big AI Brain** — one model or agent receives broad application context and is expected to infer subsystem boundaries and authority dynamically.
- **Context Soup** — cross-subsystem context lacks owner, revision, freshness, trust-domain, omission, and provenance contracts.
- **Generic AI Service Owns Domain Semantics** — a shared AI component becomes the hidden authority for several subsystem outcomes.
- **Duplicate Subject Core** — several subsystems maintain competing canonical identity or lifecycle for the same subject.
- **Cross-Subsystem Workflow Without Coordinator** — several subsystems participate but no durable owner tracks the complete application outcome.
- **Subsystem Harness Added Last** — Feature work advances before a subsystem-level case pack proves the integrated outcome.
- **Platform Absorbs Application Meaning** — reusable infrastructure acquires subsystem-specific workflow or semantics.
- **FML Item Without Subsystem Home** — a required capability is accepted without an owning subsystem or explicit subsystem-creation decision.

#### Platform and integration smells

- **Ambiguous Runtime Ownership Name** — a service such as `agent-server`, `shared-runtime`, or `common-service` does not identify the product or accepted platform owner.
- **Implementation Substrate as Product Identity** — a product-owned capability is named primarily after OpenShell, LangGraph, a database, protocol, or vendor implementation.
- **Platform Prefix by Location** — a component receives a `platform-` identity merely because it runs in a shared cluster or namespace.
- **Foreign Application Infrastructure Reuse** — one application binds to, scales, renames, migrates, or repurposes another application's runtime or stateful service without an explicit ownership-transfer architecture.
- **Historical Artifact Reanimated** — an obsolete experiment is treated as a current architecture candidate because it already exists.
- **Operational Store Appears Canonical** — framework, sandbox, session, checkpoint, or runtime bookkeeping is named or surfaced as if it owns canonical application workflow or truth.
- **Hard-Coded Runtime Dependency** — a production endpoint, database name, model identity, feature flag, limit, timeout, or environment-specific value is embedded in application logic or a container image.
- **Prompt Baked Into Application** — a load-bearing prompt, policy template, or model instruction can change only through an application rebuild rather than a governed ConfigMap-backed asset.
- **Secret in Plain Manifest** — a credential, token, connection string, or sensitive value appears directly in a Deployment or ConfigMap instead of a Secret reference.
- **Configuration Change Without Rollout** — a ConfigMap or Secret can change while workloads continue using an unidentified prior value with no checksum, immutable reference, reload contract, or effective-configuration evidence.
- **Configuration Alias Without Retirement** — multiple environment-variable names represent one concern without one canonical source, compatibility reason, owner, and removal trigger.
- **String Sentinel Masquerades as Type** — a URL, path, number, or identifier variable uses values such as `false`, `none`, `unused`, or `disabled` instead of a correctly typed enablement flag and validated value.
- **Shared Platform Knows Application Semantics** — reusable infrastructure contains domain-specific truth, lifecycle, or product decisions.
- **OpenShell Gateway and MCP Gateway Conflated** — the sandbox runtime control plane and capability access plane are described or authorized as one boundary.
- **Model-Controlled Tool Loop Outside Sandbox** — an autonomous or semi-autonomous agent selects tools, executes code, or reaches non-public systems from an ordinary broad-authority application process.
- **Sandbox Session Becomes Canonical Workflow** — durable work identity, status, checkpoint, or result exists only inside an ephemeral OpenShell session.
- **Sandbox Has Direct Database Access** — an agent can bypass application APIs and write or read canonical stores directly.
- **Sandbox Has Direct MCP Server Access** — the agent can bypass the governed MCP Gateway and its application binding.
- **Sandbox Has Arbitrary Internet Egress** — model-controlled execution can reach unregistered external destinations without a named capability and policy.
- **One Sandbox Spans Trust Domains** — one attempt includes personal, work, customer, tenant, or project contexts that are not governed as one domain.
- **Sub-Agent Inherits Parent Authority by Default** — a child execution receives the parent’s full context, credentials, and tool set without explicit attenuation.
- **Model Selects Its Own Execution Policy** — model output or prompt content can choose, widen, or relax the sandbox policy or capability grant.
- **Agent Output Directly Mutates Canonical Truth** — the sandbox result bypasses application validation, candidate state, operator approval, or deterministic promotion.
- **OpenShell Owns Application Meaning** — application workflow, canonicalization, or product semantics are embedded in sandbox runtime policy or control-plane code.
- **Network Reachability Masquerades as Tool Authorization** — an allowed connection is treated as permission to invoke a capability or perform a business action.
- **Ephemeral Sandbox State Required for Recovery** — retry or reconciliation depends on files or memory that disappear with the sandbox.
- **Shared OpenShell Gateway Assumed Multi-Tenant Without Proof** — applications or trust domains share a gateway despite unproven policy, identity, inference-route, audit, or failure isolation.
- **Hidden Fallback Behavior** — the system silently changes provider, source, method, model, or data basis while presenting one coherent result.
- **External Egress by Implication** — sovereign or sensitive context can leave the system because an external mode was selected without an explicit egress contract.
- **Generalized Platform Before Second Use** — a shared subsystem is built for one speculative consumer rather than a proven repeated capability.
- **Deferred Feature Loses Future Evidence** — a postponed capability depends on source, identity, provenance, or temporal data that the current architecture fails to preserve.
- **FML Row Without Detail** — a remembered capability exists only as a compact ledger row and cannot explain its complete impact, disposition, dependencies, or decision history.
- **Text-Only FML Dependency** — prerequisites, conflicts, or shared foundations are buried in prose rather than represented as typed links between canonical FML items.
- **Hard FML Dependency Cycle** — required capabilities depend on one another circularly and are each presented as independently ready.
- **FML Promotion Erases Memory** — promoting an item into an Epic, Feature, or Slice causes the original architectural rationale, residual scope, or revisit history to disappear.
- **FML Index Becomes Competing Truth** — the project-wide ledger summary and the item detail page can be edited independently and disagree about classification, status, or dependency state.
- **Frozen FML Tier Order** — the implementation sequence remains anchored to an earlier tier plan after completed FML work reveals new prerequisites, dependencies, implications, conflicts, shared foundations, or supersessions.

#### Delivery and evolution smells

- **Unmeasured Build Pipeline** — build, test, image, push, and rollout phases have no timings, cache evidence, or regression budget, so feedback degradation becomes normal before anyone can locate it.
- **Serialized Build Graph** — independent packages or stages execute through a hand-maintained sequential chain while available compute remains idle.
- **Dependency Reinstall on Every Build** — unchanged dependencies are restored, resolved, or rebuilt for each application change because dependency and source layers are not separated.
- **Whole Repository Rebuild for Local Change** — a change to one package, service, or surface causes unrelated components to rebuild and retest despite a knowable dependency graph.
- **Mutable Cache Without Input Identity** — cached dependencies or build products can be reused without a lockfile, source, toolchain, or configuration identity proving that the cache is valid.
- **Acceleration Without Clean-Build Proof** — the fast path works only with warm local state and no deterministic cold path proves that a clean environment can reproduce the artifact.
- **Configuration Change Triggers Application Rebuild** — an endpoint, prompt, policy, or environment value forces compilation or image creation even though it belongs to Kubernetes runtime configuration.
- **Build Succeeds but Wrong Digest Deploys** — a successful build or push is treated as proof that the intended immutable image digest reached the workload.
- **Checklist Progress Masquerades as Chain Progress** — completed TDD points, story points, or merged pull requests are reported as delivery progress without a named contiguous live frontier.
- **Completed Component Island** — a downstream component is implemented and perhaps deployed but cannot be reached from realistic ingress through the production chain.
- **Handoff Without Owner** — adjacent components exist, but nobody owns, instruments, tests, or accepts the transfer between them.
- **No Named Live Frontier** — the team cannot state where a realistic subject currently stops in the deployed workflow.
- **Fixture Frontier Presented as Live Frontier** — synthetic traversal is presented as evidence that the real production path works.
- **Cross-PR Handoff Gap** — adjacent pull requests each satisfy their local scope while the edge between them remains unimplemented or unproven.
- **Last Mile Deferred by Implication** — backend records and services are treated as product completion while the operator surface, action, or canonical write effect remains outside the tracked chain.
- **Percent Complete from Unequal Points** — checklist counts imply progress even though items differ radically in dependency, uncertainty, and operator value.
- **Sequence as Identity** — specifications, pull requests, branches, migrations, smells, or releases are identifiable only as `PR1`, `Phase 2`, `Smell 3`, or equivalent numbering.
- **Generic Change Name** — a durable artifact is named `updates`, `fixes`, `backend work`, `final`, or another label that hides the capability and outcome.
- **Architecture Branch Without Exit** — an experimental branch has no decision question, evaluation period, merge condition, fork condition, or retirement rule.
- **Fork Avoids a Decision** — incompatible lineages are created because ownership or semantics were not resolved, rather than because coexistence is necessary.
- **Fixture-Only Acceptance** — mechanical test data passes while no realistic operator subject proves semantic and surface correctness.
- **Temporary Complexity Without Removal Trigger** — compatibility code, dual writes, duplicate models, or transitional states have no retirement condition.
- **Harness as Script Pile** — critical evaluation depends on undocumented one-off commands, notebooks, or local state rather than a named architecture, case catalog, and repeatable execution contract.
- **Harness Bypasses Production Path** — a harness calls internal helpers, writes directly to stores, or uses test-only shortcuts that avoid the real API, queue, worker, retrieval, projection, or operator path it claims to prove.
- **Fixture Green, Live Unknown** — deterministic fixtures pass while the live model, live source, deployed workflow, or realistic operator subject has not traversed the same chain.
- **Skip Counted as Pass** — required gates are skipped, blocked, disabled, or not executed while the aggregate run is still presented as green.
- **Run Without Identity** — a harness result cannot be tied to an exact code digest, model, prompt, policy, schema, source snapshot, case-pack version, and effective runtime configuration.
- **Hidden State Between Runs** — prior records, caches, leases, projections, or generated artifacts can influence a later run without being declared, reset, or incorporated into the run manifest.
- **Benchmark Without Representative Workload** — performance conclusions are drawn from short prompts, synthetic data, or single-job runs that do not resemble the production context, concurrency, retrieval, or output pattern.
- **Test Backdoor Becomes Product Path** — fixture-only endpoints, bypass flags, direct-store writes, or privileged harness hooks remain reachable in normal production operation.

#### Agent operating and repository-truth smells

- **Agent Rules as Project Encyclopedia** — persistent instruction files contain copied project architecture, FML state, inventory, sequencing, or deployment truth instead of stable behavior and pointers.
- **Stale Truth in Agent Instructions** — an embedded HASF version, stack baseline, path, component, or architecture assertion no longer matches its canonical source.
- **Conversation Memory as Authority** — architecture-bearing work depends on chat or model memory that was never captured in the correct repository artifact.
- **Tool-Specific Rule Drift** — different agent or IDE instruction files prescribe materially different working behavior.
- **Feature Code Before Plan** — implementation begins before the accepted specification, bounded plan, and pre-build response establish scope and authority.
- **Review Agent Becomes Shadow Architect** — a delegated implementer or reviewer changes subsystem ownership, canonical semantics, or runtime boundaries outside the accepted plan.
- **Parallel Operational Mutation** — several actors mutate shared live state without one controller or an accepted safe-parallel runbook.
- **Code and Documentation Split** — code or runtime state changes while affected FML, architecture, current-state, specification, benchmark, or runbook records remain stale.
- **Current Architecture Missing** — target architecture exists but no canonical document describes the actual implemented and deployed system.
- **Target Presented as Built** — planned capability is presented as current without live and operator evidence.
- **Generated Projection Hand-Edited** — an FML index, tiered deployment order, README summary, or other projection is edited independently of its canonical source.
- **Tier Order Not Recomputed** — an FML implementation completes but the project selects subsequent work from the stale pre-implementation tier order.
- **Instruction Context Dependency** — correct maintenance requires one agent to retain a large prior conversation or hidden context because the repository cannot reconstruct truth.

### AJ.6 Smell Review Gates

The Architecture Smells Seed must be reviewed:

1. during the initial project foundation pass;
2. before accepting each substantial specification;
3. in the implementer's pre-build response;
4. before merging each architecture-bearing pull request;
5. during realistic end-to-end operator acceptance;
6. before a patch, minor, or major architecture release;
7. before converting an architecture branch into a fork;
8. after an incident, semantic defect, or repeated operator confusion reveals a new pattern.

Each review must record:

- applicable inherited smells;
- smells found;
- evidence;
- disposition;
- required action;
- accepted ADR exceptions;
- additions or changes to the project seed.

### AJ.7 Smell Escalation

A smell must be escalated when review proves that it is no longer merely suspicious.

```text
Smell
+ deterministic always-true requirement
→ invariant

Smell
+ product or system state that must never occur
→ forbidden outcome + deterministic fixture

Smell
+ observed violation
→ defect

Smell
+ recurring cross-project failure pattern
→ candidate addition to the governing h00pz seed
```

Escalation must preserve the original smell record and link it to the resulting invariant, forbidden outcome, defect, ADR, or framework revision.

### AJ.8 Smell Review Questions

Before accepting architecture or implementation, ask:

```text
Which inherited smells are present here?

Which smell are we calling temporary, and what removes it?

Is any policy load-bearing only because a prompt says so?

Can two components or surfaces both appear authoritative?

Does any current view mix revision roots or historical fallback?

Are we treating a completed worker as a completed product?

Are we building shared infrastructure before a second real use exists?

Does any deferred feature require evidence we are failing to preserve now?

Have we accepted a smell without an ADR, owner, and revisit trigger?

Did this project reveal a new smell that should be added to the seed?
```

### AJ.9 Forbidden Smell-Governance Outcomes

```text
Known smell present
+ no recorded disposition

Smell accepted
+ no ADR or revisit trigger

Smell named only by sequence number

Repeated defect pattern
+ never added to the project seed

Smell proven invariant violation
+ remains advisory only

Temporary compatibility architecture
+ no retirement condition

Project seed copied from framework
+ never reviewed against the actual architecture
```

The Smells Seed is useful only when it causes inspection, decisions, and learning. A copied checklist with no project-specific disposition is not compliance.

---


## AK. Runtime Configuration and Kubernetes Deployment Contract

### AK.1 Governing Principle

Production runtime configuration must be supplied by the deployment environment rather than embedded in application logic or container images.

For Kubernetes-hosted h00pz systems, the default contract is:

```text
Small scalar runtime value
→ environment variable

Secret scalar runtime value
→ environment variable from Secret key reference

Reusable non-secret scalar value
→ environment variable from ConfigMap key reference

Large, structured, or file-shaped non-secret configuration
→ ConfigMap-mounted file
→ environment variable points to the mounted path
```

This contract exists to prevent hard-coded:

- service and model endpoints;
- database names and connection details;
- feature flags;
- retry and polling behavior;
- timeouts and freshness limits;
- model identities and token budgets;
- prompt bodies;
- policy and calibration files;
- provider-specific settings;
- environment-specific paths.

A production behavior should not require an application rebuild merely because its deployment value, endpoint, prompt, bounded operating parameter, or environment assignment changed.

### AK.2 Configuration Source Classification

Every runtime setting must be classified as one of the following.

#### Secret

Use a Kubernetes Secret and `secretKeyRef` for:

- passwords;
- API keys;
- access tokens;
- private connection strings;
- credentials;
- sensitive certificates or key material.

Secrets must not be stored in ConfigMaps, checked into manifests, printed in logs, or exposed through diagnostic surfaces.

#### Small non-secret scalar

Use an environment variable, either directly in the Deployment or through `configMapKeyRef`, for:

- enablement flags;
- numeric limits;
- retry budgets;
- poll intervals;
- lease and heartbeat settings;
- model names;
- service URLs;
- database names;
- policy versions;
- mounted-file paths.

Shared or environment-specific scalar values should normally come from a ConfigMap key reference. A literal Deployment value is acceptable for a clear workload-local setting, but it remains deployment configuration rather than application code.

#### Large or structured non-secret configuration

Use a ConfigMap-mounted file for:

- prompts;
- policy documents;
- structured templates;
- calibration data;
- mapping tables;
- large allowlists or taxonomies;
- configuration that is clearer, safer, or more reviewable as a file.

An environment variable should identify the mounted directory or file path.

ConfigMaps must not be used to evade proper canonical storage. Mutable operator data, source evidence, workflow state, and durable corrections do not become configuration merely because they are representable as text.

Representative Kubernetes pattern:

```yaml
env:
  - name: MONGODB_URI
    valueFrom:
      secretKeyRef:
        name: atlas-mongo
        key: MONGODB_URI
  - name: ATLAS_DATABASE_NAME
    valueFrom:
      configMapKeyRef:
        name: atlas-runtime-config
        key: MONGODB_DATABASE
  - name: ATLAS_WORKER_MAX_ATTEMPTS
    value: "3"
  - name: ATLAS_REASONER_MODEL_URL
    valueFrom:
      configMapKeyRef:
        name: atlas-runtime-config
        key: REASONER_MODEL_URL
  - name: ATLAS_PROMPTS_DIR
    value: /etc/atlas/prompts
volumeMounts:
  - name: atlas-prompts
    mountPath: /etc/atlas/prompts
    readOnly: true
volumes:
  - name: atlas-prompts
    configMap:
      name: atlas-prompts-v1
```

The manifest names are examples. Each project must use its own stable capability prefix and governed configuration inventory.

### AK.3 Required Externalization Inventory

Every system and substantial feature specification must identify its runtime configuration inventory.

For each setting, define:

```text
Canonical name
Purpose
Owning component
Type
Unit
Required or optional
Secret or non-secret
Source: Deployment, ConfigMap, or Secret
Default, if explicitly allowed
Validation and bounds
Environment-specific behavior
Change and rollout behavior
Observability and redaction behavior
Compatibility aliases
Removal trigger for deprecated aliases
```

At minimum, review the following configuration classes:

- database and queue connections;
- internal and external service endpoints;
- model endpoints, names, credentials, and context budgets;
- feature flags;
- worker enablement;
- concurrency, retry, lease, heartbeat, and backoff settings;
- polling intervals and hard caps;
- freshness thresholds;
- prompt and policy locations;
- provider identities and user agents;
- storage paths;
- connector behavior;
- rollout-sensitive policy versions.

### AK.4 Configuration Is Not an Invariant Escape Hatch

Externalization does not mean every behavior should be configurable.

The following normally remain governed in code and specification:

- canonical identity rules;
- authority precedence;
- state-transition legality;
- source-preservation requirements;
- current-versus-history rules;
- evidence custody requirements;
- destructive-action protections;
- forbidden outcomes;
- security boundaries;
- product semantics.

A runtime setting may tune a bounded operating parameter. It must not silently redefine the product's governed meaning.

If a semantic rule is intentionally configurable, the specification must define:

- who may change it;
- its allowed range;
- its policy version;
- its effective time;
- its audit record;
- its impact on in-flight work;
- replay and comparison behavior;
- whether changing it requires an architecture version decision.

### AK.5 Naming, Typing, and Units

Kubernetes resource, namespace, service, runtime, gateway, store, policy, and observability names must follow **AI.3 Resource, Component, Namespace, and Runtime Naming**.

Environment-variable names must be descriptive and scoped.

Recommended form:

```text
<PRODUCT_OR_CAPABILITY>_<CONCERN>_<QUALIFIER>
```

Examples:

```text
FORGE_WORKER_MAX_ATTEMPTS
FORGE_WORKER_LEASE_TTL_SECONDS
FORGE_LEAD_REASONER_MODEL_URL
FORGE_PROMPTS_DIR
```

Required rules:

- use uppercase snake case;
- include units such as `_MS`, `_SECONDS`, `_MINUTES`, `_DAYS`, `_BYTES`, or `_TOKENS`;
- use explicit `true` and `false` boolean text;
- do not use ambiguous names such as `TIMEOUT`, `URL`, `MODEL`, or `ENABLED` without scope;
- do not overload one variable with multiple meanings;
- do not encode secrets in variable names;
- document numeric bounds and zero-value meaning;
- define whether an empty value is valid, unavailable, or an error;
- do not place string sentinels such as `false`, `none`, `unused`, or `disabled` in URL, path, numeric, or identifier variables;
- use a separate typed enablement flag when a capability or optional path may be disabled.

Compatibility aliases such as `MONGODB_URI` and `MONGO_URI` may temporarily point to one canonical Secret key. The alias must have:

- one canonical source;
- a compatibility reason;
- an owner;
- a deprecation notice;
- a removal trigger.

### AK.6 Prompt, Policy, and Calibration Assets

Load-bearing prompts and policy assets must not be hidden inside application code.

Use versioned ConfigMap-mounted files when size, readability, reviewability, or structured content makes environment variables unsuitable.

For each mounted prompt or policy asset, capture:

- logical name;
- file path;
- content version;
- content hash;
- owning feature;
- expected schema or template variables;
- maximum supported size;
- model or workflow compatibility;
- effective configuration revision.

A model-produced artifact should record the prompt or policy version and effective content hash used to produce it.

The application must not silently fall back to a baked-in production prompt when the required mounted asset is absent or invalid.

### AK.7 Startup Validation and Effective Configuration

Applications must validate runtime configuration before accepting work.

Required behavior:

- fail fast when a required setting is missing;
- parse values into explicit types;
- validate numeric ranges and units;
- validate URLs and file paths;
- validate cross-field dependencies;
- reject contradictory flags;
- verify required mounted files exist and are readable;
- reject oversized or malformed prompt and policy assets;
- never print secret values;
- expose a redacted effective-configuration summary or fingerprint;
- identify configuration source and revision in diagnostics.

Silent production defaults are prohibited for deployment-critical endpoints, credentials, database identities, prompt paths, or safety-relevant limits.

A default is allowed only when it is:

- safe;
- deterministic;
- documented;
- covered by tests;
- visible in the effective-configuration summary.

### AK.8 Configuration Change and Rollout

Every ConfigMap and Secret change must have an explicit activation model.

Preferred approaches include:

- immutable, versioned ConfigMap and Secret names;
- pod-template checksum annotations that force a Deployment rollout;
- another deterministic rollout mechanism tied to content revision.

The specification must define:

- whether change requires restart or supports reload;
- how old and new configuration coexist during rollout;
- how in-flight jobs retain the configuration revision under which they began;
- how rollback restores the prior configuration;
- how the operator confirms which configuration is active.

Hot reload must not be assumed. It requires a defined atomicity, validation, failure, and observability contract.

### AK.9 Local Development and Test Environments

Local execution may use `.env` files, shell variables, test fixtures, or mounted local files, but it must honor the same canonical names, types, and validation rules as Kubernetes.

Production code must not contain a hidden alternate configuration path that changes behavior only because Kubernetes is absent.

Test-only endpoints, prompts, and credentials must be unmistakably non-production and must not become silent production fallbacks.

### AK.10 Acceptance and Static Checks

Acceptance must prove:

- production service URLs are not hard-coded in application logic;
- secrets are sourced from Secrets rather than plain manifest values or ConfigMaps;
- prompts and large policy assets are loaded from governed mounted configuration;
- missing required configuration prevents startup or work acceptance;
- malformed values fail with a specific diagnostic;
- configuration changes create a new effective revision and activate through the declared rollout contract;
- model and workflow outputs retain the relevant configuration, prompt, and policy identity;
- compatibility aliases resolve to one canonical source and have a retirement plan.

Repositories should include deterministic checks for:

- known cluster-domain URLs embedded in source code;
- production credentials or connection strings in manifests;
- large prompt bodies embedded in application modules;
- undocumented environment variables;
- ConfigMap data that appears secret-bearing;
- configuration variables read by code but absent from deployment manifests or configuration inventory.

### AK.11 Exceptions

Hard-coded values are acceptable when they are true code constants rather than deployment configuration.

Examples may include:

- enum values;
- protocol constants;
- schema field names;
- invariant bounds that are intentionally non-configurable;
- deterministic test fixtures isolated from production paths.

Any production exception must be justified by an ADR that states:

- why externalization would reduce correctness or safety;
- why the value is not environment-specific;
- who owns the decision;
- the revisit trigger.

### AK.12 Forbidden Runtime-Configuration Outcomes

```text
Production endpoint or model URL
+ embedded in application code

Credential or private connection string
+ plain Deployment value or ConfigMap entry

Prompt or policy changes
+ require an unrelated application rebuild

Required mounted prompt missing
+ application silently uses a baked-in fallback

Configuration value malformed
+ application coerces it silently

ConfigMap or Secret changes
+ no rollout, reload, or active-revision evidence

Safety or authority invariant
+ bypassable through an undocumented environment variable

Multiple aliases for one setting
+ different sources or no retirement trigger

Model or workflow result
+ configuration and prompt identity cannot be reconstructed
```

---

## AL. Build and Delivery Acceleration Contract

### AL.1 Governing Principle

Build and deployment feedback time is an architectural quality.

A system that requires excessive time to install dependencies, compile, test, build images, push artifacts, or roll out a small change discourages narrow slices, slows correction, increases batch size, and makes live acceptance less frequent. The result is not merely developer inconvenience. It weakens the framework's ability to build safely and iteratively.

The governing rule is:

```text
Fast feedback
+ reproducible artifacts
+ immutable deployment identity
→ safe delivery acceleration
```

Never:

```text
Speed
→ hidden cache dependence
→ skipped correctness
→ uncertain deployed artifact
```

Every substantial project must define how it will keep its build-test-deploy loop proportionate to the narrowness of the change.

### AL.2 Required Delivery Baseline

Before optimizing, capture a representative baseline for:

- dependency resolution or restoration;
- code generation;
- compilation or transpilation;
- unit and component tests;
- application packaging;
- container image assembly;
- image push;
- manifest application;
- workload rollout;
- readiness and first successful request;
- total change-to-live-acceptance time.

Record both:

```text
Cold path
→ no reusable local build state

Warm path
→ valid reusable dependency and build cache
```

The baseline must include:

- elapsed time per phase;
- CPU and memory utilization where useful;
- cache hit or miss status;
- bytes transferred;
- artifact and image identity;
- changed components;
- whether the run was local, CI, or deployment-hosted.

Instrument before optimizing. A single total duration is insufficient when the build graph, dependency restore, image assembly, registry transfer, and rollout are separate failure and latency domains.

### AL.3 Build Graph and Parallelism

The build system must understand the actual dependency graph.

Required defaults:

- independent packages and stages execute concurrently;
- concurrency is bounded by available compute and workload safety;
- affected components are derived from source and dependency changes rather than a handwritten sequence;
- one slow package must not force unrelated packages into serial execution;
- the graph remains inspectable and deterministic;
- task ordering exists only where a real dependency requires it.

Representative transition:

```text
Hand-maintained serial build chain
→ dependency-aware task graph
→ bounded parallel execution
```

A high-core build host remaining mostly idle during compilation is an architectural smell, not proof that the workload is inherently slow.

### AL.4 Dependency and Layer Reuse

Dependencies and application source must be separated so that unchanged expensive work can be reused safely.

Recommended pattern:

```text
Lockfile + toolchain identity
→ immutable dependency layer or dependency image

Application source revision
→ application build layer

Runtime configuration
→ Deployment, Secret, or ConfigMap
```

The dependency artifact should be keyed by all inputs that can change its result, including as applicable:

- package-manager lockfile;
- language and runtime version;
- platform and architecture;
- build-tool version;
- dependency-related build arguments;
- native-system dependencies.

Registry-backed reuse is preferred when multiple builders or deployment hosts need the same artifact. Local cache may accelerate a developer loop, but it must not be the only path to a reproducible build.

Changing application source should not reinstall unchanged dependencies. Changing a prompt, policy, endpoint, feature flag, or environment-specific value should not rebuild the application when the Runtime Configuration Contract says Kubernetes owns that value.

### AL.5 Scope-Aware Build and Test

The delivery system should execute only the work required by the change, while preserving mandatory cross-cutting checks.

Define:

- how changed components are detected;
- which dependent packages must also build or test;
- which repository-wide checks always run;
- when a full clean build is required;
- how generated artifacts and schema changes expand the affected set;
- how uncertainty falls back safely to a broader build.

Required principle:

```text
Known affected graph
→ targeted build and test

Unknown or unsafe impact
→ broaden deliberately
```

Targeting must not skip semantic acceptance, migration checks, security checks, or contract tests that are load-bearing for the changed capability.

### AL.6 Reproducibility and Cache Safety

Acceleration is acceptable only when the same declared inputs produce the same governed artifact.

Every build path must define:

- immutable source revision;
- dependency identity;
- toolchain identity;
- build configuration identity;
- generated artifact identity;
- image digest;
- cache key and invalidation inputs;
- clean-build verification;
- cache corruption recovery.

Required rules:

- a cache hit is evidence of input identity, not merely the presence of a directory;
- stale or ambiguous cache entries fail closed to rebuild;
- the project retains a deterministic clean-build path;
- CI periodically proves the clean path even when normal work uses warm reuse;
- build acceleration must not depend on undocumented files on one host;
- artifacts must not be mutated after identity is assigned.

### AL.7 Container Image and Deployment Contract

Build once and deploy the same immutable artifact.

Required behavior:

```text
Source revision
→ image build
→ immutable digest
→ registry
→ deployment references or resolves intended digest
→ rollout verifies active digest
```

The delivery system must define:

- image naming and tagging;
- digest capture;
- push retry behavior;
- prevention of accidental stale-tag deployment;
- manifest and image alignment;
- rollout readiness;
- active-digest verification;
- rollback behavior;
- partial deployment recovery.

A successful compile, image build, or registry push is not a successful deployment. The active workload must prove that it is running the intended immutable digest and effective runtime configuration revision.

### AL.8 Build and Delivery Budgets

Each project must set explicit budgets appropriate to its size and infrastructure for:

- warm build;
- cold build;
- targeted test;
- full test;
- image build and push;
- rollout to ready;
- total narrow-change feedback loop.

The framework does not impose one universal duration. It requires an explicit budget and a regression policy.

The policy must state:

- warning threshold;
- blocking threshold;
- who owns investigation;
- what evidence is required before accepting a regression;
- whether the regression is temporary and its removal trigger;
- the ADR required for a deliberate long-term tradeoff.

A project that once required approximately sixteen minutes to build a primary application should preserve the architectural lesson, not the exact number: unexplained multi-minute regressions in a narrow change loop must be measured, decomposed, and corrected rather than normalized.

### AL.9 Required Build Acceleration Plan

Every System Architecture and substantial implementation program must define:

```text
Current baseline
Target budgets
Build graph
Concurrency model
Dependency-cache identity
Container-layer strategy
Affected-component detection
Cold-build path
Registry-backed reuse
Image-digest verification
Configuration-only change path
Timing and cache observability
Regression policy
Owners
Known constraints
```

For a monorepo or multi-service repository, also define which components can build independently and which events require a broader rebuild.

### AL.10 Acceptance

Acceptance must prove at least one representative narrow change through both the warm and clean paths.

Required evidence includes:

- the changed component and affected graph;
- phase timings;
- concurrency evidence;
- dependency-cache identity and reuse;
- clean-build success;
- resulting immutable image digest;
- deployed active digest;
- effective runtime configuration revision;
- readiness and live acceptance result;
- comparison with the declared budget.

Where acceleration mechanisms are introduced, acceptance must also prove that:

- changing the lockfile invalidates dependency reuse;
- changing only application source reuses valid dependencies;
- changing only ConfigMap-backed prompts or policy follows the declared configuration rollout path without an unrelated application rebuild;
- a stale tag or mismatched digest cannot silently deploy;
- cache loss degrades to a correct clean build rather than a broken delivery path.

### AL.11 Forbidden Build and Delivery Outcomes

```text
Independent build stages
+ forced serial execution without a real dependency

Application-only change
+ full dependency restoration on every build

Single-package change
+ unrelated repository-wide rebuild without stated reason

Cache reused
+ cache inputs cannot be reconstructed

Warm build succeeds
+ clean environment cannot reproduce artifact

Prompt, endpoint, or environment change
+ application rebuild required despite Kubernetes ownership

Image tag updated
+ active immutable digest unknown

Build succeeds
+ deployment runs a prior image digest

Build acceleration enabled
+ semantic, security, migration, or acceptance checks silently skipped

Build duration regresses materially
+ no phase evidence, owner, disposition, or revisit trigger
```

---



## AM. Chain Delivery Visibility and End-to-End Progress Contract

### AM.1 Governing Principle

Component completion is not chain completion.

A multi-point technical design or implementation plan can show many locally completed items while the real operator workflow remains blocked near its beginning. Records may exist without writers, workers without consumers, APIs without surfaces, surfaces without canonical write effects, or downstream components without a live upstream path.

The governing rule is:

```text
Locally complete components
+ unproven or disconnected handoffs
→ incomplete delivery chain
```

Never:

```text
12 of 15 implementation points marked done
→ product reported as 80% complete
```

Every substantial workflow must expose the furthest contiguous point reached by a realistic input through the production path.

### AM.2 Delivery Chain Definition

A delivery chain is the ordered or branched path from a real ingress or operator action to the declared operator outcome.

It includes both:

- **nodes** — capabilities, records, workers, decisions, projections, and surfaces;
- **edges** — the handoffs, contracts, triggers, writes, reads, and acknowledgements connecting those nodes.

Example:

```text
Source import
→ preserved source artifact
→ parsed blocks
→ project-mapping candidates
→ operator adjudication
→ canonical project records
→ current project read model
→ operator surface
→ accepted operator outcome
```

A node may be complete while its incoming or outgoing edge is absent. Both nodes and edges require independent status and evidence.

### AM.3 Required Chain Delivery Map

Every substantial specification, TDD, and multi-PR implementation program must maintain a Chain Delivery Map.

The map must identify:

```text
Chain point or handoff name
Canonical ID
Owning application subsystem
Producer and consumer subsystem for cross-boundary edges
Type: node or edge
Operator-relevant outcome
Upstream dependency
Downstream consumer
Input contract
Output contract
Owner
Specification section
Planned pull request title
Specification state
Implementation state
Connection state
Deployment state
Evidence state
Current blocker
Next chain-closing action
Deployed artifact or configuration revision
Acceptance evidence
Last verified time
```

The map must be understandable without reconstructing status from commit history, chat transcripts, issue comments, or merged pull requests.

### AM.4 Independent Progress Axes

Do not overload one `status` value with design, code, integration, deployment, and acceptance meaning.

Track at least these independent axes for every load-bearing node and edge:

#### Specification state

```text
missing
draft
accepted
superseded
```

#### Implementation state

```text
not_started
in_progress
merged
rework_required
```

#### Connection state

```text
unconnected
wired
contract_verified
broken
```

#### Deployment state

```text
not_deployed
deployed
healthy
unhealthy
unknown
```

#### Evidence state

```text
none
component_fixture_pass
chain_fixture_pass
live_path_pass
operator_accepted
failed
```

A merged component with `connectionState=unconnected` and `evidenceState=component_fixture_pass` has not advanced the live chain.

### AM.5 Live Frontier and Disconnected Islands

Every active delivery chain must report:

- **live frontier** — the furthest contiguous point reached from realistic ingress through the deployed production path;
- **fixture frontier** — the furthest contiguous point reached using synthetic or fixture input;
- **operator-acceptance frontier** — the furthest point accepted through the real operator surface;
- **blocked handoff** — the first load-bearing edge preventing the live frontier from advancing;
- **disconnected islands** — implemented downstream capabilities that cannot yet be reached through the contiguous chain;
- **next chain-closing action** — the smallest action that advances the live frontier or removes the first blocker.

Required rule:

```text
Downstream component implemented
+ no contiguous upstream live path
→ report as disconnected island
```

Do not hide islands inside an aggregate completion percentage.

### AM.6 Handoff Contract

Every load-bearing edge must define:

- trigger;
- producer;
- consumer;
- records read;
- records written;
- input schema and version;
- output schema and version;
- identity and idempotency key;
- ordering assumptions;
- retry and timeout behavior;
- stale-result behavior;
- failure routing;
- observability signal;
- fixture proof;
- live-path proof;
- operator-visible consequence.

A handoff is not complete because both adjacent components exist.

Required test:

```text
Producer exists
+ consumer exists
+ no verified transfer of governed data
→ handoff incomplete
```

### AM.7 TDD and Pull Request Progress Rules

For a multi-point TDD or implementation plan:

- each point must map to one or more Chain Delivery Map nodes or edges;
- each pull request must state which chain points it changes;
- each pull request must state whether the live frontier advances;
- if the live frontier does not advance, the pull request must state which prerequisite, island, recovery path, or observability capability it establishes;
- merge status must not automatically change connection, deployment, or evidence status;
- chain status must be updated when the runtime is deployed and verified, not merely when code merges;
- the TDD must identify the current blocked handoff and next chain-closing action at all times.

Required TDD status header:

```text
Planned chain points: 15
Locally implemented: 11
Contiguous chain-fixture proven: 8
Contiguous live-path proven: 5
Operator accepted: 4
Live frontier: <named chain point>
First blocked handoff: <producer> → <consumer>
Disconnected islands: <named downstream capabilities>
Next chain-closing action: <smallest concrete action>
```

Counts are supporting metadata. The named frontier and blocked handoff are the governing progress signal.

### AM.8 Progress Reporting

Delivery reporting must answer:

- Where does a realistic subject stop today?
- Why does it stop there?
- Which exact handoff is missing, failing, stale, or unproven?
- Which downstream capabilities are complete but unreachable?
- What is the smallest action that advances the operator-visible chain?
- Which steps are proven only by fixtures?
- Which steps are deployed but not live-proven?
- Which steps have been accepted through the operator surface?

A progress report must not lead with:

- story points completed;
- pull requests merged;
- files changed;
- components built;
- test-count totals;
- percent complete calculated from checklist items.

Those measures may be included, but they cannot substitute for chain position.

### AM.9 Chain Completion and Acceptance

A delivery chain is complete only when:

- every load-bearing node is implemented;
- every load-bearing edge is connected and contract-verified;
- one realistic subject traverses the complete deployed production path;
- canonical writes and current read models align;
- failure and recovery behavior are exercised at required seams;
- operator surfaces display the resulting current truth;
- the operator can perform the declared final action;
- the declared operator outcome is accepted;
- no disconnected island is being represented as part of the completed path.

Component, integration, deployment, and operator acceptance must be reported separately.

### AM.10 Chain Delivery Smells

The Architecture Smells Seed must include:

- **Checklist Progress Masquerades as Chain Progress** — completed TDD points or merged pull requests are reported as overall progress without a contiguous live-path measure.
- **Completed Component Island** — a downstream capability is implemented but has no verified production path from its upstream source.
- **Handoff Without Owner** — the producer and consumer exist, but no owner is accountable for the edge between them.
- **No Named Live Frontier** — the team cannot state where a realistic subject stops in the current deployed chain.
- **Fixture Frontier Presented as Live Frontier** — synthetic traversal is reported as if a real subject passed through production.
- **Merge Advances Status Without Runtime Proof** — merging code automatically marks a chain point connected, deployed, or accepted.
- **Last Mile Deferred by Implication** — canonical records and backend services exist while the operator surface or write effect remains outside the tracked chain.
- **Percent Complete from Unequal Points** — progress is calculated from checklist counts even though points differ materially in dependency, risk, and operator value.
- **Cross-PR Handoff Gap** — adjacent pull requests each complete their local scope while neither proves the connecting contract.
- **Unknown Next Chain-Closing Action** — work continues on downstream components while the first blocked handoff remains unnamed.

### AM.11 Forbidden Chain Delivery Outcomes

```text
Component tests pass
+ component reported as chain-complete without handoff proof

Pull request merged
+ deployment or live-path state automatically marked complete

Downstream capability exists
+ progress report hides that no realistic input can reach it

Fixture reaches terminal stage
+ live chain represented as proven

Fifteen-point TDD
+ no named live frontier, blocked handoff, or next chain-closing action

Producer and consumer implemented
+ nobody owns or tests the edge

Operator surface absent
+ backend chain represented as product-complete

Checklist percentage high
+ operator outcome still blocked near ingress
```


## AN. Git-Tracked Slice, TDD, and Pull Request Delivery Record Contract

### AN.1 Governing Principle

A delivery chain needs both current status and durable history.

Chat transcripts, pull request descriptions, issue comments, CI logs, and commit diffs are useful working evidence, but they are not a sufficient canonical written record of what a delivery stage intended, changed, proved, failed to prove, or left behind.

Every substantial slice, TDD stage, and pull request must leave a descriptive report in Git.

The governing distinction is:

```text
Architecture specification
→ intended governed design

Chain Delivery Register
→ current delivery position

Git-tracked delivery reports
→ preserved as-built and as-proven history
```

Required rule:

```text
Stage completed
+ no durable Git-tracked delivery report
→ delivery history incomplete
```

The report is not ceremony added after the work. It is part of the work product.

### AN.2 Canonical Delivery Record

The delivery report on the accepted default branch is the canonical written record for that slice, TDD stage, or pull request.

Git history preserves how the report changed as the work moved through implementation, deployment, live proof, and acceptance.

Supporting systems may contain richer transient evidence:

- pull request discussion;
- CI logs;
- deployment logs;
- screenshots;
- runtime traces;
- issue comments;
- operator chat.

The canonical report must summarize the load-bearing conclusions and link to supporting evidence where durable links exist. It must remain understandable if those external systems or conversations are unavailable later.

Do not require a future engineer to reconstruct delivery truth from:

- commit archaeology;
- a sequence of chat messages;
- closed pull requests;
- ephemeral CI output;
- tribal memory;
- screenshots with no explanation.

### AN.3 Required Report Types

#### Slice delivery report

Every named implementation slice must have one slice report that records:

- the slice outcome;
- included and excluded scope;
- parent architecture and feature specification;
- TDDs and pull requests included;
- chain frontier before the slice;
- intended frontier after the slice;
- actual frontier achieved;
- acceptance result;
- unresolved gaps;
- deferred work;
- stop-rule disposition;
- the final End-State Delivery Snapshot.

The slice report is the roll-up record for the complete narrow delivery unit.

#### TDD stage report

Every substantial TDD and every independently executed TDD stage must have a report that records:

- the exact stage outcome;
- planned chain nodes and handoffs;
- actual implementation and integration state;
- stage-level test and acceptance evidence;
- deviations from the TDD;
- failures and flyswatting encountered;
- effects on downstream stages;
- first blocked handoff;
- next chain-closing action;
- the stage End-State Delivery Snapshot.

A multi-stage TDD must not rely on a single final summary that hides where intermediate stages diverged from plan.

#### Pull request delivery report

Every substantial implementation pull request must create or update a pull request delivery report containing:

- the descriptive pull request title and canonical delivery-record ID;
- pull request number as metadata, never identity;
- parent slice, TDD, specification, and ADRs;
- exact capability and outcome delivered;
- files, components, records, surfaces, and handoffs materially changed;
- chain state before and after;
- implementation evidence;
- deployment and live-path evidence when available;
- known deviations, gaps, and follow-up work;
- the pull request End-State Delivery Snapshot.

Small mechanical, dependency-only, or editorial pull requests may use a compact report, but they may not disappear from the parent slice or TDD record.

### AN.4 Report Lifecycle

A delivery report should be created when the stage begins and updated as evidence becomes available.

Suggested report states:

```text
planned
implemented
merged_pending_deployment
deployed_pending_live_proof
live_proven
operator_accepted
closed_with_gap
superseded
```

A pull request may merge before deployment or operator acceptance. The report must state that honestly.

Never:

```text
Pull request merged
→ report silently claims deployed or accepted
```

A report may be updated in a later documentation or acceptance commit after deployment. The final state must be backed by the evidence required for that state.

### AN.5 Required Delivery Report Fields

Every report must contain, as applicable:

```text
Canonical report title
Canonical report ID
Report type: slice | tdd_stage | pull_request
Report state
Architecture version
Document/report revision
Parent project, feature specification, slice, and TDD
Owning application subsystem and participating subsystems
Subsystem boundaries, contracts, and detail pages changed
Descriptive pull request title and number
Branch, merge commit, and implementation commit range
Author or accountable owner
Created, merged, deployed, verified, and accepted times
Operator outcome
Planned scope
Actual delivered scope
Explicit non-goals
Chain frontier before
Chain frontier after
Nodes and handoffs changed
First blocked handoff
Disconnected islands created or removed
Next chain-closing action
Canonical record and schema changes
Runtime configuration, Secret, ConfigMap, prompt, or policy changes
Resource ownership classifications and canonical names changed
Product-owned, shared-platform, foreign-application, and historical resources affected
Implementation substrate or image provenance changed
Migration and compatibility effects
Build and delivery impact
Implementation summary
Tests and fixture evidence
Deployment artifact and immutable image digest
Effective configuration and prompt/policy revisions
Live-path evidence
Operator-surface evidence
Recovery or rollback evidence
Security and data-egress effects
Deviations from specification or TDD
ADRs created or changed
Failures, unexpected behavior, and flyswatting
Feature Memory Ledger changes
Architecture Smells Seed changes or dispositions
Remaining gaps and risks
Acceptance result
Stop-rule disposition
End-State Delivery Snapshot
Durable evidence links
```

Fields that do not apply should be marked `not_applicable` with a short reason rather than silently omitted when ambiguity would result.

### AN.6 As-Planned Versus As-Built

Every final report must distinguish:

- what the specification or TDD planned;
- what the implementation actually built;
- what was deployed;
- what was live-proven;
- what the operator accepted;
- what changed or remained incomplete.

Required rule:

```text
Plan copied into final report
+ no as-built comparison
→ report incomplete
```

Unexpected flyswatting is load-bearing architecture evidence. The report must capture meaningful failures, their causes, the fix, and whether they created:

- a new invariant;
- a forbidden outcome;
- an Architecture Smell;
- an FML entry;
- a follow-up specification;
- a framework lesson.

### AN.7 Relationship to Chain Delivery Visibility

The Chain Delivery Register is the canonical current projection of delivery status.

Slice, TDD, and pull request reports are historical evidence sources for that projection.

Every report must either:

- update one or more Chain Delivery Map nodes or edges; or
- explicitly state that it does not advance or alter the chain and explain its supporting purpose.

Every report must state whether it:

- advances the fixture frontier;
- advances the live frontier;
- advances the operator-acceptance frontier;
- creates a disconnected island;
- removes a disconnected island;
- closes the first blocked handoff;
- establishes only a prerequisite, observability seam, recovery path, or delivery capability.

### AN.8 Naming and Repository Placement

Delivery-report names must follow the same outcome-bearing naming contract as specifications and pull requests.

Recommended layout:

```text
docs/delivery/
  <feature-or-program-id>/
    slice-reports/
      <descriptive-slice-id>-delivery-report.md
    tdd-reports/
      <descriptive-tdd-stage-id>-delivery-report.md
    pr-reports/
      <descriptive-capability-outcome-id>-delivery-report.md
```

Good:

```text
preserve-logseq-source-artifacts-delivery-report.md
map-imported-blocks-to-canonical-projects-delivery-report.md
expose-import-conflicts-for-operator-review-delivery-report.md
```

Bad:

```text
slice-1-report.md
tdd-4.md
pr-7-report.md
final-report-v2.md
```

Sequence numbers, ticket IDs, and pull request numbers may appear in metadata. They must not be the report identity.

### AN.9 Report Completion Gates

A stage report is complete only when:

- its claimed state matches available evidence;
- as-planned and as-built behavior are distinguished;
- the chain effect is explicit;
- deviations and failures are recorded;
- deployed artifact and configuration identity are captured when applicable;
- live and operator evidence are not inferred from component tests;
- remaining gaps and the next chain-closing action are explicit;
- required FML, Smells Seed, ADR, runbook, or specification updates are linked;
- the report is committed to Git under a descriptive name;
- the parent slice or TDD report links to it;
- the report ends with a complete End-State Delivery Snapshot.

A slice cannot close merely because all planned pull requests merged. Its slice report must reconcile the intended outcome against actual chain and operator acceptance.

### AN.10 Delivery Record Smells

The Architecture Smells Seed must include:

- **Delivery by Conversation Memory** — important stage status, decisions, or failure history exist only in chat or tribal memory.
- **Pull Request Body as Only Record** — the repository contains no durable delivery report independent of the code-hosting platform.
- **Plan Repeated as As-Built** — the final report restates intended work without documenting actual behavior and deviations.
- **Merge Presented as Deployment** — a report claims runtime completion based only on merge status.
- **Evidence Link Without Durable Summary** — the report points to ephemeral logs or screenshots without preserving the conclusion they prove.
- **Flyswatting Without Institutional Memory** — meaningful failures are fixed but do not update reports, smells, invariants, forbidden outcomes, or future design.
- **Current Register Without Historical Record** — present chain status exists, but no Git-tracked stage history explains how it was reached.
- **Report Named by Sequence** — the record cannot be understood without knowing the order or surrounding conversation.
- **Parent Report Missing Child Records** — a slice or TDD roll-up omits implementation reports that materially affected its outcome.
- **Report Closed with Unknown Next Step** — the stage is incomplete, but the first blocked handoff and next chain-closing action are absent.

### AN.11 Forbidden Delivery Record Outcomes

```text
Substantial pull request merged
+ no Git-tracked delivery report

TDD stage reported complete
+ no as-built, deployment, or evidence record

Slice closed
+ actual chain frontier not reconciled against intended frontier

Report says accepted
+ no operator-acceptance evidence

Runtime behavior diverges from specification
+ deviation omitted from delivery report

Meaningful production failure fixed
+ cause and institutional lesson disappear with the chat thread

Delivery report exists
+ filename is only a sequence number

External evidence link expires
+ repository no longer explains what was proven

Substantial delivery report closes
+ no holistic implemented-versus-unimplemented snapshot
```

---


## AO. Delivery Scope Hierarchy and End-State Delivery Snapshot Contract

### AO.1 Governing Principle

Large projects need a stable scope hierarchy and a single closing summary for every material delivery stage.

The hierarchy exists to answer:

```text
What operator capability are we building?
How is it decomposed?
Which narrow increment is being delivered now?
Which technical design and pull requests implement that increment?
What, holistically, exists at the end of this stage—and what still does not?
```

The hierarchy must not become a substitute for the Chain Delivery Map.

A hierarchy explains **scope and decomposition**. The Chain Delivery Map explains **runtime connection and live progress**.

Required rule:

```text
Many completed tasks or pull requests
+ no clear Epic, Feature, Slice, and end-state relationship
→ delivery position not understandable
```

### AO.2 Canonical Delivery Hierarchy

Use the following hierarchy when the project is large enough to require decomposition:

```text
Project or Product
    ↓
Epic
    ↓
Feature
    ↓
Slice
```

TDDs, pull requests, and tasks are execution artifacts beneath or across slices. They are not interchangeable with product scope.

#### Project or Product

The durable product boundary and primary operator domain.

Example:

```text
Atlas
```

#### Epic

A coherent, multi-feature operator capability or product outcome that is too large to implement as one feature.

An Epic must define:

- one governing operator outcome;
- the features required to realize that outcome;
- the end-to-end chain it owns;
- architecture-version and release expectations;
- explicit exclusions;
- completion criteria that cannot be satisfied by component count alone.

Good Epic examples:

```text
Import external project history into governed Atlas memory
Reconstruct canonical project state from AI conversation exports
Operate architecture evolution and delivery traceability
```

Bad Epic examples:

```text
Backend work
Phase 2
Miscellaneous integrations
PR cleanup
```

An Epic is optional when a project or release contains only one coherent feature. Do not create empty hierarchy for appearance.

#### Feature

The smallest durable operator-visible capability that has its own governed semantics, acceptance outcome, and feature specification.

A Feature must:

- answer a specific operator question or enable a specific operator action;
- have one canonical specification;
- define canonical objects, workflow, surfaces, and acceptance;
- belong to one Epic or explicitly belong directly to the Project when no Epic is necessary;
- be deliverable through one or more narrow slices.

A technical component, service, database collection, prompt, endpoint, or worker is not automatically a Feature.

Required test:

```text
Item has no independent operator outcome
→ not a Feature
```

#### Slice

A narrow, vertically meaningful delivery increment that advances the contiguous chain toward the Feature outcome.

A Slice should:

- cross the minimum necessary layers;
- advance a named fixture, live, or operator-acceptance frontier;
- end in a demonstrable state;
- have an explicit stop rule;
- produce a Git-tracked slice delivery report;
- avoid creating disconnected component islands unless the prerequisite is named and intentionally accepted.

A horizontal layer such as “build all schemas” or “add all endpoints” is not automatically a valid slice unless it closes or materially enables a named chain handoff.

#### TDD

A Technical Design Document defines how one slice, one difficult technical capability, or a bounded set of chain nodes and handoffs will be implemented.

A TDD is not a product hierarchy level.

It may:

- implement one slice;
- span multiple pull requests;
- cover a cross-cutting technical prerequisite used by several slices;
- be divided into named stages when execution and proof are substantial.

Every TDD must identify the Epic, Feature, and Slice it serves—or explicitly state that it is a cross-cutting platform TDD and name every affected Feature and chain.

#### Pull Request

A pull request is a reviewable integration unit.

It may implement part or all of a slice, but merge status must never be treated as Feature or Slice completion.

#### Task

A task is an execution item. Tasks may be tracked in any appropriate system, but task completion does not define product progress.

### AO.3 Hierarchy Traceability

Every substantial artifact must declare its owning subsystem and parent delivery scope:

```text
Owning application subsystem
Project or Product
Epic, or direct-to-project reason
Feature
Slice
TDD or TDD stage
Pull request
```

Each child must link upward. Each parent must be able to enumerate its load-bearing children. The owning subsystem is a traceability dimension rather than an additional delivery hierarchy level.

Required rule:

```text
Pull request or TDD cannot identify the Feature and Slice it serves
→ orphaned delivery work
```

The hierarchy must remain outcome-bearing and descriptively named. Sequence numbers may appear as metadata only.

### AO.4 Epic and Feature Completion

An Epic is complete only when:

- every required Feature is operator-accepted or explicitly removed through a governed scope decision;
- the Epic’s end-to-end live chain is contiguous;
- no load-bearing handoff remains hidden;
- unresolved deferred work is recorded in FML;
- the final Epic delivery report contains an End-State Delivery Snapshot;
- the operator outcome is achieved honestly.

A Feature is complete only when:

- its required slices are reconciled;
- its canonical semantics and surfaces are implemented;
- its live path is proven;
- the operator outcome is accepted;
- known broken, degraded, omitted, or deferred behavior is explicit;
- the final Feature or closing Slice report contains an End-State Delivery Snapshot.

Never:

```text
All planned pull requests merged
→ Feature complete

All Features individually implemented
+ Epic handoffs unproven
→ Epic complete
```

### AO.5 Mandatory End-State Delivery Snapshot

Every substantial Slice, TDD stage, TDD, pull request, Feature closure, and Epic closure report must end with one section named exactly:

```text
End-State Delivery Snapshot
```

This is the single holistic point-in-time summary of the stage.

It must state what exists, what is connected, what is proven, what is broken, and what does not exist.

The snapshot is canonical for the state of that delivery unit at the time the report closes.

The **Chain Delivery Register remains the canonical current project status** after later work advances the system.

Required distinction:

```text
End-State Delivery Snapshot
→ immutable historical closing state of one delivery unit

Chain Delivery Register
→ current reconciled delivery state across the project
```

### AO.6 Required Snapshot Fields

Every End-State Delivery Snapshot must contain:

```text
Snapshot as of
Project or Product
Epic
Feature
Slice
TDD or TDD stage
Pull request, where applicable
Architecture version
Delivery report state
Operator outcome
Overall delivery disposition

Implemented and live-proven
Implemented and connected but not live-proven
Implemented but not connected
Implemented but not deployed
Deployed but degraded or broken
Not implemented
Explicitly deferred
Removed from scope

Fixture frontier
Live frontier
Operator-acceptance frontier
First blocked handoff
Disconnected islands
Known defects and degraded modes
Canonical data or migration state
Operator surfaces available
Operator surfaces missing or incomplete
Acceptance result
Stop-rule disposition
Next chain-closing action
Durable evidence references
```

Allowed overall delivery dispositions:

```text
not_started
implemented_islands_only
fixture_chain_proven
partially_live
live_chain_proven
operator_accepted
closed_with_gap
degraded
superseded
```

The disposition is a summary signal. It does not replace the explicit implemented and unimplemented lists.

### AO.7 Snapshot Truth Rules

The snapshot must obey:

```text
Not mentioned
≠ implemented

Code merged
≠ deployed

Deployed
≠ connected

Connected
≠ live-proven

Live-proven
≠ operator-accepted

Deferred
≠ forgotten

Known broken
≠ complete with caveat hidden elsewhere
```

Every material capability within the report’s scope must appear under exactly one current disposition in the snapshot.

When a capability is only partially implemented, name the implemented and missing portions separately.

Do not use completion percentages as the primary summary.

### AO.8 Snapshot Reconciliation

Before a report closes:

1. reconcile the original planned scope;
2. inspect the actual implementation;
3. inspect deployment state;
4. inspect fixture and live evidence;
5. inspect operator-surface behavior;
6. list every omitted, broken, degraded, or deferred item;
7. update the Chain Delivery Register;
8. update parent Feature, Epic, FML, Smells Seed, ADR, or runbook records as required;
9. write the End-State Delivery Snapshot last.

The snapshot must not be copied from the planning section or generated solely from issue status.

### AO.9 Epic and Feature Register

Every substantial project should maintain a Git-tracked Epic and Feature Register.

The register is the canonical scope-decomposition record, not the current chain-status record.

For each Epic and Feature it records:

```text
Canonical title and ID
Parent Project or Epic
Operator outcome
Architecture version introduced
Target product release
Lifecycle state
Child Features or Slices
Canonical specification path
Chain Delivery Map reference
Current closing-report reference
Scope additions and removals
FML references
Owner
```

Suggested lifecycle states:

```text
proposed
architecting
accepted
in_delivery
partially_live
operator_accepted
closed_with_gap
deferred
canceled
superseded
```

The register must link to the Chain Delivery Register rather than duplicate detailed node and handoff status.

### AO.10 Delivery Hierarchy and Snapshot Smells

The Architecture Smells Seed must include:

- **Epic as Grab Bag** — unrelated work is grouped under one Epic with no coherent operator outcome.
- **Feature Without Operator Outcome** — a service, schema, endpoint, model, or worker is treated as a Feature solely because it is substantial work.
- **Slice as Horizontal Layer** — a slice completes one technical layer but does not advance a meaningful chain frontier.
- **TDD Treated as Product Scope** — TDD stages become the only view of delivery and obscure the Feature outcome.
- **Orphaned Pull Request** — a substantial pull request cannot identify the Feature and Slice it serves.
- **Hierarchy Without Traceability** — parents cannot enumerate load-bearing children or children cannot identify parents.
- **Report Ends Without Holistic Snapshot** — a delivery report records implementation detail but provides no central account of what exists and what does not.
- **Snapshot Copies the Plan** — the closing snapshot repeats intended scope without reconciling as-built and as-proven reality.
- **Partial Capability Presented as Whole** — a capability with missing layers or handoffs appears only under implemented.
- **Historical Snapshot Presented as Current** — an old stage snapshot is treated as current project status instead of reconciling through the Chain Delivery Register.
- **Percent Complete Replaces Disposition** — a numeric completion percentage hides the live frontier, missing work, or broken handoffs.

### AO.11 Forbidden Delivery Hierarchy and Snapshot Outcomes

```text
Epic declared complete
+ required Feature operator outcome unaccepted

Feature declared complete
+ live path unproven

Slice declared complete
+ no named chain frontier effect

TDD or pull request delivered
+ no Epic, Feature, or Slice traceability

Substantial delivery report closes
+ no End-State Delivery Snapshot

Snapshot lists implemented
+ capability exists only as disconnected code

Snapshot omits known broken or unimplemented scope

Historical snapshot used as current project truth
+ Chain Delivery Register disagrees
```

---

## AP. Harness Architecture and Documentation Contract

### AP.1 Governing Principle

AI applications depend on harnesses for correctness, evolution, and trust.

A harness is not incidental test scaffolding around the system. It is the governed execution and evidence architecture that proves:

- deterministic contracts still hold;
- model behavior remains semantically acceptable;
- retrieval and evidence assembly remain grounded;
- the complete production chain still traverses;
- retries, stale work, and failure recovery remain safe;
- performance remains within the declared operating envelope;
- the operator can understand and accept the resulting product outcome.

Required rule:

```text
AI behavior, workflow behavior, or operator outcome changes
+ no repeatable harness evidence
→ change not proven
```

A green unit-test suite is not sufficient evidence for an AI-backed product.

### AP.2 Harness Authority and Boundaries

The harness may:

- construct isolated test subjects;
- invoke governed production interfaces;
- observe queues, workers, stores, projections, model calls, and surfaces;
- compare results with deterministic invariants and semantic rubrics;
- capture evidence packages;
- perform bounded cleanup;
- fail a delivery or release gate.

The harness may not:

- become a competing canonical owner;
- redefine product semantics;
- promote fixture output into production truth by implication;
- bypass operator authority;
- use hidden shortcuts and claim production-path proof;
- mutate production canonical truth except through an explicitly governed production-smoke contract;
- conceal skipped, blocked, disabled, or inconclusive gates inside an aggregate success state.

Harness expectations belong in architecture specifications, not only in test code.

### AP.3 Required Harness Classes

Every substantial project must classify which harness classes apply and document why any class is not applicable.

#### Contract and invariant harness

Proves:

- schemas;
- required fields;
- authority precedence;
- state transitions;
- idempotency;
- stale-work rejection;
- duplicate prevention;
- forbidden outcomes;
- deterministic numeric and policy bounds.

#### Workflow and chain harness

Drives a realistic subject through the production chain and proves:

- every named node executes;
- every load-bearing handoff transfers the correct record and identity;
- the fixture, live, and operator-acceptance frontiers are reported separately;
- the first blocked handoff is visible;
- disconnected component islands are not presented as chain completion.

#### Semantic calibration harness

Evaluates whether model output means the right thing.

It should include:

- clear positive cases;
- clear negative cases;
- difficult boundary cases;
- required abstention cases;
- evidence-conflict cases;
- operator-corrected prior failures;
- cases that separate adjacent but materially different classifications;
- expected omissions and forbidden inventions.

#### Retrieval and evidence harness

Proves:

- correct intent routing;
- required live versus memory retrieval;
- source custody;
- exact citation or span attachment;
- freshness behavior;
- conflicting-source handling;
- no unsupported claim promotion;
- honest unavailable and exhausted outcomes.

#### Failure, recovery, and stale-work harness

Injects and proves behavior for:

- model timeout;
- invalid structured output;
- connector failure;
- queue interruption;
- worker restart;
- duplicate delivery;
- lease expiration;
- projection lag or failure;
- stale late result;
- partial canonical write;
- cancellation;
- restart and reconciliation.

#### Import, migration, and replay harness

Proves:

- preserved-source identity;
- repeatable import;
- idempotent re-import;
- mapping correction;
- duplicate and conflict handling;
- migration compatibility;
- rollback or safe forward recovery;
- replay from preserved source under a new model, prompt, policy, or schema.

#### Performance and capacity harness

Measures realistic:

- input and context size;
- retrieval package size;
- output size;
- time to first token;
- decode throughput;
- total request latency;
- queue time;
- concurrency;
- token consumption;
- memory or VRAM use;
- cold and warm behavior;
- cache effects;
- end-to-end workflow latency.

#### Operator acceptance harness

Proves the deployed surface and action path, including:

- current versus history;
- evidence drilldown;
- empty, loading, stale, error, degraded, and unavailable states;
- operator actions and their canonical write effects;
- truthful stop reasons;
- final operator acceptance.

Automation may support this harness, but automation must not erase the need for explicit operator judgment where the product outcome is inherently operator-owned.

### AP.4 Harness Execution Modes

Every harness run must declare exactly one execution mode.

#### Deterministic fixture mode

Uses controlled synthetic or frozen inputs and deterministic substitutes where necessary.

Purpose:

- fast contract checks;
- reproducible state-machine checks;
- known failure injection;
- local and CI execution.

It does not prove live model, live retrieval, or live provider behavior.

#### Recorded replay mode

Reuses preserved model, connector, retrieval, or source responses with exact content identity.

Purpose:

- reproduce defects;
- compare code, prompt, policy, and schema changes;
- run without external availability;
- preserve a stable regression seam.

It does not prove that the current live dependency still behaves the same way.

#### Live isolated mode

Uses the actual deployed model, retrieval, connector, queue, worker, and storage path against isolated harness-owned data.

Purpose:

- prove real integration;
- detect runtime configuration or deployment defects;
- measure current model and infrastructure behavior;
- advance the live-path frontier.

#### Production smoke or shadow mode

Runs a tightly bounded check against production infrastructure or observes production behavior without gaining authority over canonical truth.

It requires:

- explicit authorization;
- defined read and write boundaries;
- unique run identity;
- cleanup behavior;
- audit evidence;
- rate and resource budgets;
- a no-surprise operator contract.

Required rule:

```text
Fixture, recorded replay, live isolated, and production smoke
→ distinct evidence classes
→ never reported as interchangeable
```

### AP.5 Production-Path Fidelity

A harness that claims end-to-end proof must traverse the same load-bearing path as production.

It should use, where applicable:

- the same API or ingress contract;
- the same application-owned `AgentRun` and `AgentAttempt` path;
- the same OpenShell execution profile, sandbox policy, and Supervisor-enforced boundaries;
- the same queue and worker;
- the same state machine;
- the same canonical write path;
- the same projection path;
- the same retrieval and evidence assembler;
- the same model adapter;
- the same operator read model.

Permitted substitutions must occur only at an explicitly named external boundary and must be visible in the run manifest.

Examples of invalid proof:

```text
Direct database insert
+ worker normally creates the record
→ worker path not proven

Calling an internal model helper
+ production uses queue, lease, retry, and persistence
→ production workflow not proven

Fixture-specific endpoint
+ normal operator cannot invoke it
→ operator path not proven
```

A test-only capability must not remain reachable as an undocumented production backdoor.

### AP.6 Harness Case and Fixture Contract

Every durable harness case must define:

```text
Case name
Canonical case ID
Purpose
Harness class
Execution modes supported
Parent Epic, Feature, Slice, and specification
Owning application subsystem and participating subsystem contracts
Input or preserved source references
Setup requirements
Expected deterministic invariants
Expected semantic disposition or allowed range
Required evidence
Forbidden outcomes
Performance or resource budgets where applicable
Expected chain frontier
Cleanup behavior
Known limitations
Owner
Case-pack version introduced
```

Case identity must survive filename or repository movement.

Fixtures must be classified as:

```text
synthetic
frozen_realistic
recorded_live
operator_accepted_reference
production_smoke
```

The classification must be visible in every result.

Large source artifacts may be stored outside Git, but Git must retain:

- the artifact reference;
- content hash;
- source type;
- custody and access rules;
- creation or capture time;
- expected availability;
- rebuild or replacement behavior.

### AP.7 Deterministic Assertions and Semantic Evaluation

The harness must separate exact deterministic assertions from probabilistic or semantic evaluation.

Use exact assertions for:

- schema validity;
- state transitions;
- ownership;
- idempotency;
- required citations;
- source byte or span custody;
- numeric bounds;
- stale-work protection;
- canonical write effects;
- forbidden outcomes.

Use bounded semantic rubrics for:

- classification quality;
- completeness;
- contradiction handling;
- evidence use;
- abstention;
- nuance;
- operator usefulness;
- unsupported inference;
- calibrated uncertainty.

Do not use byte-for-byte prose equality as the normal semantic quality gate.

A semantic case should define what must be present, what must not be present, what may vary, and what requires human adjudication.

Repeated sampling should be used only when model variance is material to the operator outcome. It must not become ritualized cost without a declared decision rule.

### AP.8 Harness Run Manifest and Evidence Package

Every substantial run must produce an immutable or append-only run manifest containing:

```text
Run ID
Run title
Start and completion time
Harness version
Case-pack version
Architecture version
Product release
Code commit and image digest
Environment and namespace
Resource ownership classification and canonical product or `platform-` names
Product Agent Runtime identity and implementation substrate where applicable
Execution mode
Agent run, attempt, execution profile, sandbox ID, sandbox-policy revision, capability-grant set, and teardown result where applicable
Model endpoint, model identity, and model artifact identity where available
Prompt version and content hash
Policy version and content hash
Schema version
Retrieval configuration and source snapshot
Effective runtime configuration revision
Case IDs executed
Random seed and sampling settings where applicable
Chain frontier before and after
Gate results
Skipped, blocked, disabled, and inconclusive gates
Latency, token, queue, cache, and resource metrics
Produced canonical and derived record references
Evidence artifact references
Cleanup result
Known limitations
Operator acceptance where applicable
```

The evidence package should retain enough information to reproduce or explain the result without depending on chat history, a temporary terminal session, or an external dashboard that may disappear.

Secrets must never be written into the run manifest.

### AP.9 Gate and Result Semantics

Allowed gate results are:

```text
passed
failed
blocked
skipped
not_applicable
inconclusive
```

A required `blocked`, `skipped`, or `inconclusive` gate prevents the aggregate run from being reported as fully passed.

A harness summary must report separately:

```text
mechanical contracts passed
semantic calibration passed
fixture chain proven
live chain proven
recovery behavior proven
performance budget met
operator accepted
```

Required rule:

```text
Some gates green
+ one required gate not executed
→ partial evidence, not full success
```

The first failed or blocked load-bearing gate must be named.

### AP.10 Baselines, Replay, and Regression Packs

The project must maintain named regression packs for load-bearing behavior.

At minimum, a pack should include:

- foundational happy paths;
- known boundary cases;
- prior production failures;
- prior operator corrections;
- forbidden outcomes;
- representative performance workloads;
- current model and prompt calibration cases.

Replay is required when changing any load-bearing:

- model;
- quantization or serving implementation;
- prompt;
- context assembly;
- retrieval strategy;
- evidence selection;
- policy;
- schema;
- workflow transition;
- retry or continuation rule;
- projection logic;
- operator action contract.

A new baseline may not be accepted merely because the new implementation produced it.

Baseline promotion must state:

- what changed;
- which regressions are accepted;
- which improvements are material;
- who approved the semantic change;
- whether the architecture or product version changes;
- how the prior baseline remains inspectable.

### AP.11 Isolation, State Control, and Cleanup

Harness runs must control hidden state.

Define:

- namespace, database, collection, tenant, or subject isolation;
- unique run and record prefixes;
- cache treatment;
- queue and lease treatment;
- pre-run state assertion;
- idempotent setup;
- bounded teardown;
- post-run residue detection;
- preservation of failed-run evidence;
- cleanup ownership and timeout.

A failed cleanup must be visible and must not silently contaminate the next run.

Production data is deny-by-default.

Any production smoke write must be:

- explicitly authorized;
- bounded to a known record type;
- tagged with run identity;
- reversible or safely disposable;
- excluded from normal operator truth where appropriate;
- removed or retained according to a declared audit rule.

### AP.12 Performance Harness Realism

Performance claims must use workloads that resemble production.

A representative workload should account for:

- actual context lengths;
- retrieval fan-out;
- evidence package size;
- structured-output size;
- concurrent workers or requests;
- cold and warm model state;
- cache state;
- queue contention;
- real orchestration overhead;
- end-to-end rather than model-only latency.

A short decode-only benchmark must not be used to claim realistic workflow throughput.

Performance reports must distinguish:

- component throughput;
- single-job end-to-end latency;
- concurrent throughput;
- starvation or fairness;
- capacity limit;
- operator-perceived latency.

### AP.13 Harness Documentation Set

Every substantial project must maintain **09 — Harness Architecture and Evaluation Plan**.

It defines:

- harness goals and non-goals;
- harness context and component topology;
- production-path fidelity boundaries;
- applicable harness classes;
- execution modes;
- environment matrix;
- case and fixture model;
- gate catalog;
- semantic rubrics;
- baseline and replay policy;
- isolation and cleanup;
- production-smoke policy;
- result and evidence schemas;
- ownership;
- runbooks;
- known gaps and limitations.

Recommended repository structure:

```text
docs/
  09-harness-architecture-evaluation-plan.md

  prompts/
    catalog/
    packages/
    context-assemblers/
    tool-contracts/
    calibration/
    change-reports/
  agent-runtime/
    execution-profiles/
    sandbox-policies/
    capability-grants/
    execution-manifests/
    change-reports/
  mcp/
    registrations/
    servers/
    application-profiles/
    bindings/
    capability-snapshots/
    schema-fingerprints/
    connector-compilers/
    change-reports/

  harness/
    case-catalog/
    case-packs/
    baselines/
    run-reports/
    fixtures/
    rubrics/
    manifests/

  runbooks/
    harness-local-run.md
    harness-cluster-run.md
    harness-live-model-run.md
    harness-cleanup-and-recovery.md
```

Generated bulk output may live in an artifact store, but the Git-tracked run report must summarize the result and link it through a stable reference and content identity.

### AP.14 Harness Lifecycle and Delivery Gates

The harness evolves with the product.

Required gates:

1. Project foundation defines the Harness Architecture and Evaluation Plan.
2. Every substantial Feature specification identifies applicable harness classes and required cases.
3. The implementer pre-build response names the harness changes required before coding.
4. Each Slice adds or updates cases for the behavior it introduces.
5. Each substantial pull request records harness execution and result identity in its delivery report.
6. Live-path closure requires a live-isolated or explicitly governed production-smoke run through the real chain.
7. Feature and Epic closure require the applicable regression packs, recovery cases, and operator-acceptance evidence.
8. Every escaped defect or material flyswatting lesson adds or updates a durable case before closure unless an ADR records why reproduction is impossible.
9. Model, prompt, policy, retrieval, or serving changes replay affected packs before promotion.
10. Harness gaps remain visible in the FML, Smells Seed, Chain Delivery Register, and End-State Delivery Snapshot where applicable.

Harness work is part of Feature and Slice scope. It must not be deferred automatically into a final testing phase.

### AP.15 Harness Acceptance

A harness architecture is acceptable when:

- a new engineer can run it from documented steps;
- required environments and permissions are explicit;
- the case catalog explains what each case proves;
- fixture and live evidence are separated;
- the same load-bearing production path is exercised;
- all run inputs and versions are identifiable;
- deterministic and semantic assertions are separated;
- failures are reproducible or honestly marked non-reproducible;
- skipped gates cannot produce a green release signal;
- cleanup and residue are controlled;
- prior baselines remain inspectable;
- escaped failures become regression memory;
- run evidence is durable enough to survive the loss of ephemeral dashboards or chat history.

### AP.16 Harness Architecture Smells

At minimum, review for:

- **Harness as Script Pile**;
- **Harness Bypasses Production Path**;
- **Fixture Green, Live Unknown**;
- **Harness Green, Semantics Unknown**;
- **Exact Prose Golden**;
- **Skip Counted as Pass**;
- **Run Without Identity**;
- **Hidden State Between Runs**;
- **Model Change Without Replay**;
- **Failure Found but Not Captured**;
- **Benchmark Without Representative Workload**;
- **Test Backdoor Becomes Product Path**;
- **Harness Can Mutate Production Truth**;
- **Case Pack Without Owner**;
- **Baseline Promoted by Implementation**.

### AP.17 Forbidden Harness Outcomes

Every applicable forbidden outcome must have a deterministic or governed semantic case.

```text
Fixture suite passes
+ live production path is reported as proven

Required gate skipped
+ aggregate result reported as green

Harness writes directly to canonical store
+ claims API or workflow path proof

Model, prompt, policy, retrieval, or schema changes
+ affected semantic packs not replayed

Run report exists
+ exact model, prompt, code, configuration, and case-pack identity cannot be recovered

Prior run state influences result
+ state is absent from setup and manifest

Production smoke run
+ unbounded or unidentified canonical mutation

Escaped production defect fixed
+ no regression case or explicit non-reproducibility record

Performance benchmark uses unrealistic workload
+ production capacity claim is made

Generated wording changes harmlessly
+ byte-for-byte golden marks semantic failure

Semantic meaning changes materially
+ baseline is silently replaced
```

### AP.18 Final Harness Rules

1. The harness is part of the architecture.
2. Harness code is not proof; a named run with durable evidence is proof.
3. Fixture, replay, live, and production-smoke evidence are distinct.
4. Mechanical correctness, semantic quality, chain traversal, and operator acceptance are independent gates.
5. A harness claiming end-to-end proof must traverse the production path.
6. Every substantial AI change requires replay against affected case packs.
7. Every escaped defect should become durable regression memory.
8. Exact prose is rarely the correct semantic golden.
9. A skipped required gate is not a pass.
10. Every run must identify its code, model, prompt, policy, schema, source, cases, and effective configuration.
11. Hidden state and failed cleanup are harness failures.
12. Performance evidence must resemble the real workload.
13. Test-only shortcuts must not become production backdoors.
14. Harness documentation must be understandable without conversation history.
15. The harness must evolve in the same Slice as the behavior it proves.

---


## AQ. Prompt Engineering and Architecture Contract

### AQ.1 Governing Principle

In AI-backed systems, prompts are executable behavioral artifacts.

They influence:

- what question the model believes it is answering;
- which evidence it considers authoritative;
- how context is prioritized or discarded;
- which tools it attempts to use;
- whether it abstains, repairs, continues, or stops;
- what structured records it proposes;
- how much uncertainty reaches the operator.

Prompts therefore require architecture, ownership, versioning, deployment, evaluation, replay, observability, and rollback.

A prompt is not:

- an informal string hidden in application code;
- a substitute for canonical semantics;
- a substitute for deterministic authorization;
- a substitute for state-machine guards;
- a substitute for schema validation;
- proof that the model behaves correctly;
- permission for a tool, write, merge, deletion, promotion, or external transmission.

Required principle:

> Prompt engineering shapes bounded model behavior. Deterministic architecture owns authority, safety, canonical state, and irreversible effects.

### AQ.2 Prompt-System Boundary

Every AI capability must distinguish the following concerns:

```text
Canonical product semantics
    owned by architecture and deterministic records

Policy and authority
    owned by code, policy engines, state machines, and operator gates

Prompt behavior
    owned by versioned prompt packages

Context assembly
    owned by a declared context-selection and budgeting contract

Model execution
    owned by the serving and routing contract

Output acceptance
    owned by schema validation, deterministic invariants, semantic evaluation, and promotion gates
```

The prompt may request an action.

The application decides whether that action is allowed.

### AQ.3 Required Prompt Architecture

Every substantial AI task must define a prompt architecture rather than one undifferentiated prompt blob.

The architecture should separate, where applicable:

1. **Stable governing policy** — enduring product and safety constraints.
2. **Task contract** — the exact operator question and model role.
3. **Input contract** — structured fields and source package presented to the model.
4. **Context assembly** — selected evidence, memory, history, and live material.
5. **Tool contract** — available tools, argument schemas, and bounded intended use.
6. **Output contract** — schema, required fields, evidence references, uncertainty, and terminal dispositions.
7. **Examples or calibration cases** — selected examples that clarify boundaries without silently becoming the product definition.
8. **Repair contract** — the bounded correction path for invalid structure or missing required fields.
9. **Presentation layer** — optional wording transformation that must not alter the governed result.

These layers may be assembled into one model request, but their ownership and precedence must remain explicit.

Required rule:

```text
Prompt text changes
+ governing meaning changes
→ architecture or feature change, not a mere copy edit
```

### AQ.4 Canonical Prompt Package and Registry

Every production prompt package must have a stable identity.

Required metadata:

```text
promptPackageId
applicationSubsystemId
promptVersion
contentHash
status
owner
purpose
operatorQuestion
modelRole
supportedModels
inputSchemaVersion
outputSchemaVersion
policyVersion
contextAssemblyVersion
toolContractVersion
repairPromptVersion
maximumContextBudget
maximumOutputBudget
requiredEvidenceBehavior
applicableCasePacks
createdAt
approvedAt
deprecatedAt
replacedBy
```

Allowed lifecycle states should include:

```text
draft
calibrating
approved
active
deprecated
retired
quarantined
```

Only an approved prompt package may become active.

A production result must be traceable to the exact active package and composition used for that invocation.

### AQ.5 Prompt Composition and Precedence

Prompt composition must declare precedence explicitly.

A typical order is:

1. non-overridable system and safety policy;
2. application authority and task boundaries;
3. exact task contract;
4. trusted canonical context;
5. retrieved or imported evidence clearly marked as data;
6. operator-provided task-specific instructions within allowed scope;
7. output schema and completion rules;
8. bounded examples;
9. repair instructions, only when repair is invoked.

Untrusted documents, web pages, conversation exports, retrieved passages, and tool results must be represented as evidence or data, never silently concatenated into the instruction layer.

Prompt ordering must not be accidental string-concatenation behavior.

### AQ.6 Context Assembly Is Architecture

Context selection is often more consequential than prompt wording.

Every context assembler must define:

- eligible source classes;
- trust domain and context-domain boundaries;
- source precedence;
- current-versus-history treatment;
- as-of time;
- retrieval query and filters;
- evidence ranking;
- deduplication;
- conflict preservation;
- mandatory context;
- optional context;
- excluded context;
- per-source and total token budgets;
- reserved output budget;
- truncation order;
- chunk expansion behavior;
- citation or source-reference mapping;
- omission reporting;
- behavior when required context does not fit;
- behavior when context is missing, stale, conflicting, or unavailable.

Required rule:

```text
Context omitted because of budget
→ omission recorded
→ model must not imply exhaustive review
```

For systems with multiple trust domains, context assembly must be deny-by-default across personal, work, customer, project, tenant, or other governed domains. Cross-domain inclusion requires an explicit governed transfer or promotion path.

### AQ.7 Prompt Authoring Contract

A production prompt should:

- name one bounded model role;
- state the exact question being answered;
- define authoritative inputs and non-authoritative inputs;
- distinguish observation, inference, recommendation, and canonical fact;
- define exhaustive versus representative behavior;
- require honest unknown, unavailable, conflicted, or exhausted outcomes;
- define allowed terminal dispositions;
- require evidence references for load-bearing claims;
- state prohibited actions and prohibited inference classes;
- specify the output schema separately from stylistic guidance;
- define numeric and temporal restrictions;
- define when to use tools and when to abstain;
- avoid contradictory duplicate instructions;
- avoid depending on magic wording that has no semantic explanation.

Prompts should request concise rationale, evidence mapping, confidence basis, or structured self-checks where useful.

They must not require, store, or expose hidden private chain-of-thought as a product contract. The durable product artifact should contain the governed conclusion, supporting evidence, explicit uncertainty, tool trace where applicable, and a concise operator-appropriate rationale.

### AQ.8 Tool and Action Authority

Tool availability and action permission must be enforced outside the prompt.

For every tool define:

- tool identity;
- allowed model roles;
- argument schema;
- authorization predicate;
- data-access boundary;
- trust-domain boundary;
- egress behavior;
- rate and cycle limits;
- idempotency behavior;
- timeout and failure behavior;
- output provenance;
- whether the tool is read-only, candidate-producing, canonical-writing, or destructive;
- whether operator confirmation is required.

Required rule:

```text
Prompt says action is allowed
+ deterministic policy denies action
→ action denied
```

Prompt-only governance is forbidden for capital-bearing, identity-merging, canonical-writing, source-deleting, externally transmitting, or otherwise irreversible operations. The model and prompt also may not select, widen, or disable the active agent execution profile, sandbox policy, trust domain, or MCP capability grant.

### AQ.9 Model Compatibility and Routing

A prompt package must not be assumed portable across models.

For every supported model or model family define:

- tokenizer and context limits;
- chat-template or API requirements;
- tool-calling behavior;
- structured-output support;
- known instruction-following behavior;
- supported context budget;
- required prompt adaptations;
- semantic calibration results;
- latency and capacity expectations;
- fallback eligibility;
- prohibited substitutions.

A serving fallback may not silently substitute a model that has not passed the applicable prompt and semantic case packs.

Model-specific variants may share a common task contract, but each variant requires its own identity and evaluation evidence.

### AQ.10 Change Classification and Versioning

Prompt changes must be classified before promotion.

#### Editorial prompt revision

Changes wording without intending to change governed behavior.

Examples:

- typo correction;
- clearer explanation;
- formatting cleanup.

Editorial changes still require targeted replay because model behavior may change even when human meaning appears unchanged.

#### Compatible behavioral prompt revision

Improves behavior within the existing operator question, authority boundaries, schemas, and lifecycle meanings.

Examples:

- better abstention;
- improved evidence mapping;
- reduced over-classification;
- improved completeness within an existing contract.

This normally increments the prompt minor version and requires affected semantic and live-path replay.

#### Breaking prompt revision

Changes the operator question, canonical meaning, allowed actions, output interpretation, authority boundary, or lifecycle effect.

This requires a Feature or architecture change, migration analysis where persisted outputs are affected, and a major prompt version.

Required test:

```text
Prior output
+ new prompt interpretation
→ could mean something materially different
```

If true, the prompt change is breaking.

### AQ.11 Evaluation and Calibration

Every production prompt package must be evaluated through the Harness Architecture and Documentation Contract.

The case pack should include, where applicable:

- clear positive cases;
- clear negative cases;
- boundary cases;
- ambiguous evidence;
- conflicting evidence;
- missing required evidence;
- unsupported numerical claims;
- stale and current evidence mixtures;
- long-context and truncation cases;
- tool success, timeout, malformed result, and partial failure;
- prompt-injection and untrusted-instruction attempts;
- known PortfolioOS or project-specific escaped failures;
- operator-corrected cases;
- expected abstention or honest exhaustion;
- model-routing and fallback cases;
- repair-loop cases;
- production-like live cases.

Evaluation must separate:

- schema validity;
- deterministic invariant compliance;
- semantic correctness;
- evidence grounding;
- completeness;
- false-positive and false-negative behavior;
- abstention quality;
- tool-use correctness;
- context-budget behavior;
- operator usefulness;
- latency and cost or capacity impact.

A prompt package cannot be promoted solely because a few hand-selected examples look good.

### AQ.12 Deployment and Configuration

Prompt assets must be Git-tracked and deployed through the Runtime Configuration and Kubernetes Deployment Contract.

Preferred deployment pattern:

```text
Git-tracked prompt package
    ↓
ConfigMap-mounted files or immutable packaged prompt artifact
    ↓
Deployment selects prompt package ID/path through scalar configuration
    ↓
Application validates package metadata and content hash at startup
    ↓
Rollout or governed reload activates the new package
```

Use:

- environment variables or ConfigMap keys for small selectors, versions, paths, feature flags, and bounded parameters;
- ConfigMap-mounted files for substantial prompt templates, examples, policy text, output schemas, and calibration assets;
- Secrets only for credentials or sensitive provider values;
- immutable image content only for safe bootstrap defaults, never as the sole production prompt source when independent prompt rollout is required.

Prompt changes must not require an application rebuild unless the prompt is intentionally part of the immutable application artifact and that decision is documented.

Runtime editing of active prompts without Git history, content identity, evaluation evidence, and rollback is forbidden.

### AQ.13 Invocation Provenance and Observability

Every material AI invocation must retain enough information to explain and replay the result without exposing secrets.

Capture:

- prompt package ID, version, and content hash;
- composition manifest and layer versions;
- context-assembly version;
- context manifest or source references and hashes;
- omitted or truncated source accounting;
- model identity and serving endpoint identity;
- sampling and decoding parameters;
- output schema version;
- policy and tool-contract versions;
- tools offered and tools used;
- tool inputs and result references where safe;
- repair attempts and repair prompt identity;
- request and response hashes;
- effective configuration revision;
- latency, token counts, stop reason, and failure classification;
- promotion or rejection outcome;
- operator correction where applicable.

Do not log credentials, secret values, unrestricted private source content, or hidden chain-of-thought.

### AQ.14 Repair, Fallback, and Exhaustion

Repair must be bounded and purpose-specific.

A repair prompt may:

- correct invalid structure;
- fill explicitly required fields using already supplied evidence;
- convert a valid conclusion into the declared schema;
- explain why completion is impossible.

A repair prompt may not:

- broaden the task;
- introduce new authority;
- invent missing evidence;
- silently change the disposition;
- bypass a deterministic validation failure;
- retry indefinitely.

Define:

- maximum repair attempts;
- which failures are repairable;
- which require full re-execution;
- which terminate as failed, incomplete, unsupported, or exhausted;
- whether a fallback model is permitted;
- which case packs every fallback must have passed;
- how the operator sees degraded or fallback behavior.

### AQ.15 Prompt Security and Injection Resistance

Treat retrieved, uploaded, pasted, imported, browsed, emailed, messaged, and tool-returned content as untrusted unless explicitly classified otherwise.

The architecture must define:

- instruction/data separation;
- trust labels;
- content-boundary encoding;
- prompt-injection detection or risk classification where useful;
- tool allowlists and deterministic permissions;
- restricted-data and cross-domain handling;
- secrets exclusion;
- external egress controls;
- behavior when source content attempts to override system instructions;
- behavior when untrusted content requests tools, credentials, or data disclosure;
- logging and operator visibility for blocked attempts.

Delimiters alone are not a sufficient security boundary.

The model may identify suspicious content. Deterministic policy owns the final permission decision.

### AQ.16 Prompt Documentation Set

Every substantial AI-backed project must maintain a standing prompt architecture and catalog.

Recommended document:

```text
10-prompt-architecture-and-catalog.md
```

It should define:

- prompt-system topology;
- canonical prompt packages;
- owners and purposes;
- composition layers and precedence;
- model compatibility matrix;
- context-assembly contracts;
- tool and authority boundaries;
- input and output schemas;
- lifecycle and versioning;
- deployment paths;
- evaluation case packs and promotion gates;
- rollout, rollback, and current active revisions;
- known limitations;
- deprecated and retired packages.

Recommended repository structure:

```text
prompts/
  catalog/
  packages/
    <prompt-package-id>/
      prompt.yaml
      system.md
      task.md
      output-schema.json
      examples/
      repair.md
      README.md
  context-assemblers/
  tool-contracts/
  calibration/
  change-reports/
```

The exact structure may vary, but prompt identity, reviewability, and replayability may not.

### AQ.17 Delivery and Promotion Gates

Before implementation:

- the prompt role and operator question must be explicit;
- prompt authority boundaries must be declared;
- the prompt package and context-assembly architecture must be named;
- input, output, tool, and repair contracts must be defined;
- model compatibility and token budgets must be declared;
- the evaluation pack and promotion gates must be identified.

Before merge:

- prompt assets must be Git-tracked;
- no production prompt may remain hidden in application code without an explicit ADR;
- content identity and version must be available;
- applicable deterministic and semantic cases must pass;
- injection, truncation, repair, and tool-failure cases must be exercised where relevant;
- delivery reports must describe prompt and context changes.

Before deployment:

- the target prompt package and content hash must be explicit;
- ConfigMap or packaged-asset rollout behavior must be proven;
- rollback must be available;
- the serving model must be compatible and calibrated;
- active configuration must be observable.

Before Feature or Epic closure:

- live-path evidence must identify the actual prompt, context, model, tool, policy, and configuration revisions;
- the operator outcome must be accepted independently from schema validity;
- known limitations and remaining prompt smells must be visible.

### AQ.18 Prompt Architecture Smells

At minimum, review for:

- **Prompt Baked Into Application**;
- **Prompt Spaghetti**;
- **Giant Prompt Compensates for Undefined Semantics**;
- **Prompt-Only Governance**;
- **Hidden Context Assembly**;
- **Instruction and Evidence Blended Together**;
- **Silent Context Truncation**;
- **Prompt Change Without Replay**;
- **Model Portability Assumed**;
- **Fallback Model Without Calibration**;
- **Prompt Version Not Recorded**;
- **Runtime Prompt Edit Without Git Record**;
- **Duplicate Prompts Drift Apart**;
- **Magic Phrase Dependency**;
- **Example Becomes Undocumented Policy**;
- **Repair Loop Changes the Decision**;
- **Unbounded Prompt or Tool Cycle**;
- **Prompt Injection Surface Without Policy Boundary**;
- **Schema Valid, Meaning Wrong**;
- **Confidence Without Calibration**;
- **Presentation Prompt Alters Canonical Meaning**;
- **Prompt Owns Destructive Permission**;
- **Context Crosses Trust Domain by Convenience**.

### AQ.19 Forbidden Prompt Outcomes

Every applicable forbidden outcome should have a harness case.

```text
Prompt text changes
+ active version and content hash remain unchanged

Prompt requests canonical write
+ deterministic authority check is absent

Untrusted source contains instructions
+ source instructions override governing policy

Context is truncated
+ output claims exhaustive review

Model fallback occurs
+ fallback has not passed the applicable case packs

Prompt package changes
+ affected semantic and live-path cases are not replayed

Production result exists
+ exact prompt, context, model, policy, tool, and configuration identity cannot be recovered

Repair attempt fails validation
+ repair result is promoted anyway

Prompt stored in ConfigMap changes
+ no rollout, reload, effective revision, or rollback path exists

Operator correction exists
+ prompt reprocessing silently removes it

Presentation rewrite changes governed disposition
+ rewritten result replaces canonical interpretation

Prompt injection attempt is blocked
+ event is invisible where security or operator review requires visibility

Context from another trust domain is available
+ it is included without explicit governed authorization
```

### AQ.20 Final Prompt Rules

1. Prompts are executable behavioral artifacts and require architecture.
2. Prompt behavior is not canonical authority.
3. Tool permission, writes, merges, deletions, egress, and irreversible effects require deterministic enforcement.
4. Context assembly is part of the prompt architecture.
5. Instruction, trusted context, untrusted evidence, examples, tools, output schema, and repair must have explicit boundaries.
6. Every production prompt package needs a stable ID, version, content hash, owner, lifecycle, and supported-model contract.
7. Prompt assets belong in Git and production configuration, not scattered application strings.
8. Large prompt assets should use ConfigMap-mounted files or another governed immutable artifact path.
9. Prompt and model changes require targeted semantic replay before promotion.
10. A prompt package is not portable to another model until calibrated there.
11. Truncation and omission must be observable and must constrain completeness claims.
12. Repair is bounded and cannot invent evidence or expand authority.
13. Untrusted content is data, not instruction.
14. Delimiters do not replace deterministic security boundaries.
15. Every material result must retain prompt, context, model, policy, tool, schema, and configuration provenance.
16. Exact prose is not the governing golden; semantic behavior and evidence are.
17. Hidden chain-of-thought is not a required product artifact.
18. Rollout and rollback must identify the exact active prompt package.
19. Prompt flyswatting becomes institutional memory only when captured in calibration and regression cases.
20. If prompt behavior changes what the product means, the architecture changed.

---

## AR. MCP Capability Access Plane and Connector Architecture Contract

### AR.0 Governing principle

Modern AI-backed systems rely on connectors and tool providers as part of their primary trust and execution architecture. MCP is the default interoperability protocol for those capabilities unless a documented exception proves that another protocol is required.

The framework follows this rule:

> **Standardize connection; localize meaning.**

The shared MCP Gateway platform standardizes dangerous and repetitive protocol, identity, credential, routing, egress, discovery, revocation, session, and observability mechanisms.

Applications retain ownership of operator intent, trust-domain scope, workflow authority, result meaning, evidence, reconciliation, promotion, and canonical truth.

MCP server implementations retain source-specific communication and translation.

The framework doctrine is vendor-neutral. Atlas records the Red Hat/Kuadrant MCP Gateway Operator as its selected platform implementation; that implementation choice does not transfer Atlas application semantics into the gateway.

### AR.1 Governing decision

MCP is the default interoperability protocol for application connectors, external tool providers, internal capability services, and specialized agent services.

HASF-governed systems use a shared governed MCP gateway platform by default rather than allow each application or agent to connect directly to arbitrary MCP servers.

The default ownership split is:

> The shared MCP capability access plane owns MCP protocol execution, routing, authentication, authorization, credential mediation, connector egress, discovery, filtering, revocation, sessions, observability, and platform operations.

> Each application owns connector intent, trust-domain policy, capability-purpose restrictions, workflow authorization, result meaning, source artifacts, semantic compilation, reconciliation, promotion, and canonical truth.

MCP is a connector protocol and capability boundary.

The MCP Gateway is not the OpenShell Gateway.

```text
OpenShell Gateway
→ agent sandbox runtime control plane

MCP Gateway
→ governed capability discovery and invocation plane
```

The OpenShell runtime may restrict which network destinations a sandbox can reach. The MCP Gateway independently decides which registered server and capability the application identity may invoke. Neither decision authorizes canonical application writes by itself.

MCP does not replace:

- application domain models;
- source artifacts;
- evidence;
- jobs;
- attempts;
- revisions;
- candidates;
- deterministic invariants;
- operator locks;
- FML;
- ADRs;
- canonical state;
- application-specific operator surfaces.

---

### AR.2 Reference implementation versus framework doctrine

The framework defines the architectural responsibilities and contracts without requiring one vendor implementation.

Atlas has selected the Red Hat/Kuadrant MCP Gateway Operator as its gateway-platform mechanism.

The framework-level rule is:

> Prefer an established MCP gateway implementation that satisfies the required routing, identity, authorization, credential, observability, isolation, lifecycle, and policy-enforcement contracts. Do not reproduce platform mechanisms inside each application when a governed shared platform already supplies them.

The Atlas-specific implementation decision is:

> Atlas operates the Red Hat/Kuadrant MCP Gateway Operator in the shared agent-serving layer and builds only the Atlas-specific policy, semantic, evidence, and canonicalization layers not supplied by the platform.

The framework does not imply that installing an operator completes application connector architecture.

---

### AR.3 Why connector architecture belongs in HASF

Modern AI-backed systems depend on connectors for:

- external context retrieval;
- enterprise-system access;
- tool invocation;
- governed writes;
- research;
- meeting and communication ingestion;
- source-control operations;
- infrastructure operations;
- internal capability exposure;
- model and agent-service composition.

Without a governing connector architecture, every feature can independently invent:

- authentication;
- credential flow;
- network egress;
- capability discovery;
- schemas;
- retries;
- tool visibility;
- authorization;
- trust domains;
- side-effect control;
- audit;
- provenance;
- prompt handling;
- source completeness;
- canonicalization;
- operator approval.

That produces duplicated security boundaries and inconsistent application behavior.

Connector architecture therefore belongs in the framework alongside:

- harness architecture;
- prompt architecture;
- evidence architecture;
- context trust domains;
- operator surfaces;
- data architecture;
- FML dependencies;
- deployment architecture.

---

### AR.4 Architectural principle

Governing principle:

> **Standardize connection; localize meaning.**

The gateway platform standardizes the dangerous and repetitive mechanism:

- protocol;
- routing;
- server identity;
- credentials;
- egress;
- discovery;
- filtering;
- revocation;
- sessions;
- telemetry;
- audit.

Applications must retain ownership of meaning:

- why a capability is used;
- which domain it belongs to;
- which workflow may invoke it;
- what its result represents;
- whether it may create side effects;
- how it becomes evidence;
- whether it may affect canonical truth.

This prevents two opposite failure modes:

1. Every application builds its own inconsistent connector infrastructure.
2. The central gateway becomes an ungoverned global tool bus containing application business logic.

---

### AR.5 Default topology

```text
Applications and agents
 Atlas | PortfolioOS | future applications
       │
       ▼
Shared MCP capability access plane
       │
       ├── registered server routing
       ├── authentication
       ├── authorization
       ├── credential mediation
       ├── tool discovery
       ├── capability filtering
       ├── revocation
       ├── sessions
       ├── observability
       └── egress enforcement
       │
       ▼
Registered MCP servers
       │
       ▼
External systems, internal capabilities, or agent services
```

Application-specific behavior sits above or behind the shared MCP Gateway:

```text
MCP result
    ↓
application source artifact
    ↓
application compiler
    ↓
typed candidate
    ↓
reconciliation
    ↓
governed promotion
    ↓
canonical truth
```

---

### AR.6 Required ownership split

#### AR.6.1 Shared platform responsibilities

The shared MCP platform owns:

- gateway implementation;
- supported MCP protocol revisions;
- routing;
- server registration;
- listeners;
- connection and session management;
- authentication;
- common authorization integration;
- credential mediation;
- token lifecycle;
- secrets integration;
- TLS and certificate handling;
- network egress;
- capability discovery;
- generic capability filtering;
- revocation;
- common request validation;
- common response handling;
- rate limiting;
- quotas;
- audit;
- traces;
- metrics;
- logs;
- scaling;
- availability;
- upgrades;
- rollback;
- isolated deployment support.

#### AR.6.2 Application responsibilities

Each application owns:

- application MCP profile;
- connector bindings;
- connector purpose;
- trust-domain grants;
- subject and initiative scope;
- approved capabilities;
- denied capabilities;
- argument constraints;
- workflow-stage rules;
- side-effect classes;
- operator-approval requirements;
- source-artifact models;
- source completeness;
- result interpretation;
- semantic extraction;
- reconciliation;
- candidate lifecycle;
- canonicalization;
- application provenance;
- retention;
- deletion lineage;
- application-specific operator surfaces.

#### AR.6.3 Connector responsibilities

Each connector owns:

- source-specific MCP methods;
- underlying system integration;
- pagination;
- remote identifiers;
- source-specific schemas;
- source-specific errors;
- protocol translation.

Connectors must not own application canonical truth.

---

### AR.7 Standard terminology

HASF uses:

**MCP Gateway Platform**
The shared runtime that routes and governs MCP access.

**Connector Registration**
The approved identity and configuration of one MCP server.

**Application MCP Profile**
The application-wide connector and trust policy.

**MCP Binding**
The application-specific contract permitting use of one connector for defined purposes.

**Capability Snapshot**
The approved resources, tools, prompts, and schemas for one connector revision.

**Connector Compiler**
Application-owned logic that converts MCP results into source artifacts, candidates, or other domain objects.

**Invocation Record**
Immutable provenance for one connector operation.

**Platform Audit**
Gateway-level authentication, routing, authorization, and execution evidence.

**Application Provenance**
The lineage between the connector invocation and application source artifacts, candidates, jobs, and canonical writes.

Applications should not describe their local policy layer as a second gateway.

---

### AR.8 Required Connector Architecture section

Every substantial specification involving external systems, tools, connector data, or MCP must include an **MCP Connector Architecture** section.

It must define:

1. Operator outcome.
2. Connector purpose.
3. Connector class.
4. Connector owner.
5. MCP server owner.
6. Gateway implementation.
7. Gateway deployment topology.
8. Shared versus isolated instance.
9. Connector registration.
10. Application MCP profile.
11. MCP binding.
12. Authentication.
13. Authorization.
14. Credential ownership.
15. Token lifecycle.
16. Network path.
17. Egress policy.
18. Trust-domain scope.
19. Capability discovery.
20. Approved capabilities.
21. Denied capabilities.
22. Capability filtering.
23. Revocation.
24. Schema fingerprinting.
25. Capability drift.
26. Resource treatment.
27. Tool treatment.
28. Prompt treatment.
29. Side-effect classification.
30. Operator approval.
31. Retry behavior.
32. Idempotency.
33. Session behavior.
34. Timeout behavior.
35. Partial-result semantics.
36. Source completeness.
37. Source-artifact behavior.
38. Current-versus-history treatment.
39. Connector compiler.
40. Canonicalization policy.
41. Platform audit.
42. Application provenance.
43. Observability.
44. Retention.
45. Deletion lineage.
46. Operator surfaces.
47. Failure states.
48. Live acceptance.
49. Forbidden outcomes.
50. FML items and dependencies.

A statement such as “integrate with X through MCP” is not a complete architecture.

---

### AR.9 Connector classes

Every connector or capability must be classified.

#### AR.9.1 Source connector

Reads existing information.

Examples:

- meetings;
- email;
- calendar;
- documents;
- source control;
- search;
- market data;
- CRM records.

Default doctrine:

> Successful retrieval creates source evidence. It does not directly establish canonical application truth.

#### AR.9.2 Action connector

Changes an external system.

Minimum side-effect classes:

```text
reversible_write
external_communication
destructive
infrastructure_mutation
privilege_change
financial
```

Each class must define:

- operator confirmation;
- authorization;
- idempotency;
- retry safety;
- rollback;
- replay;
- stale-work protection;
- external evidence;
- operator visibility.

#### AR.9.3 Internal capability connector

Exposes a governed internal capability.

Examples:

- evidence retrieval;
- FML lookup;
- ADR lookup;
- governed search;
- organization resolution;
- research invocation.

Raw database access through general-purpose MCP tools is forbidden.

#### AR.9.4 Agent-service connector

Exposes a specialized model, compiler, or agent.

MCP may provide the capability boundary.

Durable work must remain represented through jobs, attempts, artifacts, revisions, and observable lifecycle state.

---

### AR.9.5 MCP server boundary and design

An MCP server is a governed capability adapter, not a miniature application domain.

The server boundary should normally align with one coherent combination of:

- source system or internal capability owner;
- credential and authorization boundary;
- trust zone;
- deployment and availability lifecycle;
- schema and protocol evolution cadence;
- side-effect risk class.

Do not create one server per trivial method merely to maximize component count.

Do not create one global server that exposes unrelated systems, credentials, trust domains, or side-effect classes behind a single undifferentiated endpoint.

Each MCP server specification must define:

- server identity and owner;
- supported MCP protocol revision;
- resources, tools, and prompts exposed;
- capability and schema versioning;
- authentication expected from the gateway;
- upstream credentials and secret ownership;
- network ingress and egress;
- readiness, liveness, and dependency health;
- request, session, timeout, cancellation, and concurrency behavior;
- rate limits and backpressure;
- pagination and continuation;
- partial and truncated result semantics;
- idempotency and side-effect behavior;
- audit and trace correlation;
- deployment, scaling, upgrade, rollback, and deprecation;
- live acceptance through the governed gateway path.

Prefer stateless MCP servers where possible.

Durable application work must remain represented through application-owned jobs, attempts, source artifacts, revisions, and canonical lifecycle records. An MCP session must not become the only record that long-running or consequential work exists.

Required rule:

```text
MCP server restarts or session disappears
+ durable application work exists
→ application can still observe, reconcile, resume, or honestly terminate that work
```

Raw database administration, unrestricted shell execution, and broad infrastructure control must not be exposed through generic MCP servers merely because the protocol permits tools.

---

### AR.10 Resources, tools, and prompts

#### AR.10.1 Resources

A resource represents readable context or an existing object.

Specifications must define:

- visible resource namespaces;
- list versus direct-address behavior;
- trust-domain filtering;
- freshness;
- revisioning;
- persistence;
- source completeness;
- unavailable behavior;
- source-artifact mapping.

#### AR.10.2 Tools

A tool performs search, transformation, computation, or side effects.

Specifications must define:

- argument schema;
- application constraints;
- side-effect class;
- approval;
- idempotency;
- timeout;
- retry;
- result schema;
- error behavior;
- audit;
- provenance.

#### AR.10.3 Prompts

Connector-supplied prompts are untrusted connector content.

They may be used as:

- optional examples;
- source-specific hints;
- template material;
- inputs to application-controlled prompt composition.

They may not:

- override system instructions;
- modify trust boundaries;
- grant capabilities;
- bypass approval;
- change canonicalization;
- redefine application policy;
- silently enter model context as governing instructions.

Prompt discovery and prompt federation must be explicitly governed.

---

### AR.11 Trust-domain doctrine

Connector architecture must preserve first-class context trust domains.

Isolation applies to:

- connector discovery;
- server names;
- tool names;
- tool descriptions;
- resource names;
- resource metadata;
- prompt names;
- schemas;
- search results;
- returned content;
- caches;
- audit records;
- application provenance;
- reconciliation.

A workload in one customer domain must not learn that another customer’s connector, meeting, resource, repository, or tool exists.

Gateway authentication alone is insufficient.

Application-level trust policy must remain explicit and deny-by-default.

A shared physical gateway must provide logical isolation.

Where logical isolation is insufficient, use an isolated gateway deployment of the same platform architecture.

---

### AR.12 Gateway-platform doctrine

#### AR.12.1 Adopt, do not unnecessarily rebuild

Applications should reuse a governed shared MCP gateway platform.

They should not independently implement:

- protocol clients;
- routing;
- credential brokers;
- discovery registries;
- common audit;
- session managers;
- tool filtering;
- revocation;
- common egress controls;

unless the shared platform cannot meet a documented requirement.

#### AR.12.2 Baseline before extension

When a gateway platform is already installed, the first feature slice must be:

- version inventory;
- topology inventory;
- capability verification;
- configuration review;
- security review;
- live acceptance;
- gap analysis.

Do not create FML items to rebuild capabilities already supplied and verified by the platform.

#### AR.12.3 Platform capability does not remove application responsibility

A gateway may authorize that a caller can invoke a tool.

It does not necessarily know:

- whether the current application workflow should invoke it;
- whether the result belongs to the active trust domain;
- whether the result is authoritative;
- whether the result is complete;
- whether it should create a candidate;
- whether it should affect canonical truth.

These remain application concerns.

---

### AR.13 Capability discovery and drift

MCP servers may change their advertised capabilities.

Required lifecycle:

```text
connector registered
    ↓
capabilities discovered
    ↓
schemas fingerprinted
    ↓
application binding reviewed
    ↓
approved snapshot activated
    ↓
runtime filtering enforced
```

A capability being discoverable does not make it approved.

A new or changed capability must enter a governed review state.

Examples:

- new tool;
- changed schema;
- changed description;
- removed tool;
- new prompt;
- new resource pattern;
- changed authentication requirement;
- changed protocol requirement.

Forbidden pattern:

> Automatically allow whatever the MCP server currently advertises.

Tool revocation must be available as an operational control independent of a full application release where the selected platform supports it.

---

### AR.14 Security doctrine

The framework requires:

1. Direct agent access to arbitrary MCP servers is denied.
2. Every MCP server is registered.
3. Every application use has an explicit binding.
4. Credentials do not enter model context.
5. Long-lived credentials are mediated by the shared platform where possible.
6. External connector content is untrusted.
7. Embedded instructions remain data.
8. Connector prompts are non-governing.
9. Capability discovery does not grant authorization.
10. Tool descriptions do not grant permission.
11. Capability changes require review.
12. Trust-domain visibility is deny-by-default.
13. Cross-domain caches are forbidden.
14. Connector egress is restricted.
15. Mutating tools have side-effect classes.
16. Non-idempotent writes are not automatically retried.
17. Revoked tools become unusable within a defined bounded interval.
18. Audit and traces do not expose secrets.
19. Connector success does not prove source completeness.
20. Protocol success does not prove business success.
21. Unsupported content types are quarantined.
22. Connector software is treated as a governed dependency.
23. Third-party connectors require source, credential, network, and schema review.
24. Application canonicalization logic does not belong in the shared MCP Gateway.

---

### AR.15 Source artifact and canonicalization doctrine

The default flow is:

```text
MCP result
    ↓
immutable source artifact
    ↓
typed extraction
    ↓
candidate
    ↓
reconciliation
    ↓
governed promotion
    ↓
canonical truth
```

A specification may simplify this only when it proves that the remote source is itself authoritative and defines:

- identity;
- revision;
- freshness;
- conflict;
- completeness;
- history;
- deletion;
- provenance.

Connector-generated summaries and model-generated interpretations must remain distinguishable from raw source content.

Current truth and source history must be separately modeled.

---

### AR.16 Completeness and partial-result doctrine

Connector calls may succeed at the protocol level while returning incomplete business data.

Every feature must define completeness states appropriate to its source.

Examples:

```text
complete
partial
truncated
stale
unavailable
unknown
```

A partial or truncated result must not be represented as complete.

Bounded continuation and retries are allowed.

Honest exhaustion is required.

The operator surface must distinguish:

- connector reachable;
- authentication valid;
- tool invocation successful;
- source retrieved;
- source complete;
- source compiled;
- candidate created;
- candidate promoted.

---

### AR.17 Provenance doctrine

Every connector call must be attributable.

The combined platform audit and application provenance must answer:

- which application initiated the call;
- which workload initiated it;
- which operator was responsible;
- which trust domain was active;
- which connector was used;
- which server revision was used;
- which capability and schema were used;
- which policy allowed it;
- whether approval was required;
- which arguments were supplied;
- which result was returned;
- whether the result was complete;
- which source artifacts were created;
- which candidates were created;
- which canonical records changed;
- which retries occurred;
- which failures occurred;
- whether replay is safe.

Platform telemetry alone is insufficient when it cannot connect a tool call to application meaning and downstream state.

---

### AR.18 Interaction with harness architecture

MCP architecture is part of harness architecture.

The harness specification must define:

- which connectors are model-visible;
- which tools are model-selectable;
- which calls are deterministic workflow calls;
- whether discovery is dynamic;
- how approved capability lists reach the model;
- how tool descriptions are sanitized;
- how connector prompts are handled;
- how external content is delimited;
- model context limits;
- truncation;
- continuation;
- tool-loop limits;
- malformed-call handling;
- retry behavior;
- evidence requirements;
- invocation traces;
- replay;
- evaluations;
- forbidden tool paths.

A working MCP call is not sufficient acceptance for an agentic feature.

The full harness behavior must be specified.

---

### AR.19 Operator surface requirements

Substantial connector platforms require operator surfaces for:

- gateway health;
- gateway instances;
- registered connectors;
- authentication state;
- authorization state;
- application bindings;
- trust-domain grants;
- discovered capabilities;
- approved capabilities;
- revoked capabilities;
- capability schema changes;
- prompts and resources;
- side-effect classes;
- operator-approval policies;
- invocation history;
- errors;
- retries;
- rate limits;
- quotas;
- traces;
- source completeness;
- quarantined results;
- downstream source artifacts;
- downstream candidates;
- disable and revoke actions.

Forbidden UI state:

> “Connected” presented as one undifferentiated green state.

The operator must be able to distinguish:

- installed;
- registered;
- reachable;
- authenticated;
- authorized;
- bound;
- capability-approved;
- healthy;
- complete;
- application-successful.

---

### AR.20 Deployment doctrine

The default is a shared logical MCP gateway platform in the capability-access plane. It is separate from the OpenShell runtime plane even when both are operated by the same platform team.

The gateway should support:

- horizontal replication;
- application-scoped policy;
- application-scoped quotas;
- application-scoped audit views;
- connector-specific circuit breakers;
- connector-specific routes;
- connector-specific egress;
- separate connector deployments;
- isolated gateway instances where necessary.

Dedicated or isolated gateway instances are justified by:

- customer-dedicated tenancy;
- legal separation;
- regulatory separation;
- air gaps;
- infrastructure ownership;
- incompatible credentials;
- materially different availability;
- trust-zone requirements.

A dedicated instance remains the same architectural platform substrate deployed into another boundary. Its primary resource identity still reflects the actual owner:

```text
Application-owned gateway instance
→ <product>-mcp-gateway

Intentionally shared multi-application gateway
→ platform-mcp-gateway
```

The Red Hat/Kuadrant or other gateway implementation belongs in labels, image provenance, deployment metadata, and documentation. It does not replace the capability identity.

A gateway running in a shared namespace is not automatically `platform-` owned. A product must not reuse another application's MCP gateway, bindings, credentials, policy state, invocation history, or operational persistence without an explicit transfer or shared-platform decision.

---

### AR.21 Exceptions to MCP

MCP is the default, not an unconditional mandate.

A feature may use another protocol when MCP is unsuitable because of:

- transactional requirements;
- unsupported streaming behavior;
- performance constraints;
- existing authoritative internal protocol;
- constrained environment;
- unavailable or unacceptable MCP server;
- unacceptable security profile;
- incompatible lifecycle.

Every exception must document:

1. Why MCP is unsuitable.
2. Authentication.
3. Authorization.
4. Credentials.
5. Egress.
6. capability governance.
7. trust domains.
8. schema versioning.
9. provenance.
10. retries.
11. idempotency.
12. side effects.
13. operator surfaces.
14. live acceptance.
15. future interoperability implications.

“Writing a custom adapter is easier” is not sufficient rationale.

---

### AR.22 Required testing

Connector features must test:

- registered connector success;
- unregistered endpoint denial;
- direct-egress denial;
- disabled binding denial;
- cross-domain discovery denial;
- cross-domain invocation denial;
- credential non-disclosure;
- unapproved capability denial;
- revoked capability denial;
- schema drift detection;
- prompt isolation;
- prompt-injection handling;
- malformed response handling;
- partial-result handling;
- timeout;
- bounded retries;
- non-idempotent retry prevention;
- source revisioning;
- stale-work protection;
- application quota isolation;
- connector disable;
- connector revoke;
- platform audit;
- application provenance;
- source-artifact lineage;
- candidate-only canonicalization;
- gateway failure isolation;
- isolated deployment where required.

Live acceptance must exercise the real:

- network path;
- identity;
- authorization;
- connector;
- source;
- audit path;
- application persistence path.

Mock-only acceptance is insufficient.

---

#### AR.22.1 MCP architecture smells

The Architecture Smells Seed must include, as applicable:

- **Direct Agent-to-Server Bypass** — an application or model can invoke an MCP server outside the governed gateway path.
- **Global Undifferentiated Tool Bus** — unrelated connectors, domains, credentials, and side effects appear as one shared capability namespace.
- **Gateway Owns Application Meaning** — canonicalization, workflow policy, or domain semantics have leaked into the shared MCP Gateway.
- **Application Rebuilds Gateway Mechanism** — an application duplicates routing, credential, discovery, session, revocation, or common audit functions already supplied by the platform.
- **Discoverable Means Authorized** — newly advertised server capabilities become usable without an approved capability snapshot.
- **Connected Means Complete** — gateway reachability or protocol success is presented as source completeness or application success.
- **Connector Writes Canonical Truth** — connector output bypasses source artifacts, candidates, reconciliation, or governed promotion.
- **Connector Prompt Becomes Policy** — connector-supplied prompt content enters the governing instruction layer.
- **Cross-Domain Connector Visibility** — a workload can discover another domain's server, capability, resource, prompt, schema, cache, or audit record.
- **Session Becomes Durable Workflow** — consequential work exists only inside an MCP session with no application-owned job or attempt record.
- **Mega-Server Without Coherent Boundary** — unrelated source systems or side-effect classes are exposed from one server for implementation convenience.
- **Tiny-Server Fragmentation** — one source capability is split into excessive servers without a credential, trust, lifecycle, or ownership reason.
- **Server Schema Drift Without Binding Review** — a changed tool or resource schema reaches callers without fingerprinting and application-binding reconciliation.
- **Unsafe Mutating Retry** — a non-idempotent tool is retried automatically without a stable operation identity or reconciliation.
- **Platform Audit Without Application Provenance** — the gateway logs a call, but the application cannot connect it to source artifacts, candidates, or canonical effects.

Every present smell requires a disposition, owner, and removal or revisit trigger.

---

### AR.23 FML requirements

Connector architecture must be visible in the Feature Memory Ledger.

Expected FML coverage includes:

- gateway platform baseline;
- platform operating model;
- connector registration;
- application binding;
- trust-domain policy;
- capability approval;
- filtering and revocation;
- authentication;
- authorization;
- credential flow;
- network path;
- source artifacts;
- connector compiler;
- invocation provenance;
- content and prompt isolation;
- operator surfaces;
- failure states;
- retention;
- canonicalization;
- live acceptance.

Each substantial connector should have its own FML item or subpage.

Connector work must not be buried as an implementation detail inside a consuming feature.

FML dependencies should distinguish:

- platform dependency;
- connector dependency;
- trust-domain dependency;
- source-artifact dependency;
- compiler dependency;
- operator-surface dependency;
- canonicalization dependency.

---

### AR.24 Forbidden outcomes

The framework explicitly forbids:

- direct agent access to arbitrary MCP servers;
- one global undifferentiated connector tool bus;
- credentials in model context;
- every app building its own gateway without exception;
- automatic activation of discovered tools;
- connector prompts acting as system instructions;
- shared cross-domain caches;
- hidden side effects;
- writes without side-effect classification;
- unsafe retry of non-idempotent actions;
- protocol success represented as business success;
- partial source represented as complete;
- gateway authorization represented as application authorization;
- MCP responses directly mutating canonical truth by default;
- raw database capabilities exposed through broad internal MCP tools;
- application canonicalization logic embedded in the shared MCP Gateway;
- gateway installation represented as complete connector architecture;
- application bypass of the gateway for convenience;
- connector health represented as equivalent to source freshness or completeness.

---

### AR.25 Atlas implementation note

Atlas has already installed the Red Hat/Kuadrant MCP Gateway Operator.

Therefore Atlas-specific specifications should begin with:

1. live platform inventory;
2. supported-capability verification;
3. security and topology review;
4. gap analysis;
5. application binding design;
6. reference-connector implementation;
7. live end-to-end acceptance.

Atlas should not begin with a greenfield gateway build.

The selected operator is the platform mechanism.

Atlas remains responsible for:

- context domains;
- connector purpose;
- application bindings;
- evidence models;
- candidate compilation;
- reconciliation;
- promotion;
- canonical truth.

---

### AR.26 Framework conclusion

The framework codifies a shared MCP connector platform because connectors are now part of the system’s primary trust and execution architecture.

The governing balance is:

```text
MCP capability access plane owns protocol mechanism and tool-access enforcement
applications own intent and meaning
connectors own source-specific communication
```

This creates a reusable connector substrate without creating either duplicated security infrastructure or an ungoverned centralized tool monopoly.

---

## AS. Agent Runtime, Sandbox, and Execution Architecture Contract

### AS.0 Governing principle

Autonomous and semi-autonomous AI behavior is an execution-security problem as well as a prompt, model, workflow, and connector problem.

The h00pz architecture therefore distinguishes five planes:

```text
Application control plane
→ durable intent, workflow, context, approvals, state, result validation, and canonical truth

OpenShell runtime plane
→ isolated agent execution, sandbox lifecycle, process, filesystem, network, credential, and inference enforcement

MCP capability access plane
→ governed capability discovery, authentication, authorization, routing, filtering, revocation, and invocation audit

Model-serving plane
→ bounded inference execution and model capacity

Domain execution plane
→ business invariants, canonical APIs, source-system operations, and durable side effects
```

Required rule:

> **Applications own durable intent and truth. Agent harnesses own bounded model behavior. OpenShell owns isolated execution. The MCP Gateway owns governed capability access. MCP servers own source-specific operations. Domain services own business invariants.**

No single gateway, prompt, agent framework, or sandbox replaces the other planes.

---

### AS.1 Governing decision

OpenShell is the standard h00pz implementation substrate for product-owned agent runtime capabilities in Atlas, PortfolioOS, and subsequent AI applications.

The Red Hat/Kuadrant MCP Gateway Operator is the standard h00pz MCP capability access mechanism unless a later accepted architecture release replaces it.

The application remains free to choose an agent harness or orchestration library appropriate to its problem, but that harness must operate within this contract.

Required default:

```text
Model-controlled tool selection, code execution, non-public context access, or external side effects
→ application-owned agent harness
→ inside an OpenShell sandbox
→ capabilities only through the governed MCP Gateway or an explicitly named narrow application API
```

The primary architectural identity is the product capability, such as **Atlas Agent Runtime** or **PortfolioOS Agent Runtime**. OpenShell is recorded as implementation substrate, image provenance, runtime policy mechanism, and deployment metadata.

OpenShell is not the application agent framework.

MCP is not the agent sandbox.

The MCP Gateway is not the OpenShell Gateway.

---

### AS.2 Why agent runtime belongs in HASF

Without a mandatory runtime architecture, applications can independently invent:

- where agent loops execute;
- which credentials the agent process receives;
- whether the agent can use `curl`, shell, package managers, databases, or the Kubernetes API;
- how tools are reached;
- how filesystem writes are bounded;
- how one customer or project is separated from another;
- how sub-agents inherit context and authority;
- what survives sandbox termination;
- how attempts are retried;
- how results become candidates or canonical state;
- how policy, model, prompt, MCP, and application audit are correlated.

Prompt instructions and MCP authorization do not prevent a compromised or manipulated agent process from trying an alternate execution path.

The runtime contract closes that gap.

---

### AS.3 Standard topology

```text
Operator, scheduler, event, or application workflow
                    │
                    ▼
Application Control Plane
  - canonical application state
  - workflow state machine
  - AgentRun and AgentAttempt records
  - prompt and context selection
  - execution-profile selection
  - operator approval and policy checks
  - result validation and promotion
                    │
                    │ create bounded attempt
                    ▼
Product Agent Runtime
  - application-owned runtime identity
  - application policy and authorization binding
  - application integration and operational state
  - implementation substrate: OpenShell
                    │
                    ▼
OpenShell Gateway
  - sandbox runtime control plane
  - policy and settings delivery
  - sandbox identity
  - provider and inference routing
  - lifecycle and runtime audit
                    │
                    ▼
OpenShell Sandbox
  OpenShell Supervisor
    └── Application-owned Agent Harness
          - model interaction
          - planning and bounded loop
          - tool selection
          - checkpoint and result assembly
              │
              ├── inference.local
              │       ▼
              │   Model-serving plane
              │
              ├── governed MCP client
              │       ▼
              │   Red Hat/Kuadrant MCP Gateway
              │       ▼
              │   Registered MCP servers
              │       ▼
              │   source systems and domain services
              │
              └── narrow application checkpoint/result API
                    │
                    ▼
Application validates result
                    │
                    ▼
Candidate, operator review, deterministic promotion, or honest terminal state
```

The application control plane normally remains outside the sandbox.

The model-controlled execution loop normally remains inside the sandbox.

---

### AS.4 Standard terminology

**Application Control Plane**  
The application-owned durable workflow and state layer that creates attempts, selects approved execution profiles, validates outputs, coordinates approvals, and owns canonical truth.

**Product Agent Runtime**  
The application-owned runtime capability through which the product executes governed agent attempts. Its primary name carries the product identity. It may be implemented with OpenShell and may use platform-operated substrate, but its policy boundary, run lifecycle, application integration, and application-specific operational state remain product-owned unless an explicit shared-platform architecture states otherwise.

**Agent Harness**  
The application-owned behavioral execution package containing the agent loop, prompt and context adapters, tool adapter, checkpoint client, result assembler, and bounded retry behavior.

**OpenShell Gateway**  
The OpenShell sandbox runtime control plane. It manages sandbox lifecycle, runtime state, policy and settings delivery, provider and inference configuration, and Supervisor coordination.

**OpenShell Supervisor**  
The local security boundary inside each sandbox workload. It launches the agent harness as a restricted child process and enforces process, filesystem, network, credential, and inference policy.

**OpenShell Sandbox**  
The isolated execution environment for one bounded agent attempt or explicitly governed group of tightly coupled attempts.

**MCP Gateway**  
The governed capability access plane that authenticates callers, filters approved capabilities, authorizes server and tool use, routes requests, applies quotas, supports revocation, and records invocation audit.

**AgentRun**  
The durable logical assignment representing one requested agent outcome across one or more attempts.

**AgentAttempt**  
One bounded physical execution of an AgentRun using one immutable execution manifest.

**AgentExecutionProfile**  
The approved application-owned declaration of harness image, role, sandbox mode, model route, prompt and context contract, capability grant, resource limits, timeout, checkpoint behavior, and result contract.

**SandboxPolicyRevision**  
The exact OpenShell policy identity applied to an attempt, including process, filesystem, network, credential, inference, and dynamic-policy rules.

**AgentCapabilityGrantSet**  
The approved application and trust-domain-specific MCP bindings and narrow direct APIs exposed to an attempt.

**AgentExecutionManifest**  
The immutable identity package for one attempt, including code, image, prompt, model, context, policy, capability, configuration, trust-domain, and operator or trigger identity.

**AgentResultEnvelope**  
The structured result returned from the sandbox, including disposition, outputs, evidence references, tool trace references, omissions, checkpoints, failure or exhaustion reason, and proposed downstream effects.

---

### AS.5 Execution classification

Every AI capability must be classified before implementation.

#### Bounded non-agentic inference

An ordinary application worker may call a model without OpenShell when all of the following are true:

- the application deterministically selects the model call;
- the model receives a bounded declared input;
- the model cannot select tools;
- the model cannot execute generated code;
- the process has no broad filesystem or network authority;
- the process cannot access arbitrary credentials or canonical stores;
- the model returns a validated bounded schema;
- no model-controlled loop changes the execution path.

Examples may include:

- one-shot classification;
- bounded extraction;
- schema repair;
- presentation rewriting;
- deterministic embedding generation.

#### Model-controlled agentic execution

OpenShell is required when the model can perform one or more of the following:

- select among tools;
- decide whether or when to continue;
- execute or modify code;
- inspect or modify a workspace;
- invoke external or internal capabilities;
- access non-public context from multiple steps;
- create external side effects;
- spawn sub-agents;
- alter its execution plan based on tool results;
- run for a material duration with checkpoints or resumable state.

Required rule:

```text
Uncertain classification
→ treat as agentic
→ use OpenShell
```

A project may not classify a tool-using loop as “just a worker” to avoid the sandbox contract.

---

### AS.6 Required ownership split

#### AS.6.1 Application ownership

The application owns:

- operator outcome;
- canonical Product Agent Runtime identity and ownership-bearing resource names;
- deployed application-specific runtime boundary, gateway instance, control-plane integration, policy binding, and operational persistence where applicable;
- durable workflow;
- `AgentRun` and `AgentAttempt` records;
- context-domain scope;
- execution-profile selection;
- prompt and context package selection;
- capability-purpose policy;
- operator approvals;
- result schema;
- output validation;
- candidate lifecycle;
- canonicalization and promotion;
- retries and reconciliation;
- operator surfaces;
- application provenance;
- retention and deletion lineage.

Any OpenShell internal operational state used by the product is non-canonical and subordinate to the application-owned `AgentRun`, `AgentAttempt`, checkpoint, workflow, and result records.

#### AS.6.2 OpenShell substrate and shared-platform ownership

The shared platform owns:

- OpenShell distribution, installation mechanisms, upgrade qualification, and supported versions;
- shared OpenShell Gateway operation only where an explicit shared-platform deployment has been accepted;
- application-isolated Gateway deployment mechanisms and runbooks;
- sandbox drivers and cluster integration;
- Supervisor-compatible base images;
- common policy templates;
- sandbox identity integration;
- runtime credentials and inference routing;
- common sandbox observability mechanisms;
- platform-level lifecycle reliability;
- quota and resource enforcement;
- common security baselines;
- gateway and sandbox runbooks.

Platform operation of the substrate does not transfer ownership of an application's Agent Runtime capability, authorization, run state, operational store, integration contracts, or canonical records.

#### AS.6.3 MCP capability access ownership

The MCP capability access plane owns the responsibilities defined in AR, including registered server routing, MCP authentication and authorization, capability filtering, connector credentials, revocation, quotas, and invocation audit.

#### AS.6.4 Model-serving ownership

The model-serving plane owns:

- model artifacts;
- serving endpoints;
- capacity and placement;
- model health;
- inference protocol compatibility;
- model and quantization identity;
- request and token telemetry;
- service-level reliability.

It does not own application task meaning or agent authority.

#### AS.6.5 Domain-service ownership

Domain services own:

- canonical business APIs;
- deterministic validation;
- business invariants;
- authoritative side effects;
- source-system writes;
- idempotency and reconciliation at the business boundary.

---

### AS.7 Canonical execution records

Every substantial agentic application must define the following records or prove an equivalent model.

#### AgentRun

Required fields include:

```text
agentRunId
applicationId
contextDomainId
operatorOrTriggerIdentity
requestedOutcome
workflowRevision
status
createdAt
currentAttemptId
attemptCount
approvalState
terminalDisposition
canonicalResultRefs
```

Recommended states:

```text
requested
waiting_for_approval
ready
running
waiting
completed_candidate
completed_no_action
failed
canceled
exhausted
superseded
```

#### AgentAttempt

Required fields include:

```text
agentAttemptId
agentRunId
attemptNumber
executionProfileId
executionManifestId
sandboxId
status
startedAt
heartbeatAt
completedAt
checkpointRef
resultEnvelopeRef
failureClass
cleanupState
```

Recommended states:

```text
planned
provisioning
starting
running
checkpointed
waiting
completing
succeeded
failed
canceled
timed_out
lost
cleanup_pending
cleaned
```

#### AgentExecutionProfile

Required fields include:

```text
agentExecutionProfileId
applicationId
applicationSubsystemId
productAgentRuntimeId
runtimeResourceName
implementationSubstrate
agentRole
harnessImageDigest
entrypoint
sandboxMode
sandboxPolicyRevision
modelRouteId
promptPackageId
contextAssemblyVersion
capabilityGrantSetId
resourceLimits
timeoutBudget
maxToolCalls
maxModelCalls
maxSubAgents
checkpointContract
resultSchemaVersion
supportedTrustDomains
status
```

#### AgentExecutionManifest

The manifest must bind one attempt to exact immutable identities.

At minimum:

```text
application code and image digest
application subsystem identity
Product Agent Runtime identity and ownership-bearing resource name
implementation substrate and immutable image provenance
agent harness identity
execution profile
OpenShell Gateway identity
sandbox and Supervisor identity
sandbox-policy revision and effective policy hash
context-domain and application identity
operator or trigger identity
prompt package and context-assembly identity
model route and model artifact identity
MCP binding and capability snapshot identity
runtime configuration revision
resource and cycle budgets
start and terminal timestamps
```

---

### AS.8 Agent-run and attempt lifecycle

The standard lifecycle is:

```text
Application receives governed trigger
    ↓
Application creates AgentRun
    ↓
Application resolves approvals and execution profile
    ↓
Application creates AgentAttempt and immutable execution manifest
    ↓
OpenShell provisions sandbox
    ↓
Supervisor launches application-owned harness
    ↓
Harness executes bounded model and tool loop
    ↓
Harness checkpoints and returns AgentResultEnvelope
    ↓
Application validates schema, policy, provenance, and stale-work conditions
    ↓
Application creates candidate, no-action outcome, failure, or governed promotion
    ↓
Sandbox is terminated and cleanup verified
    ↓
Application retains durable records and evidence
```

Required rules:

```text
One AgentRun
→ may have multiple attempts

One AgentAttempt
→ exactly one immutable execution manifest

Retry
→ new AgentAttempt
→ same logical AgentRun unless the operator outcome changed

Sandbox termination
→ does not delete AgentRun, AgentAttempt, checkpoints, result evidence, or application provenance
```

---

### AS.9 Agent execution profile contract

Every production agent role must use an approved AgentExecutionProfile.

The profile must define:

- application and agent role;
- harness image digest and entrypoint;
- full-agent or separated-execution mode;
- OpenShell sandbox driver and policy revision;
- supported context domains;
- model route;
- prompt and context package;
- MCP capability grant set;
- allowed narrow application APIs;
- process and binary allow rules;
- filesystem mounts and write locations;
- network destinations;
- credential providers;
- CPU, memory, GPU, storage, process, and time limits;
- model-call, tool-call, loop, and sub-agent caps;
- checkpoint interval and retention;
- output schema and maximum size;
- timeout, cancellation, and cleanup behavior;
- applicable harness case packs;
- rollout and rollback;
- owner and lifecycle.

Allowed lifecycle states:

```text
draft
calibrating
approved
active
deprecated
retired
quarantined
```

The application must fail closed when the selected profile is missing, inactive, incompatible with the trust domain, or cannot be reconstructed.

The model, prompt, tool result, or connector content may not select or widen the profile.

---

### AS.10 Sandbox execution modes

#### Full-agent sandbox

The agent harness, model loop, tool client, workspace, and generated code run inside OpenShell.

This is the default h00pz mode for tool-using agents.

#### Deterministic external orchestrator with sandboxed execution

A deterministic application orchestrator may remain outside OpenShell and create one or more sandboxed attempts for model-controlled or code-execution steps.

This mode is allowed only when:

- orchestration transitions are deterministic and application-owned;
- every model-controlled tool or code path remains inside a sandbox;
- durable workflow state remains outside the sandbox;
- each sandbox step has a separate attempt or explicitly governed execution identity;
- handoffs are observable and replayable.

#### Code-only sandbox

Sandboxing only generated code while the agent loop retains broad credentials, direct tools, or unrestricted network access is not the standard production architecture.

It requires an ADR explaining:

- why full-agent or separated-execution isolation is not feasible;
- which authority remains outside the sandbox;
- compensating controls;
- accepted blast radius;
- migration trigger to the standard architecture.

---

### AS.11 OpenShell component boundary

The OpenShell Gateway may own:

- sandbox API access;
- sandbox state;
- policy and settings delivery;
- provider and inference configuration;
- runtime credential routing;
- Supervisor coordination;
- sandbox logs and policy decisions;
- lifecycle operations.

The OpenShell Supervisor may own:

- launching the harness as a restricted child process;
- process and binary identity enforcement;
- filesystem policy;
- network proxy and egress enforcement;
- credential injection or mediation;
- inference routing;
- runtime session maintenance.

OpenShell must not own:

- the operator outcome;
- application state-machine meaning;
- canonical application records;
- FML or feature status;
- prompt package meaning;
- MCP capability-purpose policy;
- candidate promotion;
- application retries or business reconciliation;
- operator approval semantics.

Required one-way rule:

```text
Application declares approved execution intent
→ OpenShell enforces the runtime envelope

OpenShell observes runtime events
↛ OpenShell invents application meaning
```

---

### AS.12 Process and filesystem policy

Every execution profile must declare:

- permitted entrypoint;
- approved executable identities or classes;
- generated-code execution rules;
- package-manager behavior;
- shell availability;
- read-only application assets;
- writable workspace paths;
- temporary paths;
- persistent checkpoint mount, if any;
- prohibited host paths;
- size and inode limits;
- artifact export path;
- cleanup behavior.

Default rules:

```text
Host filesystem
→ unavailable

Application secrets
→ unavailable as files unless explicitly mediated

Prompt and policy assets
→ read-only

Agent workspace
→ attempt-scoped

Canonical application storage
→ unavailable as a mounted filesystem

Write outside declared workspace or artifact path
→ denied
```

A writable shared volume across trust domains is forbidden.

A persistent workspace must have an application-owned identity, retention policy, and reconciliation contract. Persistence must not silently turn a sandbox filesystem into a canonical store.

---

### AS.13 Network and egress policy

The standard sandbox network policy is deny-by-default.

A normal h00pz agent attempt may reach only the destinations required by its execution profile, normally:

```text
inference.local
approved MCP Gateway endpoint
narrow application checkpoint/result endpoint
approved telemetry endpoint
explicitly approved package or artifact service where required
```

The sandbox must not directly reach:

```text
MCP server endpoints
MongoDB, PostgreSQL, Qdrant, Redis, Neo4j, or other canonical stores
Kubernetes or OpenShift API
cloud metadata endpoints
arbitrary internet destinations
another application’s private APIs
another customer or context domain
secret-management control planes
unapproved model-serving endpoints
```

Required rule:

```text
Agent needs a new external capability
→ register or bind a governed MCP capability
or
→ amend the execution profile through application and platform review

Never:
agent discovers reachable network path
→ path becomes authorized capability
```

Network reachability is not application authorization.

---

### AS.14 Credentials and secrets

The agent harness must receive the minimum runtime credential material required for its bounded execution.

Preferred behavior:

- provider and inference credentials remain behind OpenShell routing;
- connector credentials remain behind the MCP Gateway or MCP server;
- application credentials are represented through short-lived workload identity where possible;
- secrets are never placed in prompt or model context;
- secrets are never written to checkpoints, result envelopes, tool traces, or logs;
- static long-lived credentials inside the sandbox are exceptional;
- every credential has an owner, audience, lifetime, rotation path, and revocation behavior.

The application must not pass one broad service-account token merely because it is simpler than defining capability-specific identity.

---

### AS.15 Inference routing

Sandboxed agents use the OpenShell-governed inference route, normally through `inference.local`, rather than receiving provider credentials or selecting arbitrary model endpoints.

The execution manifest must identify:

- model route;
- serving endpoint identity;
- model and artifact identity;
- quantization or serving profile where material;
- context limit;
- sampling configuration;
- provider credential boundary;
- fallback policy.

Required rules:

```text
Agent requests model outside approved route
→ denied

Fallback model not approved for prompt and case packs
→ denied or honest unavailable outcome

Gateway-scoped inference routing creates incompatible application or trust-domain coupling
→ partition gateway instances or adopt a proven per-sandbox routing mechanism
```

The model-serving plane does not infer which application data the agent may access.

---

### AS.16 MCP composition

The agent harness may use MCP only through the approved MCP Gateway endpoint and AgentCapabilityGrantSet.

The complete authorization chain is:

```text
Application workflow and approval policy
        AND
AgentExecutionProfile and OpenShell network policy
        AND
MCP Gateway server/tool authorization
        AND
MCP server argument and source policy
        AND
Domain-service business invariants
        ↓
operation allowed
```

A denial at any layer stops the operation.

Required distinctions:

```text
OpenShell allows connection to MCP Gateway
≠ tool authorized

MCP Gateway authorizes tool invocation
≠ business operation valid

Tool invocation succeeds
≠ source result complete

Source result complete
≠ canonical application truth
```

The harness may receive only the capability descriptions approved for the active grant set. Discovery from unrelated applications or trust domains is forbidden.

---

### AS.17 Trust-domain identity

Every attempt must belong to exactly one governed application context domain.

The minimum runtime identity package is:

```text
applicationId
contextDomainId
agentRole
agentRunId
agentAttemptId
operatorOrTriggerIdentity
agentExecutionProfileId
sandboxPolicyRevision
capabilityGrantSetId
promptPackageId
modelRouteId
```

Required rule:

```text
One sandbox attempt
→ one application
→ one context trust domain
→ one bounded capability envelope
```

Cross-domain context requires a governed promotion or transfer before the attempt begins, or a separately approved multi-domain profile with an explicit operator outcome and evidence contract.

Physical gateway sharing does not relax logical isolation.

---

### AS.18 Sub-agent architecture

A sub-agent is a new bounded execution identity, not merely another prompt turn.

Default behavior:

```text
Parent requests sub-agent
→ application or approved harness policy creates child AgentAttempt
→ child receives equal or narrower context and capability envelope
→ child runs in a separate sandbox
→ child returns a structured result to parent or application
```

A child attempt must identify:

- parent run and attempt;
- delegated outcome;
- context subset;
- capability grant subset;
- budget;
- timeout;
- result contract;
- terminal and cleanup state.

Forbidden default:

```text
Parent capability envelope
→ copied wholesale to child
```

A shared sandbox for multiple sub-agents requires an ADR proving that the agents are one trust domain, one lifecycle, one policy envelope, and one cleanup unit.

---

### AS.19 Durable state, checkpoints, and workspace

Durable work state belongs to the application.

The sandbox may hold temporary execution state, but the application must be able to determine:

- what assignment exists;
- which attempt is active;
- what checkpoint was last accepted;
- whether the attempt is stale, lost, canceled, or complete;
- what result was returned;
- whether cleanup completed;
- what can be retried or resumed.

Checkpoint requirements:

- checkpoint identity includes run, attempt, sequence, and content hash;
- checkpoint content is bounded and schema-defined;
- secret material is excluded;
- accepted checkpoints are stored through an application-owned path;
- a checkpoint from an old attempt cannot overwrite a newer attempt;
- resumption creates a new attempt unless the execution substrate proves continuation of the same active attempt;
- checkpoint retention and deletion are explicit.

Required rule:

```text
Sandbox lost
+ accepted checkpoint exists
→ application may create a new attempt from that checkpoint

Sandbox lost
+ no accepted checkpoint
→ application records honest loss and follows declared retry or exhaustion policy
```

---

### AS.20 Result and canonicalization boundary

The normal sandbox output is an AgentResultEnvelope, not a direct canonical write.

The envelope must distinguish:

- observed source material;
- model interpretation;
- proposed candidates;
- proposed actions;
- completed external actions;
- evidence and invocation references;
- omissions and truncation;
- uncertainty;
- no-action, incomplete, failed, or exhausted dispositions.

The application validates:

- schema;
- execution manifest identity;
- policy and capability trace;
- source and evidence custody;
- stale-work protection;
- operator approval state;
- deterministic invariants;
- semantic acceptance where required.

Default flow:

```text
AgentResultEnvelope
    ↓
application validation
    ↓
candidate or explicit no-action state
    ↓
reconciliation and operator or deterministic gate
    ↓
canonical write
```

An agent may call a governed domain service that performs an approved external side effect, but that service remains responsible for the business invariant and idempotency contract.

---

### AS.21 Side effects

Every capability available to a sandbox must retain the side-effect classification defined in AR.

For each mutating capability define:

- operation identity;
- precondition;
- application approval state;
- tool and domain authorization;
- idempotency key;
- retry safety;
- stale-attempt behavior;
- external confirmation or receipt;
- rollback or compensation;
- operator-visible record;
- application provenance.

Required rule:

```text
Old or canceled AgentAttempt
→ cannot initiate new side effect
→ cannot replace newer canonical state
```

A model-generated statement that an action succeeded is never sufficient evidence. The domain service or source-system receipt is authoritative for execution status.

---

### AS.22 Retry, cancellation, timeout, and stale work

Retry is application-owned.

OpenShell may report runtime failure, but it does not decide the business retry policy.

Every profile must define:

- provisioning timeout;
- startup timeout;
- heartbeat interval;
- idle timeout;
- total attempt timeout;
- model and tool cycle limits;
- cancellation propagation;
- checkpoint-on-cancel behavior;
- lost-sandbox detection;
- cleanup timeout;
- retryable and non-retryable failures;
- maximum attempts;
- exhaustion state.

Required rules:

```text
Attempt times out
→ terminal attempt state
→ late output preserved diagnostically
→ late output cannot promote or create new side effects

Cancellation requested
→ application marks cancellation intent
→ sandbox execution is terminated or denied further capability use
→ cleanup result recorded

Retry
→ new attempt identity
→ prior attempt remains inspectable
```

---

### AS.23 Observability and provenance

The combined application, OpenShell, MCP, model-serving, and domain-service evidence must answer:

- who or what requested the run;
- which application and trust domain were active;
- which run and attempt executed;
- which execution profile and sandbox policy were active;
- which sandbox and Supervisor ran the harness;
- which code and image digest ran;
- which prompt, context, model, and configuration were used;
- which capabilities were offered, invoked, denied, or revoked;
- which files and network destinations were accessed or denied where policy exposes that evidence;
- which checkpoints and result envelope were accepted;
- which external side effects occurred;
- which candidates and canonical records resulted;
- whether cleanup completed;
- which failure or exhaustion path occurred.

Required correlation keys:

```text
agentRunId
agentAttemptId
sandboxId
traceId
MCP invocation ID
application job or candidate ID
external operation ID where applicable
```

Platform audit without application meaning is incomplete.

Application provenance without runtime enforcement evidence is incomplete for agentic execution.

---

### AS.24 Operator surfaces

Substantial agent platforms require operator surfaces for:

- active and recent AgentRuns;
- product Agent Runtime name, ownership, and implementation substrate;
- attempts per run;
- agent role and execution profile;
- trust domain;
- current lifecycle state;
- sandbox provisioning and health;
- active sandbox-policy revision;
- model route;
- MCP capability grant set;
- tool calls, denials, and side effects;
- checkpoints;
- timeout and budget consumption;
- cancellation;
- retry;
- result disposition;
- cleanup state;
- degraded or unavailable dependencies;
- runtime and application provenance;
- links to downstream candidates or canonical effects.

The operator must distinguish:

```text
run requested
attempt provisioned
sandbox running
agent making progress
agent waiting
attempt completed
result validated
candidate created
side effect confirmed
canonical promotion completed
cleanup completed
```

Forbidden UI state:

> “Agent completed” shown as one green state when only the sandbox process exited.

---

### AS.25 Deployment, ownership, naming, and gateway partitioning

OpenShell is centrally governed as a supported platform substrate.

Each application owns its **Product Agent Runtime** capability, its application control-plane integration, runtime policy and authorization binding, application-specific operational persistence, and integration contracts. A platform team may deploy and operate the underlying OpenShell substrate without becoming the owner of application run state or product semantics.

Primary resource names follow **AI.3**:

```text
Application-owned runtime
→ <product>-agent-runtime

Application-owned control-plane component
→ <product>-agent-control-plane

Application-owned non-canonical runtime persistence
→ <product>-agent-runtime-store

Application-owned runtime policy and observability
→ <product>-agent-policy
→ <product>-agent-observability
```

OpenShell appears in implementation metadata, image provenance, labels, execution manifests, documentation, and runbooks. It is not the primary service identity.

Central substrate governance does not require one physical gateway instance for every application and trust domain.

The default deployment decision must consider:

- application ownership;
- trust-domain isolation;
- sandbox identity isolation;
- policy administration;
- inference routing;
- credential boundaries;
- audit visibility;
- resource quotas;
- failure blast radius;
- upgrade cadence;
- availability requirements;
- upstream maturity and proven multi-tenancy.

Initial h00pz default:

> Operate common OpenShell distributions, base images, policy templates, observability mechanisms, and runbooks through the platform, while deploying ownership-bearing product runtime instances and partitioning Gateway instances by application or material trust boundary until shared logical isolation has been proven through live tests and accepted architecture evidence.

A later consolidation may occur without changing application semantics when the shared deployment proves:

- cross-domain discovery denial;
- policy isolation;
- identity isolation;
- inference-route isolation or compatible routing;
- credential isolation;
- quota isolation;
- audit isolation;
- failure isolation;
- upgrade and rollback safety.

A dedicated Gateway remains the same OpenShell substrate deployed into a narrower boundary. It is named and operated as part of the owning product capability, not as a product-specific replacement for OpenShell.

No application may bind to, reuse, scale, rename, migrate, or repurpose another application's agent runtime, runtime store, graph, database, gateway, or control-plane component merely because it is present or idle. Historical experimental resources are excluded by default.

A separate application runtime store, if required by OpenShell or the harness, must be classified `operational_noncanonical` and remain subordinate to the application-owned `AgentRun` and `AgentAttempt` records.

---

### AS.26 Harness and acceptance

Agent-runtime acceptance is part of the Harness Architecture and Evaluation Plan.

Required deterministic and live cases include:

- bounded inference correctly classified as non-agentic;
- tool-using execution correctly classified as agentic;
- sandbox created from approved execution profile;
- inactive or altered profile denied;
- exact sandbox-policy revision observable;
- ownership-bearing product runtime, gateway, policy, store, and observability names verified;
- implementation substrate visible as metadata without replacing product capability identity;
- foreign-application and historical runtime resources excluded;
- runtime operational persistence proven non-canonical and subordinate to `AgentRun` and `AgentAttempt`;
- direct database access denied;
- direct MCP-server access denied;
- arbitrary internet egress denied;
- Kubernetes API and metadata access denied;
- approved `inference.local` route succeeds without exposing provider credentials;
- approved MCP Gateway route succeeds;
- unapproved tool and cross-domain discovery denied;
- prompt or source content cannot widen sandbox or capability policy;
- sandbox loss preserves durable run and attempt state;
- checkpoint resumption creates correct new attempt identity;
- stale or canceled attempt cannot create side effects or promote output;
- sub-agent receives narrower or equal authority and separate identity;
- cleanup removes attempt workspace and reports residue;
- application validation separates process exit from product outcome;
- platform audit correlates with application provenance;
- one realistic subject traverses application → OpenShell → model/MCP → result → application validation → operator surface.

Evidence must identify the exact:

- application code and image digest;
- Product Agent Runtime canonical name and ownership classification;
- implementation substrate and immutable image provenance;
- agent harness;
- OpenShell Gateway and Supervisor version;
- execution profile;
- sandbox-policy revision and effective hash;
- trust domain;
- prompt and context package;
- model route and model identity;
- MCP binding and capability snapshot;
- result envelope;
- cleanup state.

Mock-only proof is insufficient for the final live-path gate.

---

### AS.27 Exceptions

An exception to OpenShell may be approved only when:

- the behavior is proven bounded non-agentic inference under AS.5; or
- OpenShell cannot satisfy a documented technical requirement; and
- the alternative provides equivalent or stronger process, filesystem, network, credential, inference, identity, audit, and lifecycle controls.

Every exception must define:

1. Exact behavior excluded from OpenShell.
2. Why the standard profile is unsuitable.
3. Model and tool authority.
4. Process and filesystem boundary.
5. Network and egress boundary.
6. Credentials.
7. Trust-domain isolation.
8. Durable run and attempt state.
9. Retry and stale-work behavior.
10. MCP path.
11. Side effects and canonicalization.
12. Observability and provenance.
13. Harness acceptance.
14. Blast radius.
15. Owner.
16. Revisit and migration trigger.

Convenience, implementation familiarity, or minor latency alone are not sufficient reasons.

---

### AS.28 Agent-runtime architecture smells

The Architecture Smells Seed must include, as applicable:

- **OpenShell Gateway and MCP Gateway Conflated**;
- **Model-Controlled Tool Loop Outside Sandbox**;
- **Sandbox Session Becomes Canonical Workflow**;
- **Sandbox Has Direct Database Access**;
- **Sandbox Has Direct MCP Server Access**;
- **Sandbox Has Arbitrary Internet Egress**;
- **One Sandbox Spans Trust Domains**;
- **Sub-Agent Inherits Parent Authority by Default**;
- **Model Selects Its Own Execution Policy**;
- **Agent Output Directly Mutates Canonical Truth**;
- **OpenShell Owns Application Meaning**;
- **Network Reachability Masquerades as Tool Authorization**;
- **Ephemeral Sandbox State Required for Recovery**;
- **Shared OpenShell Gateway Assumed Multi-Tenant Without Proof**;
- **Process Exit Presented as Product Completion**;
- **Sandbox Cleanup Assumed Rather Than Proven**;
- **Agent Profile Without Immutable Identity**;
- **Direct Model Endpoint Bypasses Inference Routing**;
- **One Broad Credential Powers Every Capability**;
- **Sub-Agent Spawn Without Durable Child Attempt**.

Every present smell requires a disposition, owner, and removal or revisit trigger.

---

### AS.29 FML requirements

Agent runtime must be visible in the Feature Memory Ledger.

Expected FML coverage includes:

- OpenShell platform baseline;
- Gateway deployment and ownership;
- standard sandbox policy;
- application execution profiles;
- `AgentRun` and `AgentAttempt` lifecycle;
- checkpoint and recovery;
- trust-domain identity;
- sub-agent attenuation;
- inference routing;
- MCP capability grant integration;
- credential mediation;
- network and filesystem controls;
- result and canonicalization boundary;
- operator surfaces;
- observability and provenance;
- cleanup and residue detection;
- live acceptance;
- exceptions and migration triggers.

Each application with agentic execution must have its own execution-profile and application-integration FML coverage even when the OpenShell platform is shared.

Typed dependencies should distinguish:

- OpenShell platform dependency;
- MCP capability access dependency;
- model-serving dependency;
- trust-domain dependency;
- execution-profile dependency;
- checkpoint and durable-state dependency;
- operator-surface dependency;
- harness and live-acceptance dependency.

---

### AS.30 Forbidden outcomes

The framework explicitly forbids:

- model-controlled tool selection or generated-code execution outside a governed sandbox without an accepted exception;
- direct agent access to canonical databases;
- direct agent access to arbitrary MCP servers;
- direct agent access to the Kubernetes or OpenShift API;
- arbitrary internet egress from agent sandboxes;
- provider or connector credentials in model context;
- the model selecting or widening its own sandbox policy;
- the model selecting or widening its own MCP capability grant;
- one sandbox attempt spanning unrelated trust domains;
- sub-agents inheriting unrestricted parent authority by default;
- an MCP session or sandbox filesystem becoming the only durable workflow state;
- sandbox process exit represented as application or product completion;
- agent output directly replacing canonical truth without application validation;
- a stale, timed-out, canceled, or lost attempt creating new side effects or promotions;
- retry reusing the same attempt identity after terminal failure;
- cleanup failure hidden from subsequent runs;
- OpenShell runtime code containing application canonicalization or workflow meaning;
- network reachability treated as tool authorization;
- MCP authorization treated as business authorization;
- one shared OpenShell Gateway assumed safe for multiple domains without evidence;
- active agent execution whose code, profile, policy, prompt, model, capability grant, configuration, and trust-domain identity cannot be reconstructed.

---

### AS.31 h00pz implementation profile

The default h00pz technology profile is:

```text
Container and orchestration platform
→ Red Hat OpenShift

Agent runtime and sandbox
→ NVIDIA OpenShell operated by agent-serving

Agent harness
→ application-owned and selected per application

Inference route
→ OpenShell-governed route to on-prem model-serving

MCP capability access
→ Red Hat/Kuadrant MCP Gateway Operator

MCP servers
→ source-system or internal-capability adapters

Durable application state
→ application canonical stores and workflows
```

Atlas and PortfolioOS may use different agent harnesses, prompts, models, capabilities, and execution profiles while retaining the same runtime architecture.

A future implementation replacement must preserve the contracts in this section or require an explicit architecture-version decision.

---

### AS.32 Framework conclusion

The standard h00pz agent execution chain is:

```text
Application owns run and intent
    ↓
OpenShell contains the agent harness
    ↓
OpenShell routes approved inference
    ↓
MCP Gateway governs capability access
    ↓
MCP servers perform source-specific operations
    ↓
Domain services enforce business invariants
    ↓
Application validates results and owns canonical truth
```

This architecture prevents agents from acquiring authority merely because a prompt, tool description, network route, credential, or sandbox session exists.

---

## AT. AI Application Subsystem Architecture Contract

### AT.0 Governing principle

An AI application must be architected as a coherent set of bounded application subsystems before features, pages, agents, prompts, pipelines, and services accumulate into an accidental architecture.

The governing rule is:

> **Architect the subsystem before implementing the feature set that will inhabit it.**

An application subsystem is a bounded vertical part of the product that owns a coherent operator outcome, canonical semantics, lifecycle, AI behavior, operator surfaces, and integration contracts.

A subsystem is not merely:

- a page;
- a navigation section;
- a database collection;
- a service;
- a worker;
- a model;
- an agent;
- a prompt package;
- a queue;
- a report;
- a collection of related tickets.

Those may implement or expose a subsystem. They do not define its identity.

Required relationship:

```text
AI application
    ↓
explicit application subsystems
    ↓
features owned by those subsystems
    ↓
components, models, agents, prompts, stores, and surfaces implementing the features
```

Never:

```text
features, pages, workers, and agents accumulate
    ↓
shared tables and ad hoc handoffs appear
    ↓
retroactively call the pile a subsystem
```

---

### AT.1 Lessons from Market Intelligence and the Hunt

Market Intelligence and the Hunt exposed the same underlying architecture failure in different forms.

#### Feature-first accumulation

Useful capabilities were added one at a time before the owning subsystem had a complete boundary and internal architecture.

Market Intelligence accumulated:

- economic and market inputs;
- ETF-flow analysis;
- news and sentiment;
- event tracking;
- thesis mapping;
- research requests;
- evidence candidates;
- horizon views;
- cockpit surfaces;
- model-generated synthesis.

The Hunt accumulated:

- company discovery;
- leader discovery;
- company and leader registries;
- employment and relationship history;
- investigation workflows;
- research triggers;
- rankings and leaderboards;
- lifecycle changes such as retirement, death, succession, and inactivity;
- company and leader detail surfaces.

Each individual capability was defensible. The architecture problem was that the subsystem boundary, canonical subject model, workflow ownership, internal contracts, surface family, and evaluation model were not fully established before the capabilities began defining them implicitly.

#### Surfaces became de facto architecture

Pages and queues began carrying their own representations of:

- subjects;
- status;
- evidence;
- freshness;
- confidence;
- current state;
- history;
- required follow-up;
- model output.

The application then had to reconcile page-local meanings after implementation rather than projecting one designed subsystem model into multiple surfaces.

#### Pipelines became de facto ownership boundaries

Ingestion workers, research loops, ranking jobs, model prompts, and background workflows began deciding:

- which record was authoritative;
- what counted as complete;
- what happened next;
- which result became current;
- when additional research was required.

Execution machinery acquired domain authority because the subsystem had not assigned that authority explicitly.

#### Shared data became hidden integration

Features coordinated through shared collections, implied joins, copied fields, or direct knowledge of another feature's records rather than through named subsystem contracts.

This made it difficult to answer:

- which subsystem owned the subject;
- which subsystem owned the assessment;
- which subsystem owned the workflow;
- which subsystem could change current truth;
- which handoff had failed;
- whether a downstream feature was reading canonical state or an incidental implementation record.

#### Harnesses proved components rather than subsystem outcomes

Individual jobs, prompts, endpoints, and screens could work while the subsystem still failed to produce one coherent operator outcome.

The lesson is not that these products needed more services or more abstraction.

The lesson is:

> **The bounded application subsystem, its internal architecture, and its operator contract must exist before its feature inventory becomes large enough to define them accidentally.**

---

### AT.2 Standard terminology

**AI Application**  
The complete operator-facing product that combines deterministic software, AI behavior, workflows, data, and platform capabilities.

**Application Subsystem**  
A bounded vertical part of the application that owns one coherent operator outcome or closely related outcome family, the canonical semantics required for that outcome, and the complete path from governed ingress to operator-visible result.

**Application Foundation Subsystem**  
A bounded application-owned subsystem that serves several domain subsystems while retaining application-specific meaning. Examples may include governed context, application identity, collaboration, evidence custody, or application-wide decision queues. It is not a generic shared platform merely because several subsystems use it.

**Domain Subsystem**  
An application subsystem centered on a domain outcome such as market analysis, company investigation, portfolio construction, project memory, or collaboration.

**Shared Platform Capability**  
Reusable infrastructure that owns mechanism rather than application meaning, such as model serving, OpenShell, the MCP Gateway, storage, queues, observability, or Kubernetes configuration. It is not an application subsystem.

**Feature**  
A durable operator-visible capability owned by one application subsystem.

**Component**  
A technical implementation unit such as a service, module, worker, collection, API, or UI component.

**Agent or Model Role**  
A bounded execution role used by a subsystem. It does not become the subsystem's canonical owner.

**Operator Surface**  
A projection and action surface over subsystem-owned state. It does not establish canonical meaning merely because the operator sees it.

**Subsystem Contract**  
A versioned request, event, read model, source-artifact handoff, candidate handoff, or other governed boundary between subsystems.

---

### AT.3 Subsystem identity test

A capability should normally become or belong to a distinct application subsystem when several of the following are true:

- it serves a distinct operator outcome or question family;
- it owns canonical concepts with an independent lifecycle;
- it has a distinct authority or correction model;
- it has a coherent ingress-to-outcome workflow;
- it requires a dedicated context-assembly and AI-behavior contract;
- it has a distinct surface family or operator workspace;
- it has materially different freshness, evidence, or revision behavior;
- it has a distinct security, privacy, or trust-domain boundary;
- it can fail or degrade independently;
- it has a distinct scaling, availability, or operational profile;
- it has a meaningful release and acceptance lifecycle of its own.

A capability should normally remain within an existing subsystem when:

- it uses the same canonical subjects and lifecycle;
- it answers an adjacent question for the same operator outcome;
- it changes only presentation or projection;
- it introduces another model or worker but no new semantic boundary;
- it is an additional workflow state within the same owned lifecycle;
- separating it would require duplicated identity, evidence, corrections, or current truth.

Required test:

```text
Different page, service, model, queue, or team
≠ automatically a different subsystem

Different canonical meaning, authority, lifecycle, trust boundary, or operator outcome
→ likely a distinct subsystem
```

Where the answer remains ambiguous, prefer the smaller number of coherent subsystems and record the decision in an ADR.

---

### AT.4 Subsystem versus platform boundary

An application subsystem owns product meaning.

A shared platform owns reusable mechanism.

Required direction:

```text
Application subsystem
→ uses shared platform capability

Shared platform capability
↛ owns application workflow, canonical meaning, feature state, or operator decision
```

Examples:

```text
Model serving
→ supplies inference capacity
→ does not own Market Intelligence analysis semantics

OpenShell
→ supplies governed execution isolation
→ does not own Hunt investigation lifecycle

MCP Gateway
→ supplies governed capability access
→ does not decide whether evidence changes a thesis

Qdrant
→ supplies retrieval projection
→ does not own canonical knowledge

Shared evidence service
→ may preserve source custody and common evidence contracts
→ does not own every subsystem's domain interpretation
```

An application foundation subsystem may be shared by several domain subsystems while remaining application-specific. It must not be pushed into the platform merely to avoid acknowledging shared application semantics.

#### AT.4.1 Ownership-bearing subsystem and runtime names

Subsystem and runtime names must reveal the product boundary.

Required patterns:

```text
Product-owned subsystem or runtime capability
→ <product>-<capability>

Product-owned subsystem-specific capability
→ <product>-<subsystem>-<capability>

Intentionally shared platform capability
→ platform-<capability>
```

A product-owned subsystem may use OpenShell, LangGraph, Kubernetes, MongoDB, Neo4j, Qdrant, or another implementation substrate without adopting that substrate as its primary architectural identity.

Examples:

```text
Atlas Agent Runtime
→ atlas-agent-runtime
→ implementation substrate: OpenShell

PortfolioOS research runtime
→ portfolioos-research-runtime
→ implementation substrate: LangGraph or another approved harness
```

Two applications using the same framework remain two application-owned capabilities unless an accepted shared-platform architecture deliberately unifies them.

Existing resources owned by another application or left by an earlier experiment must be listed as explicit exclusions in the subsystem detail page. They must not become dependencies through convenience, proximity, spare capacity, or renaming.

The complete naming contract is defined in **AI.3 Resource, Component, Namespace, and Runtime Naming**.

---

### AT.5 Required Subsystem Architecture Map

Every substantial AI application must maintain a **Subsystem Architecture Map**.

The map must identify all accepted application subsystems and all material shared platform dependencies.

For each subsystem, record:

```text
Canonical subsystem title
Canonical subsystem ID
Canonical product and resource-name prefix
Subsystem type: domain | application_foundation
Operator outcome or question family
Accountable owner
Canonical concepts owned
Canonical writes owned
Current read models owned
Primary operator surfaces
Owned Features
Upstream subsystem contracts
Downstream subsystem contracts
Shared platform dependencies
Owned namespaces and runtime resource-name stems
Implementation substrates and image provenance
Foreign-application and historical-resource exclusions
Context and trust-domain scope
AI roles and execution classification
Harness and case-pack identity
Lifecycle status
Architecture version introduced
Canonical detail-page link
```

Recommended lifecycle states:

```text
proposed
boundary_review
architecting
accepted
in_delivery
partially_live
live
operator_accepted
degraded
retiring
retired
superseded
```

The Subsystem Architecture Map is a current projection.

Each substantial subsystem must have one canonical detail page.

Required rule:

```text
Subsystem map conflicts with subsystem detail page
→ detail page wins
→ map must be reconciled
```

The map must support answering:

- What are the application’s actual subsystems?
- Which operator outcome does each own?
- Which canonical concepts and writes does each own?
- Which Features belong to each subsystem?
- Which subsystem boundaries are crossed by the current workflow?
- Which boundaries are direct dependencies, and which are merely shared platform use?
- Where are duplicate ownership, hidden coupling, or missing contracts present?
- Which subsystem is degraded or incomplete even though some of its Features are live?

---

### AT.6 Canonical subsystem detail page

Each subsystem detail page must contain, as applicable:

```text
Canonical subsystem title
Canonical subsystem ID
Architecture version
Document revision
Subsystem type
Status
Accountable owner
Canonical product prefix and subsystem resource-name stem
Owned namespaces and runtime resources
Shared-platform dependencies by canonical `platform-` name
Implementation substrates and deployment metadata
Excluded foreign-application and historical resources
Purpose
Operator outcome
Primary operator questions
Included responsibilities
Explicit exclusions and non-goals
Boundary rationale
Owned Features and FML items
Owned canonical concepts and records
Referenced external canonical concepts
Authority and correction model
Current-truth and history model
Internal lifecycle and state machines
Ingress and source contracts
Internal information flow
Derived artifacts and projections
AI roles and model responsibilities
Prompt and context architecture
Bounded versus agentic execution decisions
Agent-runtime and MCP dependencies
Operator surface family
Outbound contracts and downstream consumers
Cross-subsystem dependency graph
Security, privacy, and trust-domain scope
Runtime and deployment view
Failure and degraded modes
Observability and operational health
Semantic and product-quality measures
Harness classes, case packs, and live acceptance
Migration from prior feature-first structures
Known smells and accepted ADR exceptions
Open questions
Revisit triggers
```

A detail page may link to deeper feature, prompt, harness, connector, and agent-runtime specifications. It must remain sufficient to explain the subsystem without reconstructing it from those documents.

---

### AT.7 Canonical ownership inside and across subsystems

Every canonical concern must have one owning subsystem.

The owner controls:

- identity;
- lifecycle;
- authoritative fields;
- current revision;
- history;
- correction behavior;
- legal transitions;
- canonical write APIs;
- emitted change events;
- rebuildable projections.

Other subsystems may hold:

- identifiers;
- versioned references;
- cached read projections;
- local derived assessments;
- local workflow state;
- source-artifact links;
- operator decisions belonging to their own outcome.

They may not independently maintain a competing copy of the same canonical truth.

A shared real-world subject may be referenced by several subsystems without granting them all ownership.

Example pattern:

```text
Canonical Company Identity subsystem
→ owns company identity, aliases, merge, split, and lifecycle identity

Hunt subsystem
→ owns investigation state, coverage, leader relationships, and investigation outcomes

Market Intelligence subsystem
→ owns market-relevance assessments, signal relationships, and analytical conclusions
```

The exact decomposition is application-specific. The ownership rule is not.

Forbidden shortcut:

```text
Two subsystems need the same object
→ both write the same collection
```

Required alternative:

```text
One subsystem owns the canonical object
→ other subsystems reference it
→ local meaning remains locally owned
→ changes cross a governed contract
```

---

### AT.8 Reference internal subsystem architecture

Every subsystem must define its internal path from ingress to operator outcome.

A common reference shape is:

```text
Governed ingress
    ↓
Preserved source or request
    ↓
Normalization and identity resolution
    ↓
Candidate or working state
    ↓
Deterministic and AI-assisted evaluation
    ↓
Canonical subsystem decision or revision
    ↓
Current subsystem read model
    ↓
Operator surface and action
    ↓
Governed outbound event, request, or projection
```

Not every subsystem requires every stage.

Every included stage must define:

- purpose;
- owner;
- input contract;
- output contract;
- state transition;
- canonical and derived writes;
- AI involvement;
- idempotency;
- stale-work behavior;
- failure behavior;
- operator visibility;
- harness proof.

Internal layers should normally distinguish:

1. **Ingress and source custody** — what enters and how it is preserved.
2. **Canonical domain core** — the records and invariants the subsystem owns.
3. **Workflow orchestration** — the legal lifecycle and continuation behavior.
4. **AI behavior** — bounded model and agent roles operating under subsystem policy.
5. **Read models and projections** — current operator-facing state.
6. **Operator surfaces** — understanding, decisions, corrections, and actions.
7. **Outbound contracts** — governed handoffs to other subsystems.
8. **Harness and operations** — proof, observability, recovery, and degradation.

---

### AT.9 AI role architecture within a subsystem

Every model, agent, prompt package, context assembler, retrieval path, and tool set must belong to a named subsystem role or to a named shared platform mechanism.

For each subsystem AI role, define:

- exact task;
- operator outcome supported;
- canonical inputs;
- eligible context;
- trust-domain scope;
- model and compatibility contract;
- bounded versus agentic classification;
- prompt package;
- tool and capability grants;
- output schema;
- evidence and provenance requirements;
- deterministic validation;
- canonical-write authority;
- repair, fallback, and abstention;
- evaluation pack;
- latency and resource budget;
- owner.

Required rules:

```text
One shared model endpoint
≠ one shared behavioral role

One generic agent harness
≠ one application-wide semantic authority

Model output
≠ subsystem contract

Agent completion
≠ subsystem outcome completion
```

A model may serve several subsystems physically. Each subsystem retains distinct prompts, context, tools, output contracts, evaluation cases, and authority boundaries.

A generic “AI service” must not become the hidden owner of multiple subsystem semantics.

---

### AT.10 Subsystem context architecture

Each AI-backed subsystem must define how it assembles the context required for its own operator outcome.

The subsystem context contract must define:

- canonical subjects in scope;
- permitted context domains;
- current versus historical sources;
- required and optional sources;
- cross-subsystem read contracts;
- evidence or source precedence;
- freshness;
- ranking and deduplication;
- token budgets;
- truncation and omission behavior;
- contradiction preservation;
- provenance;
- context-package identity;
- invalidation and replay.

Required rule:

```text
Subsystem needs context owned elsewhere
→ request a governed projection or source package
→ preserve owner, revision, freshness, and provenance

Never:
subsystem agent scans arbitrary application stores
→ assembles undocumented global context
```

The application must resist the **one big brain** pattern in which one model receives a mixture of unrelated subsystem state and is expected to infer boundaries, authority, freshness, and operator intent dynamically.

Cross-subsystem context is a governed contract, not a convenient database join or vector search across everything.

---

### AT.11 Operator architecture for a subsystem

Each subsystem must define a coherent family of operator surfaces rather than a collection of unrelated pages added by Feature.

The subsystem surface architecture must identify, as applicable:

- overview or current-state surface;
- work or decision queue;
- canonical subject detail;
- evidence or source drilldown;
- history and revision comparison;
- failure, stale, degraded, and unavailable states;
- administrative or policy surface;
- cross-subsystem navigation and handoff points.

Every surface must state:

- which subsystem owns it;
- which subsystem read model it presents;
- which other subsystem projections it consumes;
- which writes remain local;
- which actions request work from another subsystem;
- which current revision root governs the display.

Required rule:

```text
Surface needs data from several subsystems
→ compose declared projections
→ preserve each owner and freshness state

Never:
UI join invents a new canonical meaning
→ no subsystem owns the result
```

Navigation categories do not define subsystem boundaries. A subsystem may expose several surfaces, and one application workspace may compose several subsystems, but canonical ownership must remain visible in the architecture.

---

### AT.12 Cross-subsystem contract types

Subsystems integrate only through explicit contracts.

Allowed contract classes include:

#### Request or command

One subsystem requests that another perform work it owns.

The receiving subsystem decides the legal transition and retains canonical authority.

#### Domain event

One subsystem publishes a completed fact about state it owns.

Consumers may react but may not reinterpret the event as permission to mutate the producer's truth.

#### Read projection or query

One subsystem exposes a current or historical read model for another subsystem.

Freshness, revision, completeness, and unavailable behavior must be explicit.

#### Source or evidence handoff

One subsystem transfers a preserved source artifact or evidence reference for another subsystem to interpret under its own semantics.

Source custody and interpretation ownership remain distinct.

#### Candidate or proposal handoff

One subsystem proposes work, a relationship, an action, or an assessment to another subsystem.

The receiving subsystem owns acceptance, rejection, reconciliation, and canonicalization.

Each contract must define:

```text
Contract ID and version
Producer subsystem
Consumer subsystem
Purpose
Trigger
Input and output schema
Canonical owner
Identity and correlation keys
Revision and freshness
Completeness
Idempotency
Ordering
Retry and timeout
Stale-work behavior
Authorization and trust domain
Evidence and provenance
Failure and degraded behavior
Observability
Harness cases
Deprecation and migration
```

Model-generated prose, copied database rows, and UI-side joins are not subsystem contracts.

---

### AT.13 Cross-subsystem workflow ownership

Every workflow that crosses subsystem boundaries must have one declared coordinator.

The coordinator may be:

- an application workflow service;
- one owning subsystem;
- a dedicated application foundation subsystem;
- a deterministic saga or state machine.

The coordinator owns:

- the end-to-end workflow identity;
- requested outcome;
- current cross-subsystem stage;
- handoff correlation;
- timeout and cancellation;
- recovery and reconciliation;
- operator-visible progress;
- honest terminal state.

Each participating subsystem still owns its internal lifecycle and canonical writes.

Required rule:

```text
Cross-subsystem workflow coordinator
→ may request work and observe results
→ may not bypass participant invariants
```

An agent may assist with planning or execution, but durable workflow coordination remains application-owned and must survive model, agent, sandbox, connector, or process loss.

---

### AT.14 Identity, relationship, and shared-subject boundaries

Where several subsystems reason about the same people, organizations, projects, instruments, documents, or other subjects, the architecture must define:

- canonical identity owner;
- alias and resolution owner;
- merge and split authority;
- temporal identity behavior;
- relationship ownership;
- local subsystem assessments;
- cross-subsystem subject references;
- behavior when identity remains unresolved.

Required rule:

```text
Shared subject
→ one canonical identity
→ multiple subsystem-owned interpretations may reference it

Never:
subsystem convenience copy
→ second canonical identity
```

Relationships also require ownership.

One subsystem may own an employment relationship while another owns an investigation hypothesis about that employment. These are not the same record and must not be collapsed merely because they concern the same subjects.

---

### AT.15 Source, evidence, and derived-artifact boundaries

AI application subsystems often share source material without sharing interpretation.

The architecture must distinguish:

- preserved source custody;
- source identity and revision;
- evidence references;
- subsystem-specific extraction;
- subsystem-specific candidates;
- subsystem-specific derived assessments;
- operator corrections;
- canonical decisions.

A shared source or evidence foundation may provide common custody and addressing.

Each subsystem remains responsible for:

- why the source is relevant to its outcome;
- which claim or observation it derives;
- how contradiction is represented;
- how the result affects its lifecycle;
- whether the result becomes canonical within the subsystem.

Required rule:

```text
Shared source
≠ shared interpretation

Shared evidence reference
≠ shared canonical conclusion
```

---

### AT.16 Lifecycle, revision, and freshness

Every subsystem must define its own complete lifecycle and how that lifecycle interacts with upstream and downstream change.

Define:

- current revision root;
- historical revisions;
- source or request time;
- processing time;
- effective time;
- freshness requirements;
- invalidation triggers;
- reprocessing behavior;
- supersession;
- retirement;
- downstream notification;
- stale dependent behavior.

A subsystem must not silently fill missing current state from its own history or from another subsystem's older projection.

Material upstream change must trigger one of:

- deterministic update;
- bounded reassessment;
- explicit stale state;
- operator review;
- no action under a declared rule.

It must not trigger unbounded application-wide research merely because a shared subject changed.

---

### AT.17 Failure, degradation, and isolation

Subsystems must fail honestly and, where practical, independently.

For each subsystem define:

- unavailable state;
- degraded state;
- stale state;
- partial state;
- dependency-blocked state;
- recovery behavior;
- queued work behavior;
- operator visibility;
- downstream impact;
- isolation boundary.

Required distinctions:

```text
Infrastructure healthy
≠ subsystem semantically current

Model endpoint healthy
≠ subsystem result valid

Subsystem internal workflow complete
≠ cross-subsystem operator outcome complete
```

A subsystem failure must not corrupt another subsystem's canonical truth.

A downstream subsystem must not present stale or partial upstream projections as current merely because the integration call returned successfully.

---

### AT.18 Logical versus physical decomposition

A subsystem is a logical architecture boundary.

It does not automatically require:

- a separate repository;
- a separate service;
- a separate namespace;
- a separate database;
- a separate deployment;
- a separate team.

The default h00pz implementation preference is:

> **Preserve logical subsystem boundaries first. Split physical deployment only when scale, security, availability, ownership, release cadence, or failure isolation justifies it.**

A modular monolith may implement several well-bounded subsystems safely.

Microservices do not create subsystem coherence by themselves.

Required rules:

```text
Logical boundary absent
+ services separated
→ distributed feature pile

Logical boundary explicit
+ modules share one deployable
→ potentially valid subsystem architecture
```

When a subsystem is physically separated, the previously defined contracts become network contracts without changing semantic ownership.

---

### AT.19 Security, privacy, and trust boundaries

Every subsystem detail page must define:

- subjects and data classes it may access;
- operator roles;
- trust domains;
- write authority;
- external egress;
- model and agent access;
- connector access;
- audit requirements;
- cross-subsystem disclosure rules;
- deletion and retention consequences.

A subsystem may not gain access to another subsystem's full internal store merely because both belong to the same application.

Access should be limited to the contract required for the declared outcome.

Cross-domain transfer remains governed even when both participating subsystems run in the same process or database.

---

### AT.20 Feature placement and ownership

Every substantial Feature must identify exactly one owning application subsystem.

A Feature may cross several subsystem boundaries, but it must still define:

- the owning subsystem;
- participating subsystems;
- canonical writes per subsystem;
- contracts crossed;
- coordinator;
- operator surface ownership;
- harness cases for every handoff.

Required rule:

```text
Feature crosses multiple subsystems
→ one Feature owner
→ explicit participating subsystem contracts

Never:
Feature is "shared"
→ no subsystem owns outcome or writes
```

Every Feature specification, FML item, Slice, TDD, pull request, delivery report, and Chain Delivery node or edge must name its owning subsystem or state why it is a shared platform artifact.

A Feature that cannot be placed cleanly is an architecture signal. The subsystem map must be corrected before implementation continues.

---

### AT.21 FML and subsystem architecture

The Feature Memory Ledger remains the canonical memory of remembered capabilities.

The Subsystem Architecture Map remains the canonical current decomposition of the application.

They serve different purposes:

```text
FML
→ what capabilities have been remembered and how they are classified

Subsystem Architecture Map
→ where accepted application responsibility and canonical ownership live
```

Every FML item detail page must record:

- proposed or accepted owning subsystem;
- whether it changes a subsystem boundary;
- whether it creates a new subsystem candidate;
- subsystem contracts introduced or changed;
- shared platform dependencies;
- affected subsystem detail pages;
- subsystem-specific harness and operator-surface impact.

Required rule:

```text
FML item classified required_now
+ no owning subsystem or explicit subsystem-creation decision
→ item not ready to weave
```

Subsystem architecture does not replace FML. FML does not replace subsystem architecture.

---

### AT.22 Subsystem architecture and delivery hierarchy

The delivery hierarchy remains:

```text
Project
→ Epic
→ Feature
→ Slice
```

Subsystem is an architecture and ownership dimension, not another delivery-container level.

Typical relationship:

```text
One subsystem
→ may own several Epics and Features

One Epic
→ may coordinate Features across several subsystems

One Feature
→ has one owning subsystem and may consume contracts from others
```

Every Chain Delivery Map must mark:

- the owning subsystem for each node;
- the producer and consumer subsystem for each cross-boundary edge;
- the first blocked subsystem handoff;
- disconnected subsystem islands;
- the operator-visible frontier.

A locally complete subsystem component does not advance the application chain until its required boundary contracts are connected and proven.

---

### AT.23 Required subsystem design sequence

Before a large Feature set begins, design the subsystem in this order:

```text
1. Subsystem charter and boundary
2. Canonical concepts and ownership
3. Internal lifecycle and current read model
4. Ingress, source, and evidence contracts
5. AI roles, prompts, context, tools, and execution classification
6. Operator surface family
7. Cross-subsystem contracts and workflow coordination
8. Harness, observability, failure, and recovery
9. Deployment and security boundaries
10. One narrow end-to-end reference Slice
```

Do not attempt to implement the entire subsystem at once.

The first reference Slice should prove one real path through:

```text
realistic ingress
→ subsystem canonical core
→ bounded AI behavior where applicable
→ current read model
→ operator surface
→ one governed downstream or upstream handoff where required
```

Only after the reference Slice proves the architecture should the subsystem expand through additional Features.

---

### AT.24 Subsystem architecture gates

A substantial subsystem must pass the following gates before broad Feature implementation.

#### Gate 1 — Boundary

- operator outcome is explicit;
- included and excluded responsibilities are explicit;
- subsystem identity test has been applied;
- overlap with existing subsystems is resolved.

#### Gate 2 — Canonical ownership

- canonical concepts and writes are assigned;
- referenced concepts have external owners;
- current truth and history are defined;
- shared mutable ownership is absent.

#### Gate 3 — Internal lifecycle

- ingress-to-outcome workflow is defined;
- states and transitions are explicit;
- failure, stale, partial, and exhausted outcomes are honest;
- current read model is defined.

#### Gate 4 — AI and context

- model and agent roles are bounded;
- prompt and context architecture is explicit;
- tools and authority are deterministic;
- bounded versus agentic execution is classified;
- provenance and replay are possible.

#### Gate 5 — Operator system

- operator questions have intentional surfaces;
- actions and write effects are defined;
- current, history, evidence, failure, and degraded behavior are visible.

#### Gate 6 — Integration

- upstream and downstream subsystem contracts are versioned;
- coordinator is named for cross-subsystem workflows;
- idempotency, freshness, failure, and reconciliation are explicit;
- direct cross-subsystem canonical mutation is prohibited.

#### Gate 7 — Harness and acceptance

- subsystem case packs exist;
- one realistic subject or workflow can traverse the subsystem production path;
- semantic, mechanical, failure, recovery, and operator gates are distinct;
- cross-subsystem handoffs have cases.

#### Gate 8 — Operations and evolution

- deployment and security boundaries are justified;
- observability distinguishes technical and semantic health;
- migration from prior structures is defined;
- FML, Smells, delivery, and version impacts are recorded.

Broad Feature implementation begins only after these gates are accepted or an ADR records a bounded exception.

---

### AT.25 Subsystem harness and acceptance contract

Every substantial subsystem requires its own named harness scope and case pack.

Acceptance must prove:

- canonical ownership and invariants;
- internal lifecycle;
- one realistic ingress-to-operator path;
- AI behavior on clear, boundary, failure, and abstention cases;
- context and provenance behavior;
- current versus history;
- stale, partial, unavailable, and degraded states;
- operator corrections and regeneration;
- cross-subsystem requests, events, projections, and candidate handoffs;
- dependency failure and recovery;
- no direct cross-subsystem mutation;
- migration or rebuild where applicable;
- operator acceptance through the real surface.

The subsystem must report separately:

```text
component health
internal chain health
semantic quality
upstream dependency health
downstream handoff health
operator-acceptance state
```

A collection of green Feature tests is not sufficient if the subsystem's complete operator outcome remains unproven.

---

### AT.26 Subsystem operator and architecture surfaces

Projects with several substantial subsystems should expose architecture and operational views that answer:

- Which subsystems exist?
- What outcome does each own?
- Which are live, degraded, blocked, or incomplete?
- Which canonical records does each own?
- Which cross-subsystem handoffs are failing?
- Which Features and FML items belong to each?
- Which models, prompts, agents, connectors, and harness packs serve each?
- Which subsystem owns the current operator-visible result?

This may be a Git-tracked architecture map, an application administration surface, or both.

A visual diagram is useful.

A complete textual ownership and contract map is mandatory.

---

### AT.27 Subsystem architecture smells

The Architecture Smells Seed must include, as applicable:

- **Feature Pile Becomes Subsystem** — related Features accumulate without an accepted subsystem charter, canonical model, or internal lifecycle.
- **Page Defines the Domain** — a surface introduces subjects, statuses, or decisions that no subsystem owns canonically.
- **Agent Becomes the Architecture** — an agent loop implicitly owns workflow, continuation, and truth because the subsystem did not define them.
- **Pipeline Owns Meaning** — an ingestion or research pipeline decides domain semantics or canonical promotion by implementation convenience.
- **Shared Database as Integration** — subsystems coordinate by reading and writing each other's collections rather than using governed contracts.
- **Cross-Subsystem Canonical Mutation** — one subsystem directly changes records owned by another.
- **One Big AI Brain** — one model or agent receives broad application context and is expected to infer subsystem boundaries and authority dynamically.
- **Context Soup** — context from multiple subsystems is assembled without owner, revision, freshness, trust-domain, or omission contracts.
- **Generic AI Service Owns Domain Semantics** — a shared AI component becomes the hidden authority for several subsystem outcomes.
- **Subsystem Without Operator Outcome** — a technical cluster is labeled a subsystem despite owning no coherent operator result.
- **Duplicate Subject Core** — several subsystems maintain competing canonical identity or lifecycle for the same subject.
- **Duplicate Acquisition or Research Path** — multiple subsystems independently fetch, preserve, or investigate the same source class without a deliberate custody and interpretation split.
- **UI Composition Creates New Truth** — a dashboard joins projections into a conclusion that no subsystem owns.
- **Navigation Equals Architecture** — menu sections are treated as subsystem boundaries without semantic review.
- **Microservices Masquerade as Boundaries** — physical separation exists without logical ownership or contract discipline.
- **Modular Monolith Without Modules** — one deployable permits unrestricted cross-subsystem access and hidden coupling.
- **Cross-Subsystem Workflow Without Coordinator** — several subsystems participate, but no durable owner tracks the complete outcome.
- **Subsystem Harness Added Last** — Feature implementation advances while no subsystem case pack proves the integrated outcome.
- **Subsystem Locally Green, Application Chain Broken** — the subsystem passes internally while required upstream or downstream handoffs remain unproven.
- **FML Item Without Subsystem Home** — a required capability is accepted without an owning subsystem or explicit subsystem-creation decision.
- **Foundation Subsystem Becomes Global Junk Drawer** — shared application semantics accumulate in one catch-all subsystem with no coherent outcome or ownership rule.
- **Platform Absorbs Application Meaning** — reusable infrastructure acquires subsystem-specific semantics merely because several subsystems use it.

Every present smell requires a disposition, owner, and removal or revisit trigger.

---

### AT.28 Forbidden subsystem outcomes

Every applicable forbidden outcome must have a deterministic or governed harness case.

```text
Feature implementation begins
+ owning subsystem is unknown

Two subsystems
+ independently own the same canonical concern

Subsystem A
+ writes Subsystem B canonical store directly

Surface displays combined conclusion
+ no subsystem owns its meaning or revision root

Agent or pipeline completes
+ subsystem outcome represented as complete without application validation

One model or context assembler
+ receives unrestricted application-wide context by convenience

Cross-subsystem context used
+ owner, revision, freshness, trust domain, and provenance absent

Shared platform component
+ contains application subsystem workflow or canonical semantics

Subsystem boundary
+ inferred only from deployment or repository layout

Subsystem deployed separately
+ no versioned contract or independent failure behavior

Subsystem shares one deployable
+ unrestricted internal writes bypass ownership boundaries

Cross-subsystem workflow
+ no durable coordinator, correlation identity, timeout, or recovery path

Feature tests pass
+ subsystem production path or operator outcome unproven

FML item required_now
+ no subsystem placement or boundary decision

Subsystem map says owner A
+ detail page or implementation gives canonical writes to owner B

Subsystem dependency fails
+ stale or partial projection displayed as current without visible degradation
```

---

### AT.29 Migration from feature-first architecture

Existing applications may already contain emergent subsystems.

Do not begin by rewriting everything.

Use this sequence:

1. Inventory current Features, pages, workers, prompts, agents, stores, and queues.
2. Group them by actual operator outcome and canonical concern.
3. Identify competing owners and duplicate subject models.
4. Name the smallest coherent subsystem set.
5. Create the Subsystem Architecture Map and detail pages.
6. Assign every existing Feature and FML item to an owner.
7. Freeze new cross-boundary direct writes.
8. Define contracts around the existing implementation.
9. Select one broken or high-value end-to-end path as the reference Slice.
10. Migrate canonical ownership and read models incrementally.
11. Add subsystem-level harness cases before broad new Feature work.
12. Retire duplicated records, pipelines, and surfaces only after migration and operator acceptance.

Required rule:

```text
Emergent architecture is messy
→ first make ownership and handoffs explicit
→ then simplify incrementally

Never:
architecture cleanup declared
→ big-bang rewrite with no operator-visible Slice
```

Market Intelligence and the Hunt should be evaluated using this migration sequence rather than repaired through another round of isolated Features.

---

### AT.30 Required standing document

Every substantial AI application with more than one application subsystem must maintain:

```text
13-ai-application-subsystem-architecture.md
```

It defines:

- the Subsystem Architecture Map;
- subsystem identity criteria;
- canonical detail-page links;
- subsystem boundaries and ownership;
- shared subjects and identity ownership;
- cross-subsystem contracts;
- workflow coordinators;
- shared application foundation subsystems;
- platform boundaries;
- context and trust-domain flows;
- AI roles by subsystem;
- operator surface ownership;
- subsystem harness and acceptance scopes;
- deployment and failure-isolation decisions;
- migration from emergent feature-first structures;
- known smells, exceptions, and revisit triggers.

Recommended repository structure:

```text
docs/
  13-ai-application-subsystem-architecture.md
  14-current-as-built-architecture.md
  hasf/
    current.md                    # stable pointer to the accepted HASF release
  subsystems/
    subsystem-detail-template.md
    <canonical-subsystem-id>.md
    contracts/
      <producer>-to-<consumer>-<contract-id>.md
    diagrams/
    migrations/
```

The standing map is the canonical navigation and current decomposition record.

Each subsystem detail page is the canonical architecture record for that subsystem.

Individual Feature specifications govern Feature behavior. They do not replace the subsystem detail page.

---

### AT.31 Final subsystem rules

1. Architect the subsystem before its Feature inventory becomes the architecture.
2. Every Feature has one owning application subsystem.
3. Every canonical concern has one owning subsystem.
4. A subsystem owns an operator outcome, not merely a technical component.
5. A page, service, model, agent, prompt, queue, or database is not automatically a subsystem.
6. Shared platform mechanism must not own application meaning.
7. Shared application semantics must not be hidden inside a supposedly generic platform.
8. Subsystems integrate through explicit versioned contracts.
9. Cross-subsystem canonical writes are denied.
10. Shared subjects retain one canonical identity owner.
11. Shared source does not imply shared interpretation.
12. Context crossing a subsystem boundary requires owner, revision, freshness, trust-domain, and provenance contracts.
13. AI roles are scoped to subsystem outcomes and evaluation packs.
14. Cross-subsystem workflows require a durable coordinator.
15. Logical boundaries come before physical deployment boundaries.
16. A subsystem is not complete until its real ingress-to-operator path and required handoffs are proven.
17. FML remembers capabilities; the Subsystem Architecture Map assigns accepted responsibility.
18. Existing feature-first systems should be bounded and migrated incrementally, not rewritten blindly.
19. If a Feature cannot be placed cleanly, the architecture is not ready for that Feature.
20. If no subsystem owns the meaning of a result, the application does not own that result coherently.

---

## AU. Agent Operating Instructions and Repository Truth Contract

### AU.0 Governing principle

AI implementation agents require two different systems:

1. a small operating contract that tells them **how to work**;
2. a canonical repository architecture that tells them **what is true**.

These systems must remain distinct.

Required rule:

```text
Agent operating rules
→ behavior, sequencing, delegation, review, documentation, and change discipline

Repository architecture and delivery artifacts
→ project meaning, ownership, decisions, capability state, deployed reality, scoped work, and evidence
```

The operating contract must not become a copied miniature of the repository.

The repository must not depend on an agent remembering project truth from conversation or prior prompt context.

---

### AU.1 Responsibility model

The default h00pz responsibility split is:

```text
Agent operating instructions
→ govern behavior

HASF
→ governs architecture and delivery method

Architecture documents
→ govern target system design, semantics, ownership, invariants, and boundaries

ADRs
→ govern accepted difficult-to-reverse decisions and rejected alternatives

Canonical FML detail pages
→ govern remembered capability truth, classification, dependencies, weaving, and lifecycle state

FML index and generated tiered deployment order
→ project current FML summaries and living sequencing from canonical item records and typed dependencies

Current As-Built Architecture
→ governs the current implemented and deployed system reality

Feature specifications and accepted plans
→ govern the bounded intended work for the active change

Chain Delivery Register
→ governs current connected delivery position, frontiers, blocked handoffs, and next chain-closing action

Git-tracked delivery reports
→ preserve historical as-built and as-proven results for completed delivery stages

Git and pull requests
→ govern reviewed change, atomic history, and integration
```

This is not one global authority ladder. Each artifact is authoritative for a different question.

Required rule:

> Ask the repository artifact that owns the question. Do not ask the agent instruction file to answer every question.

---

### AU.2 Canonical answer by question

A contributor or implementation agent should be able to resolve the following without relying on conversation memory:

| Question | Canonical source |
|---|---|
| How must work be performed? | Canonical Agent Operating Contract |
| Which method governs specification and delivery? | Current accepted HASF release |
| What is the target system architecture? | Foundation and standing architecture documents |
| Why was a major decision made? | Accepted ADR |
| What is true about one remembered capability? | Canonical FML item detail page |
| What is the project-wide FML summary and current tiered deployment order? | Generated FML index and tiered deployment-order projection |
| What is implemented and deployed now? | Current As-Built Architecture |
| What is the bounded intended outcome of this Feature or Slice? | Accepted Feature specification and implementation plan |
| Where does the live delivery chain stop now? | Chain Delivery Register |
| What did a completed Slice, TDD stage, or pull request actually deliver and prove? | Git-tracked delivery report and End-State Delivery Snapshot |
| What exact change introduced the current state? | Git history and pull request record |

Where two artifacts appear to answer the same question, the architecture must identify which is canonical and which is a projection, summary, plan, or historical record.

---

### AU.3 Canonical Agent Operating Contract

Every substantial repository should maintain one canonical Agent Operating Contract.

The default filename is:

```text
AGENTS.md
```

A project may choose another stable canonical filename when its toolchain requires it.

Tool-specific instruction files such as `CLAUDE.md`, IDE instruction files, or automation-specific rule files may project or adapt the canonical contract. They must not independently redefine project truth or drift into competing behavior contracts.

The canonical operating contract should contain:

- stable imperative working rules;
- the required Feature and operational execution modes;
- documentation and implementation synchronization rules;
- delegation and review boundaries;
- pull request, merge, and push behavior;
- ownership and naming behavior;
- the repository path to the current HASF pointer;
- the repository paths to the architecture index, FML, Current As-Built Architecture, specifications, plans, Chain Delivery Register, and delivery records;
- the established build, language, and container baseline or stable links to their canonical declarations;
- explicit stop and escalation behavior when repository truth is missing or contradictory.

It should not contain:

- copied architecture chapters;
- a current component inventory;
- a copied FML item list or dependency graph;
- current delivery status;
- copied ADR decisions and rationale;
- current deployed image, model, prompt, or configuration revisions;
- full Feature requirements;
- transient task plans;
- secrets or credentials;
- conversation-derived project facts that have not been captured canonically.

There is no universal line-count limit. The governing test is whether the rules remain small enough to stay salient and stable enough to avoid becoming another project encyclopedia.

---

### AU.4 Default operating rules

A project may adapt the wording, but the following seven behaviors form the default h00pz agent operating contract:

1. **Documentation and implementation move together.**
2. **Features follow Spec → Plan → Code.**
3. **Sub-agents implement; reviews constrain them.**
4. **Operational work stays serial.**
5. **Ownership determines naming and reuse.**
6. **Every build follows the established stack and container baseline.**
7. **Design broadly; implement narrowly.**

These rules intentionally describe behavior rather than restating product architecture.

#### Documentation and implementation move together

A change is not complete when code exists but the affected canonical documentation remains stale.

#### Features follow Spec → Plan → Code

Architecture-bearing Feature work begins only after the governing specification and bounded implementation plan are accepted.

#### Sub-agents implement; reviews constrain them

Sub-agents may execute bounded planned work. Review roles challenge assumptions, enforce contracts, and reject violations. A sub-agent does not gain authority to redesign subsystem ownership, canonical truth, or runtime boundaries because implementation is difficult.

#### Operational work stays serial

Live-cluster mutation, stateful migration, secret rotation, production repair, destructive action, and other operational work remain under one accountable controller unless an accepted runbook explicitly proves a safe alternative.

#### Ownership determines naming and reuse

The resource-classification and naming contract applies before an existing service, runtime, store, namespace, or platform component is reused.

#### Every build follows the established stack and container baseline

An implementation agent uses the project-declared language, framework, dependency, base-image, and container contracts rather than introducing a parallel stack for convenience.

#### Design broadly; implement narrowly

The specification considers the complete operator, subsystem, failure, and delivery architecture. The active Slice implements only the smallest coherent vertical increment required to advance the chain.

---

### AU.5 Feature work versus operational work

The execution model must match the work class.

#### Feature work

Feature work changes governed product capability, semantics, workflow, operator surfaces, AI behavior, or durable application state.

Default sequence:

```text
accepted specification
→ bounded implementation plan
→ pre-build review
→ delegated or direct implementation
→ constrained review
→ deployment and proof
→ canonical documentation reconciliation
```

Feature implementation may use sub-agents after the plan establishes:

- bounded ownership;
- exact files and components;
- allowed architectural decisions;
- acceptance criteria;
- handoff contracts;
- stop rule.

The coordinating implementer remains accountable for cross-task integration and repository truth.

#### Operational work

Operational work changes the live environment or durable operational state directly.

Examples include:

- cluster or namespace mutation;
- database migration;
- storage movement;
- credential or Secret rotation;
- live gateway or policy change;
- production incident response;
- state reconciliation;
- destructive cleanup;
- rollout rollback.

Default sequence:

```text
one accountable controller
→ one explicit operation
→ observe and verify
→ record result
→ continue or stop
```

Parallel operational mutation is prohibited unless an accepted plan or runbook proves that the operations are independent, reversible, observable, and safe.

Required principle:

> **Sub-agents for bounded Feature implementation; one hand on the wheel for operations.**

---

### AU.6 Documentation and change atomicity

Documentation is part of the implementation change.

Before a substantial pull request is opened or represented as ready, the implementer must sweep every artifact affected by the change, including as applicable:

- README architecture-at-a-glance summary;
- foundation and standing architecture documents;
- subsystem detail pages and contracts;
- ADRs;
- Feature specifications and plans;
- benchmarks and harness records;
- canonical FML item pages;
- generated FML index and tiered deployment order;
- Chain Delivery Register;
- Current As-Built Architecture;
- delivery reports and End-State Delivery Snapshot;
- runbooks and operational baselines.

Required rules:

```text
Code changes governed behavior
+ affected canonical documentation unchanged
→ pull request incomplete

FML item reaches live or delivery_active state
→ canonical FML detail page updated
→ learned dependency edges and affected dependents reconciled
→ complete tiered deployment order regenerated
→ generated ledger and dependency projections refreshed
→ Current As-Built Architecture updated
→ architecture-at-a-glance projection updated
→ affected architecture, ADR, specification, benchmark, and runbook records updated in the same change
```

Generated projections must be regenerated from canonical records. They must not be hand-edited into a competing truth.

Documentation-only corrections are valid changes when they reconcile stale or contradictory canonical truth.

---

### AU.7 Context loading and retrieval

The Agent Operating Contract is suitable for persistent instruction context because it contains stable behavior.

Project truth should be retrieved from the repository when needed.

At the start of a task, the implementation agent must identify and read the smallest relevant canonical set, normally including:

- the current HASF pointer;
- applicable architecture documents and ADRs;
- the owning subsystem detail page;
- the canonical FML item pages;
- the current Feature specification and plan;
- the Current As-Built Architecture;
- the Chain Delivery Register and relevant delivery history.

The agent should not preload every architecture document into every task context.

Required rule:

```text
Stable behavior
→ persistent operating instructions

Task-relevant project truth
→ repository retrieval at task start and when boundaries change
```

Conversation history, model memory, issue comments, and prior generated summaries may help locate a fact. They do not become authoritative until the fact is captured in the correct canonical repository artifact.

When required truth is missing, contradictory, or stale, the agent must resolve or explicitly record the contradiction before architecture-bearing implementation continues.

---

### AU.8 Stable pointers and embedded truth

Agent instruction files should prefer stable repository pointers over embedded versioned facts.

Preferred:

```text
Current HASF → docs/hasf/current.md
Current architecture → docs/14-current-as-built-architecture.md
FML index → docs/04-feature-memory-ledger.md
```

Avoid requiring every instruction file to embed a release number such as `v1.2.2 r3` when a stable canonical pointer can identify the current release.

Where a rule file intentionally embeds a version, stack baseline, image family, or other project fact, that line is a cached assertion.

Required rule:

```text
Canonical fact changes
+ cached assertion exists in an operating-rule projection
→ update both atomically
```

A stale HASF version, container baseline, stack declaration, path, or architecture reference in an agent instruction file is a documentation defect.

---

### AU.9 Current As-Built Architecture

Every substantial project must maintain a Current As-Built Architecture document.

Recommended filename:

```text
14-current-as-built-architecture.md
```

This document answers:

> What system actually exists now?

It must describe the current implemented and deployed reality, including as applicable:

- current subsystem and component inventory;
- ownership-bearing resource names and namespaces;
- canonical stores and operational stores;
- active runtime, gateway, connector, model-serving, and platform relationships;
- current canonical read and write paths;
- implemented operator surfaces;
- current live and operator-acceptance frontiers;
- active architecture, schema, prompt, policy, model, image, and configuration identities where material;
- known degraded, partial, unavailable, or unimplemented behavior;
- accepted temporary architecture and removal triggers;
- links to canonical detail documents and delivery evidence.

It must not:

- describe target architecture as though it is live;
- become a Feature backlog;
- replace subsystem, runtime, MCP, prompt, harness, or system architecture documents;
- infer live state from merged code alone;
- hide degraded or disconnected capability.

The target architecture documents define what the system is intended to become.

The Current As-Built Architecture defines what the system is now.

The README architecture-at-a-glance section, if present, is a concise projection of the Current As-Built Architecture and must be updated with it.

---

### AU.10 Review and acceptance

A substantial change is ready only when reviewers can confirm:

- the Agent Operating Contract remains short, behavioral, and internally consistent;
- task-specific truth was retrieved from canonical repository sources;
- no architecture-bearing decision exists only in conversation or instruction context;
- the accepted specification and plan preceded Feature implementation;
- delegated tasks remained inside their bounded authority;
- operational mutation remained serial or followed an accepted exception;
- all affected documentation moved with the implementation;
- FML detail truth and generated projections agree;
- when an FML implementation completed, the tiered deployment order was regenerated from the reconciled full graph before subsequent work was selected;
- the Current As-Built Architecture matches deployed reality;
- target architecture, current reality, scoped plan, current delivery state, and historical delivery evidence remain distinguishable;
- tool-specific instruction projections agree with the canonical operating contract;
- embedded version or baseline assertions are current.

The implementation agent's pre-build response must name the canonical repository sources consulted and any contradictions or stale references found.

---

### AU.11 Architecture smells

The Architecture Smells Seed must include:

- **Agent Rules as Project Encyclopedia** — a tool instruction file contains copied architecture, FML, inventory, delivery, or deployment truth instead of stable behavior and pointers.
- **Stale Truth in Agent Instructions** — a version, stack, path, component, dependency, or architecture assertion in an operating file no longer matches its canonical source.
- **Conversation Memory as Authority** — implementation proceeds from chat or model memory without capturing the decision or fact in the owning repository artifact.
- **Tool-Specific Rule Drift** — `AGENTS.md`, `CLAUDE.md`, IDE instructions, or automation rules give materially different working behavior.
- **Feature Code Before Plan** — implementation begins before the accepted specification, bounded plan, and pre-build response establish authority and scope.
- **Review Agent Becomes Shadow Architect** — a review or implementation sub-agent silently changes canonical semantics, subsystem ownership, or runtime boundaries outside the accepted plan.
- **Parallel Operational Mutation** — several agents or processes mutate shared live state without one controller, safe independence proof, and coordinated recovery.
- **Code and Documentation Split** — implementation changes while affected FML, architecture, current-state, specification, or runbook records remain stale.
- **Current Architecture Missing** — target documents exist, but no canonical page explains the actual implemented and deployed system.
- **Target Presented as Built** — a planned component, workflow, or integration appears in current architecture or README as live without deployment and acceptance evidence.
- **Generated Projection Hand-Edited** — an index, tiered deployment order, or architecture summary is edited independently of its canonical records.
- **Instruction Context Dependency** — the system can be maintained correctly only when one agent retains a large prior conversation or hidden prompt context.

---

### AU.12 Forbidden outcomes

```text
Agent instruction file
+ becomes canonical source for project architecture, FML state, or deployed reality

Feature implementation begins
+ no accepted specification and bounded plan

Sub-agent encounters implementation difficulty
+ silently changes system architecture or ownership

Multiple agents mutate live operational state
+ no single controller or accepted safe-parallel runbook

Code ships
+ affected canonical documentation remains stale

FML item becomes live
+ item page, generated ledger, current architecture, and architecture-at-a-glance remain unchanged

Conversation contains accepted architecture decision
+ repository has no ADR, specification, FML update, or architecture change

Tool-specific operating rules disagree
+ contributor behavior depends on which agent is used

Current As-Built Architecture lists target capability
+ capability is not deployed and live-proven

Agent rule references old HASF or stack baseline
+ change is represented as documentation-complete

Generated index or tiered deployment order changes
+ canonical item records do not explain the change
```

---

### AU.13 Final operating and truth rules

1. Agent operating instructions govern behavior; repository artifacts govern truth.
2. HASF governs method, not project-specific current state.
3. Architecture documents govern target system design.
4. ADRs govern accepted decisions and alternatives.
5. Canonical FML detail pages govern capability memory and state; indexes and dependency order are projections.
6. The Current As-Built Architecture governs implemented and deployed reality.
7. Specifications and plans govern bounded intended work, not current live truth.
8. The Chain Delivery Register governs current connected delivery position.
9. Delivery reports preserve historical as-built and as-proven truth.
10. Git and pull requests govern change and atomic history.
11. Keep persistent operating rules small, imperative, stable, and linked.
12. Retrieve task-relevant truth from the repository rather than carrying the whole system in prompt context.
13. Feature work follows Spec → Plan → Code.
14. Sub-agents implement bounded plans; reviews constrain them.
15. Operational mutation remains serial by default.
16. Documentation and implementation move together.
17. Every shipped capability updates both its capability truth and current as-built truth.
18. Stable pointers are preferred; embedded project facts must be updated atomically.
19. Conversation memory is never the only home of an architecture-bearing fact.
20. If the repository cannot tell an agent what is true, the project documentation architecture is incomplete.

---

# 6. Architecture Document Set for a New Project

Every new substantial h00pz project should begin with four foundation documents, eleven standing architecture-memory, scope, review, delivery-traceability, historical-delivery, harness-evidence, prompt-governance, connector-governance, agent-runtime, AI-application-subsystem, and current-as-built artifacts, plus one short repository-level Agent Operating Contract.

## 00 — Project Primer

Explains:

- product vision;
- operator;
- problem;
- terminology;
- platform context;
- conceptual model;
- core workflows;
- assumptions;
- non-goals;
- project-specific background needed by a new contributor.

## 01 — Architecture Constitution

Defines:

- governing principles;
- authority;
- invariants;
- forbidden outcomes;
- ownership boundaries;
- ownership-bearing resource, namespace, runtime, gateway, store, policy, and observability naming rules;
- product-owned, shared-platform, external, foreign-application, and historical-resource classifications;
- AI application subsystem boundaries, canonical ownership, and cross-subsystem write prohibitions;
- KISS rules;
- semantic safety rules;
- external-data rules;
- model rules;
- prompt authority, context-domain, tool-permission, and prompt-change rules;
- MCP gateway, server, binding, capability-approval, side-effect, and connector trust-domain rules;
- agent runtime, OpenShell sandbox, execution-profile, run/attempt, sub-agent, and direct-access-denial rules;
- current/history rules.

## 02 — System Architecture

Defines:

- Subsystem Architecture Map, canonical subsystem identities, detail-page links, subsystem-scoped AI roles, and cross-subsystem contracts;
- resource ownership inventory and canonical product or `platform-` names;
- owned namespaces, runtimes, gateways, stores, policies, and observability resources;
- implementation-substrate and image-provenance metadata;
- foreign-application and historical-resource exclusions;
- components;
- services;
- records;
- stores;
- projections;
- state machines;
- APIs;
- agents;
- models;
- connectors;
- deployment;
- security;
- observability;
- runtime configuration inventory;
- Kubernetes environment-variable, Secret, and ConfigMap contracts;
- configuration validation, revision, and rollout behavior;
- build graph, dependency caching, container layering, delivery budgets, and immutable digest verification;
- delivery chains, handoff contracts, live frontiers, disconnected islands, and end-to-end acceptance;
- harness topology, production-path fidelity, execution modes, evidence flows, and isolation boundaries;
- prompt packages, composition, context assembly, model compatibility, tool authority, prompt deployment, provenance, rollout, rollback, and semantic evaluation;
- MCP gateway topology, connector registrations, application profiles and bindings, capability snapshots, server boundaries, credential and egress paths, trust-domain isolation, side-effect classes, source-artifact compilation, provenance, revocation, and capability drift;
- application control plane, OpenShell Gateway and Supervisor, AgentRun and AgentAttempt records, execution profiles, sandbox policies, trust-domain identity, inference routes, checkpointing, teardown, cleanup, and result boundaries;
- subsystem-level failure, degradation, migration, and acceptance;
- failure and recovery.

## 03 — Operator Experience and Style Guide

Defines:

- operator mental model;
- navigation;
- surfaces;
- wireframes;
- responsive behavior;
- editing;
- typography;
- themes;
- code blocks;
- interaction;
- loading/error/stale states;
- live acceptance.

## 04 — Feature Memory Ledger

Defines and records:

- the project-wide FML index;
- one canonical detail page per remembered capability;
- descriptive FML identities;
- discovery source and operator need;
- classification and independent lifecycle status;
- target architecture and product releases;
- canonical, workflow, surface, AI, platform, security, and migration impact;
- typed incoming and outgoing interdependencies;
- hard blockers, decision blockers, conflicts, shared foundations, duplicates, and supersession;
- dependency health, cycle detection, and reconciliation;
- deferral, rejection, duplicate, or supersession rationale;
- revisit triggers;
- promotion into Epics, Features, Slices, and delivery chains;
- owners, history, evidence, and current next action.

The ledger begins during project foundation work and remains active for the life of the architecture.

The index is a current projection. Each FML item detail page is the canonical architectural memory for that item.

## 05 — Architecture Smells Seed

Records:

- inherited h00pz architecture smells;
- project-specific smells discovered during design and operation;
- observable symptoms and failure modes;
- smell dispositions;
- accepted ADR exceptions;
- owners and revisit triggers;
- escalation into invariants, forbidden outcomes, defects, or future framework changes.

The seed begins during project foundation work and remains active for the life of the architecture.

## 06 — Chain Delivery Register

Records every active end-to-end delivery chain, including:

- named chain nodes and handoffs;
- specification, implementation, connection, deployment, and evidence states;
- live, fixture, and operator-acceptance frontiers;
- the first blocked handoff;
- disconnected component islands;
- deployed artifact and configuration revisions;
- acceptance evidence;
- the next chain-closing action;
- owner and last verification time.

The register is updated as code merges, deployments occur, live paths are exercised, and operator acceptance advances. It must never infer chain progress from pull request status alone.

## 07 — Delivery Record Index

Indexes the canonical Git-tracked slice, TDD-stage, and pull request delivery reports.

It records:

- descriptive report title and canonical ID;
- report type and state;
- parent feature, slice, TDD, and specification;
- pull request number as metadata where applicable;
- chain frontier effect;
- acceptance status;
- report path;
- owner and last update.

The index is navigational. The individual reports remain the canonical as-built and as-proven delivery records.

## 08 — Epic and Feature Register

Records the canonical scope hierarchy for the project.

It defines:

- Project or Product;
- outcome-bearing Epics;
- operator-visible Features;
- child Slices;
- architecture and product-release placement;
- lifecycle state;
- specification and closing-report references;
- scope additions, removals, deferrals, and supersession;
- links to the Chain Delivery Register without duplicating its node and handoff status.

The register answers what the project is decomposed into. The Chain Delivery Register answers how far the connected live implementation has advanced.

## 09 — Harness Architecture and Evaluation Plan

Defines:

- harness goals, authority, and non-goals;
- harness topology and production-path fidelity;
- applicable contract, workflow, semantic, retrieval, recovery, migration, performance, and operator-acceptance harnesses;
- fixture, recorded-replay, live-isolated, and production-smoke modes;
- case packs, fixtures, rubrics, gates, and baselines;
- run manifests and evidence packages;
- model, prompt, policy, retrieval, schema, source, code, and configuration identity;
- isolation, state control, cleanup, and production safety;
- replay and regression policy;
- harness runbooks, ownership, limitations, and acceptance.

The plan is a standing architecture document. Harness cases and reports evolve with each Feature and Slice rather than being deferred to a final testing phase.


## 10 — Prompt Architecture and Catalog

Defines:

- prompt-system topology and bounded model roles;
- canonical prompt package IDs, versions, hashes, owners, and lifecycle;
- composition layers and instruction precedence;
- context-assembly, trust-domain, token-budget, truncation, and omission contracts;
- tool contracts and deterministic action authority;
- input, output, repair, and evidence contracts;
- model compatibility and routing;
- deployment through Git-tracked assets, ConfigMaps, selectors, and effective revisions;
- semantic calibration, regression packs, promotion gates, rollout, and rollback;
- invocation provenance, observability, and known limitations;
- active, deprecated, retired, and quarantined prompt packages.

The catalog is the canonical navigational record of prompt behavior. Individual prompt-package files remain the canonical executable artifacts.

## 11 — MCP Capability Access and Connector Architecture

Defines:

- shared MCP Gateway topology, ownership, and implementation;
- MCP server identities, boundaries, owners, resources, tools, prompts, and protocol revisions;
- connector registrations, application MCP profiles, and MCP bindings;
- authentication, authorization, credential mediation, token lifecycle, TLS, and network egress;
- trust-domain discovery, invocation, cache, audit, and provenance isolation;
- approved capability snapshots, schema fingerprints, drift review, filtering, disablement, and revocation;
- source, action, internal-capability, and agent-service connector classes;
- side-effect classes, approval, idempotency, retry, rollback, and reconciliation;
- source artifacts, connector compilers, candidates, canonicalization, completeness, and current-versus-history behavior;
- gateway and server availability, scaling, upgrade, rollback, retention, deletion lineage, and runbooks;
- operator surfaces, platform audit, application provenance, harness behavior, and live acceptance;
- Atlas-specific use of the Red Hat/Kuadrant MCP Gateway Operator where applicable.

The standing document records the governed platform and application connector architecture. Individual connector specifications, server contracts, bindings, capability snapshots, and invocation records remain separately versioned artifacts.

## 12 — Agent Runtime and Sandbox Architecture

Defines:

- application control-plane ownership;
- Product Agent Runtime canonical name, ownership classification, namespaces, runtime resources, policy, operational store, and implementation-substrate metadata;
- explicit exclusion of foreign-application and historical runtime resources;
- bounded inference versus agentic execution classification;
- OpenShell Gateway, Supervisor, sandbox, and deployment topology;
- agent-harness ownership and supported execution modes;
- canonical `AgentRun`, `AgentAttempt`, AgentExecutionProfile, SandboxPolicyRevision, AgentCapabilityGrantSet, AgentExecutionManifest, and AgentResultEnvelope contracts;
- process, filesystem, network, credential, inference, and trust-domain policy;
- MCP capability access from inside the sandbox;
- sub-agent delegation and authority attenuation;
- checkpoint, retry, cancellation, stale-work, teardown, cleanup, and residue behavior;
- result validation, side effects, candidates, and canonicalization boundaries;
- runtime audit, application provenance, operator surfaces, harness cases, live acceptance, rollout, rollback, and exceptions;
- h00pz use of OpenShell on OpenShift and its separation from the Red Hat/Kuadrant MCP Gateway Operator.

The standing document is the canonical application-specific instantiation of the AS contract. Individual execution profiles, sandbox-policy revisions, capability-grant sets, manifests, run records, and attempt records remain separately versioned or durably stored artifacts.

## 13 — AI Application Subsystem Architecture

Defines:

- the complete Subsystem Architecture Map;
- subsystem identity criteria and boundary decisions;
- canonical subsystem detail pages;
- domain and application-foundation subsystem ownership;
- owned Features and FML items;
- canonical concepts, writes, current read models, and shared-subject ownership;
- internal ingress-to-operator architecture;
- subsystem-scoped AI roles, prompt packages, context assemblers, agents, tools, and harness packs;
- cross-subsystem request, event, projection, source, and candidate contracts;
- cross-subsystem workflow coordinators;
- operator-surface ownership and composed-workspace behavior;
- logical versus physical deployment decisions;
- subsystem failure, degradation, observability, security, and trust boundaries;
- migration from emergent Feature-first structures;
- subsystem gates, live acceptance, smells, exceptions, and revisit triggers.

The standing document is the canonical current decomposition of the AI application. Individual subsystem detail pages are the canonical architecture records for each subsystem. Feature specifications govern Feature behavior but do not replace subsystem architecture.

## 14 — Current As-Built Architecture

Defines the current implemented and deployed system reality.

It records:

- current subsystem and component inventory;
- ownership-bearing resource names and namespaces;
- canonical and operational stores;
- live runtime, MCP, connector, model-serving, and platform relationships;
- current ingress, workflow, canonical-write, projection, and operator paths;
- active operator surfaces;
- live, fixture, and operator-acceptance frontiers where material;
- active image, model, prompt, policy, schema, configuration, and architecture identities where material;
- known degraded, partial, disconnected, unavailable, temporary, and unimplemented behavior;
- links to the canonical architecture, subsystem, FML, delivery, and acceptance evidence.

The Current As-Built Architecture is distinct from target architecture documents.

Required rule:

```text
Target architecture
→ what the system is intended to become

Current As-Built Architecture
→ what the system actually is now
```

The README architecture-at-a-glance section, when present, is a projection of this document rather than an independently maintained source of truth.

## Repository-level Agent Operating Contract

Every substantial repository must maintain a short canonical Agent Operating Contract, normally `AGENTS.md`.

It governs how agents and contributors work and points to canonical repository truth. It is not numbered as an architecture document because it must not become a competing source of system design, capability state, or deployed reality.

Tool-specific instruction files may project it but must not contradict it.

Before feature specifications may begin:

- the four foundation documents must be accepted;
- the canonical Agent Operating Contract must exist, remain behavioral, and point to the current HASF and repository truth surfaces;
- the initial Current As-Built Architecture must exist, even when its honest initial state is that no product capability has yet been implemented;
- the initial Subsystem Architecture Map, subsystem identity decisions, canonical detail pages, owned Feature placement, canonical ownership, and cross-subsystem contract inventory must be accepted before broad Feature implementation;
- the initial Feature Recall pass must be complete;
- all discovered capabilities must have canonical FML detail pages and be classified in the Feature Memory Ledger;
- all FML interdependencies must be typed, linked, and reviewed for hard blockers, conflicts, and cycles;
- every `required_now` capability must pass the Architecture Weaving Gate;
- the inherited Architecture Smells Seed must be reviewed and every applicable smell must have a disposition;
- the initial build and delivery baseline, target budgets, cache identity, and immutable deployment-verification path must be declared;
- the delivery-report repository structure, templates, and index must exist before the first implementation slice begins;
- the Epic and Feature Register must define the initial scope hierarchy, or explicitly record why the project is small enough to place a Feature directly under the Project;
- the Harness Architecture and Evaluation Plan, initial case catalog, required gate catalog, execution environments, and run-report template must exist before the first implementation Slice begins;
- the Prompt Architecture and Catalog, initial prompt-package identities, context-assembly contracts, model compatibility assumptions, authority boundaries, and prompt evaluation gates must exist before the first AI-backed implementation Slice begins;
- the MCP Capability Access and Connector Architecture, platform inventory, trust-domain policy, connector registration model, application binding model, server-boundary rules, capability-approval lifecycle, and live-path acceptance plan must exist before the first connector-backed implementation Slice begins;
- the Agent Runtime and Sandbox Architecture, OpenShell platform inventory, execution classification, application control-plane boundary, run and attempt model, initial execution profiles, sandbox-policy baseline, trust-domain identity, MCP access path, checkpoint and cleanup contract, operator surface, and live-path acceptance plan must exist before the first agentic implementation Slice begins;
- the AI Application Subsystem Architecture, subsystem map, detail-page template, shared-subject ownership, cross-subsystem contract model, subsystem harness scopes, and migration plan for any emergent Feature-first structures must exist before multiple substantial subsystem Features begin implementation.

---

# 7. Feature Specification Template

Use the following for each substantial feature.

```text
1. Specification identity, canonical name, and filename
2. Project, Epic, Feature, and planned Slice placement
3. Owning application subsystem, participating subsystems, boundary impact, and subsystem detail-page links
4. Summary
5. Operator outcome
6. Governing question
7. Non-goals
8. Conceptual model
9. Canonical ownership
10. State machines
11. Information flow
12. Operator flow
13. Cross-subsystem contracts, workflow coordinator, and shared-subject ownership
14. Chain Delivery Map and handoff contracts, including owning subsystem per node and producer/consumer subsystem per boundary edge
15. Operator surface definitions and subsystem surface-family placement
16. AI/model contract and bounded-inference versus agentic-execution classification
17. Prompt architecture, subsystem context assembly, tool authority, model compatibility, rollout, rollback, and prompt provenance
18. Agent runtime and sandbox architecture, including application control plane, agent harness, OpenShell topology, AgentRun and AgentAttempt, execution profile, sandbox policy, trust domain, network and filesystem boundary, inference route, checkpoint, teardown, result envelope, and live acceptance
19. MCP capability access and connector architecture, including gateway and server ownership, registration, application profile and binding, capabilities, trust domains, credentials, side effects, source artifacts, provenance, and live acceptance
20. Retrieval/freshness
21. Evidence/provenance and shared-source versus subsystem-interpretation boundaries
22. Idempotency/restart
23. Security/privacy
24. Runtime configuration, resource ownership classification, canonical product and platform names, implementation-substrate metadata, foreign and historical resource exclusions, and Kubernetes deployment contract
25. Logical-versus-physical subsystem deployment decision
26. Build, test, image, and delivery impact
27. Harness architecture, subsystem case-pack impact, applicable harness classes, execution modes, gates, replay, and evidence plan
28. Invariants
29. Forbidden outcomes
30. Acceptance plan, including subsystem-boundary, mechanical, semantic, fixture, live-path, agent-runtime, connector, recovery, performance, prompt-behavior, and operator-acceptance gates
31. Capability preflight
32. Named Slice build order and proposed pull request titles
33. Stop rule
34. Feature recall and counterfactual walkthroughs
35. Feature Memory Ledger item pages, subsystem placement, classifications, typed dependencies, blockers, conflicts, cycles, and deferrals
36. Architecture Smells review and seed changes
37. Git-tracked Slice, TDD-stage, pull request, prompt-change, agent-runtime-change, connector-change, subsystem-change, and harness-run delivery-record plan
38. Required End-State Delivery Snapshot fields and closing reconciliation
39. Architecture version impact
40. Open questions
```

---

# 8. Pre-Build Response Required From the Implementer

Before coding, the implementer must return:

1. Canonical specification title, ID, filename, architecture version, and document revision.
2. Project, Epic, Feature, Slice, TDD, and planned pull request traceability.
3. Owning application subsystem, participating subsystems, subsystem boundary impact, canonical detail-page links, shared-subject ownership, and cross-subsystem contracts.
4. Interpretation of the operator outcome.
5. Exact question or workflow being implemented.
6. What the feature is not authorized to do.
7. Canonical objects and owners.
8. Current truth and history model.
9. Complete state machine.
10. Independent state axes.
11. Authority ladder.
12. Projection and consistency model.
13. Correction model.
14. Identity model where relevant.
15. Task lifecycle where relevant.
16. AI/model responsibilities and classification as bounded non-agentic inference or model-controlled agentic execution.
17. Prompt architecture, including prompt package identity, composition, context assembly, authority boundaries, supported models, token budgets, output and repair contracts, deployment, provenance, evaluation, rollout, and rollback.
18. Agent runtime and sandbox architecture where applicable, including application control-plane owner, agent harness, OpenShell Gateway and Supervisor topology, `AgentRun` and `AgentAttempt` lifecycle, AgentExecutionProfile, SandboxPolicyRevision, trust-domain identity, sub-agent behavior, process and filesystem policy, network and egress policy, credentials, inference route, checkpointing, timeout, cancellation, teardown, cleanup, result envelope, canonicalization boundary, operator surfaces, and live acceptance.
19. MCP capability access and connector architecture where applicable, including gateway implementation and topology, server identity and owner, connector registration, application MCP profile and binding, authentication, authorization, credential ownership, network and egress path, trust-domain scope, approved and denied capabilities, schema fingerprints, capability drift, side-effect class, source completeness, source artifacts, connector compiler, canonicalization, platform audit, application provenance, operator surfaces, and live acceptance.
20. Freshness routing.
21. External egress behavior.
22. Idempotency and stale-work behavior, including logical run versus physical attempt identity.
23. Runtime configuration and resource inventory, including ownership classification, canonical product or `platform-` names, namespaces, runtime and gateway names, operational-store classification, implementation-substrate metadata, foreign and historical resource exclusions, environment variables, Secret references, ConfigMap keys or mounted assets, validation, and rollout behavior.
24. Build and delivery impact, including affected components, build graph, cache identity, concurrency, expected timing, image digest, deployment verification, and whether the Slice changes the delivery system.
25. Harness architecture impact, including applicable harness classes, OpenShell, connector and gateway modes, production-path fidelity, cases and fixtures, deterministic and semantic gates, replay packs, run-manifest identity, isolation, cleanup, and evidence retention.
26. Complete Chain Delivery Map covering all load-bearing nodes and handoffs from realistic ingress through application control, sandbox execution, model and MCP calls, result validation, and operator outcome.
27. Initial live, fixture, and operator-acceptance frontiers; expected disconnected islands; first likely blocked handoff; and next chain-closing action.
28. Operator surfaces.
29. Forbidden outcomes.
30. Realistic acceptance workflow and the harness runs that will prove mechanical, semantic, prompt-behavior, agent-runtime, connector-path, live-path, recovery, performance, and operator outcomes separately.
31. Recovery plan.
32. Security plan.
33. Proposed narrow Slice build order with an outcome-bearing title for every planned pull request and its expected chain, prompt, agent-runtime, connector, and harness impact.
34. Explicit non-goals.
35. Feature Recall findings.
36. Counterfactual walkthrough results.
37. Feature Memory Ledger item pages, additions, classification changes, dependency edges, unresolved hard blockers, conflicts, cycles, and affected dependents.
38. Architecture Weaving Gate mapping for every `required_now` capability.
39. Architecture Smells Seed review, including present smells, dispositions, ADR exceptions, and proposed additions.
40. Proposed descriptive paths and lifecycle for the Slice, TDD-stage, pull request, prompt-change, agent-runtime-change, connector-change, and harness-run delivery reports.
41. Required End-State Delivery Snapshot fields and reconciliation owner.
42. Proposed architecture version classification and compatibility reasoning.
43. Remaining contradictions or ambiguities.
44. Canonical repository sources consulted, including the current HASF pointer, applicable architecture and ADRs, owning subsystem detail page, canonical FML item pages, Current As-Built Architecture, Feature specification and plan, Chain Delivery Register, and relevant delivery history.
45. Stale, contradictory, duplicated, or missing truth discovered and the canonical artifact that will be corrected.
46. Complete same-change documentation sweep, including FML, generated projections, Current As-Built Architecture, architecture-at-a-glance, architecture documents, specifications, benchmarks, delivery records, and runbooks affected by the Slice.

Coding begins only after this response is reviewed, the applicable Agent Operating Contract has been followed, the task-relevant canonical repository truth has been consulted and reconciled, the owning subsystem and every participating subsystem boundary are accepted, every cross-subsystem contract and workflow coordinator is explicit, every `required_now` capability passes the Architecture Weaving Gate, every applicable architecture smell has an explicit disposition, the Chain Delivery Map identifies the complete path and every load-bearing handoff, the Epic → Feature → Slice hierarchy and Git-tracked delivery-record paths and lifecycle are declared, the runtime configuration contract is complete enough to prevent production values from being invented in code, the delivery impact is understood well enough to avoid accidental full rebuilds or unverifiable deployments, and the harness plan identifies how the Slice will be proven mechanically, semantically, through the live chain, under failure, and at the operator surface. For AI-backed work, the prompt package, context assembly, tool authority, model compatibility, evaluation pack, deployment identity, rollout, and rollback must also be explicit before coding begins. For agentic work, the application control-plane boundary, OpenShell path, run and attempt model, execution profile, sandbox-policy revision, trust-domain identity, network and filesystem restrictions, inference route, MCP grant set, checkpoint and cleanup behavior, result boundary, and live acceptance must also be explicit. For connector-backed work, the MCP Gateway path, server boundary, connector registration, application binding, capability snapshot, trust-domain policy, credential and egress flow, side-effect behavior, source-artifact path, provenance, and live acceptance must also be explicit. For work inside a multi-subsystem AI application, the subsystem charter, canonical ownership, internal lifecycle, subsystem context and AI roles, operator surface family, cross-subsystem contracts, coordinator, logical-versus-physical boundary, subsystem harness pack, migration impact, and real ingress-to-operator acceptance path must also be explicit.

---

# 9. Narrow Build Order

The framework requires complete design before implementation, but implementation should remain narrow.

Feature work follows:

```text
Specification
→ bounded Plan
→ reviewed Code
```

Sub-agents may implement bounded Feature tasks after the plan is accepted. Review roles constrain their output and the coordinating implementer owns integration.

Operational work that mutates live or shared state remains serial under one accountable controller unless an accepted runbook proves safe parallel execution.

Recommended sequence and naming pattern:

```text
Subsystem foundation and reference path
Example title: Establish <subsystem> boundary, canonical ownership, and reference workflow

Canonical foundation
Example title: Establish canonical <subject> records and invariants

Lifecycle
Example title: Implement guarded <subject> lifecycle transitions

Current read model
Example title: Materialize the current <subject> read model

Operator surface
Example title: Expose <operator action> through the <named surface>

MCP platform baseline and binding
Example title: Verify <gateway platform> and bind <connector> for <specific governed purpose>

Connector source or action path
Example title: Integrate governed <connector capability> through <source artifact or side-effect> handling

AI integration
Example title: Integrate bounded <model> execution for <specific outcome>

Agent runtime profile and sandbox path
Example title: Establish governed OpenShell execution for <specific agent role and outcome>

Prompt package and context assembly
Example title: Establish calibrated <prompt package> behavior for <specific governed outcome>

Harness and regression proof
Example title: Prove <named behavior> through <fixture, replay, live, recovery, or operator> harness gates

Recovery and operations
Example title: Add <workflow> replay, recovery, and observability

Live acceptance closure
Example title: Close <named end-to-end workflow> acceptance gaps
```

These are patterns, not literal pull request names. Every project must replace the placeholders with the actual governed capability and outcome.

Sequence numbers may be recorded separately as implementation metadata. They must not become the pull request identity.

Every planned and merged pull request must also identify:

- the owning subsystem, participating subsystems, subsystem detail pages, and boundary contracts it changes;
- the Chain Delivery Map nodes or edges it changes;
- whether it advances the live frontier;
- whether it creates or removes a disconnected island;
- the fixture, live-path, or operator-acceptance evidence required after deployment;
- the next chain-closing action if the live frontier does not advance;
- the descriptive Git-tracked pull request delivery report it creates or updates;
- the End-State Delivery Snapshot fields it is expected to change;
- the harness cases, execution modes, gates, and run-report evidence it creates or changes;
- the prompt packages, context assemblers, tool contracts, supported models, calibration packs, and prompt-change reports it creates or changes;
- the AgentRun and AgentAttempt records, execution profiles, OpenShell sandbox policies, trust-domain identities, inference routes, checkpoints, result envelopes, runtime operator surfaces, and agent-runtime change reports it creates or changes;
- the MCP gateway routes, connector registrations, MCP server contracts, application profiles and bindings, capability snapshots, trust-domain grants, side-effect classes, source-artifact paths, and connector-change reports it creates or changes.

---

# 10. Documentation Taxonomy

Use twelve complementary documentation types.

## Agent operating instructions

Define stable, imperative working behavior, execution-mode rules, documentation discipline, delegation boundaries, and pointers to canonical repository truth. They do not own project architecture, capability state, delivery state, or deployed reality.

## Architecture specifications

Describe the governed target product and system.

## Current As-Built Architecture

Describes the current implemented and deployed system, including active ownership, components, stores, paths, surfaces, identities, live frontiers, degraded behavior, and known gaps. It must remain distinct from target architecture and scoped plans.

## ADRs

Record major decisions and alternatives.

## Diátaxis user documentation

Use:

- tutorials;
- how-to guides;
- reference;
- explanation.

## Delivery reports

Preserve the as-built and as-proven record for every substantial Epic closure, Feature closure, Slice, TDD stage, TDD, and pull request, including chain impact, deviations, deployment identity, live evidence, failures, acceptance, and a final End-State Delivery Snapshot.

## Harness documentation and run evidence

Define the harness architecture, cases, fixtures, rubrics, baselines, execution environments, run manifests, evidence packages, replay results, regression decisions, and known limitations.

## Prompt architecture and change records

Define prompt packages, composition, context assembly, model compatibility, tool authority, schemas, calibration, deployment, active revisions, change classification, replay evidence, rollout, rollback, and known limitations.

## MCP capability access and connector architecture records

Define MCP Gateway topology, connector registrations, MCP server contracts, application profiles and bindings, capability snapshots, schema fingerprints, trust-domain grants, credential and egress paths, source-artifact and side-effect behavior, provenance, capability drift, revocation, live acceptance, rollout, rollback, and known limitations.

## Agent runtime and sandbox architecture records

Define application control-plane boundaries, OpenShell Gateway and Supervisor topology, agent harnesses, AgentRun and AgentAttempt lifecycles, execution profiles, sandbox-policy revisions, trust-domain identities, process, filesystem, network, credential, inference, checkpoint, teardown, cleanup, result, sub-agent, provenance, rollout, rollback, and live-acceptance behavior.

## AI application subsystem architecture records

Define the Subsystem Architecture Map, canonical subsystem detail pages, subsystem boundaries, owned Features and FML items, canonical ownership, shared-subject identity, internal ingress-to-operator architecture, AI and context roles, cross-subsystem contracts, workflow coordination, operator-surface ownership, logical-versus-physical decomposition, migration, harness scope, failure isolation, and live acceptance.

## Runbooks

Describe:

- deployment;
- backup;
- restore;
- rebuild;
- incident response;
- migration;
- connector and MCP server recovery;
- MCP Gateway failover, upgrade, rollback, capability revocation, credential rotation, and binding reconciliation;
- OpenShell Gateway recovery, sandbox cleanup, policy rollback, stuck-attempt reconciliation, credential-provider recovery, inference-route recovery, and cross-domain isolation incident response;
- model restart;
- build-cache invalidation and recovery;
- delivery-pipeline and stale-digest recovery;
- harness local, cluster, live-model, cleanup, and failed-run recovery;
- prompt rollout, rollback, active-revision verification, ConfigMap recovery, and model-fallback recovery.

Do not mix these into one giant document.

---

# 11. Repository Layout

Recommended:

```text
AGENTS.md
CLAUDE.md                         # optional tool-specific projection of AGENTS.md

docs/
  00-primer.md
  01-architecture-constitution.md
  02-system-architecture.md
  03-operator-experience-style-guide.md
  04-feature-memory-ledger.md
  fml/
    fml-item-template.md
    items/
      fml-<descriptive-capability-slug>.md
  05-architecture-smells-seed.md
  06-chain-delivery-register.md
  07-delivery-record-index.md
  08-epic-feature-register.md
  09-harness-architecture-evaluation-plan.md
  10-prompt-architecture-and-catalog.md
  11-mcp-capability-access-and-connector-architecture.md
  12-agent-runtime-and-sandbox-architecture.md
  13-ai-application-subsystem-architecture.md
  subsystems/
    subsystem-detail-template.md
    <canonical-subsystem-id>.md
    contracts/
    diagrams/
    migrations/

  adr/
  specs/
  delivery/
    <feature-or-program-id>/
      slice-reports/
      tdd-reports/
      pr-reports/
  agent-runtime/
    execution-profiles/
    sandbox-policies/
    capability-grants/
    execution-manifests/
    change-reports/
  prompts/
    catalog/
    packages/
    context-assemblers/
    tool-contracts/
    calibration/
    change-reports/
  harness/
    case-catalog/
    case-packs/
    baselines/
    run-reports/
    fixtures/
    rubrics/
    manifests/
  releases/
  branches/
  forks/
  diagrams/
  runbooks/
  user/
  archive/
```

---

# 12. Document and Architecture Versioning

Document versioning and architecture versioning are distinct.

A document revision may correct wording without changing the architecture version. An architecture version changes only when the governed operator, semantic, workflow, ownership, or trust contract changes as defined in **AH. Architecture Evolution, Versioning, and Forking**.

For any reviewed revision:

- identify the parent document and architecture version;
- classify the change as editorial, patch, minor, major, branch, or fork;
- create a new version rather than overwriting the accepted source;
- preserve the prior version during review;
- compare the versions side by side;
- update the Feature Memory Ledger and Architecture Release Packet where required;
- accept the new version explicitly;
- archive the superseded version;
- clean canonical filenames separately.

Do not erase architecture history during active review.

Do not represent an editorial document update as a new architecture release.

Do not represent a semantic compatibility break as a minor document revision.

Agent operating instruction projections and stable current-document pointers must be reconciled whenever their referenced canonical release, path, stack baseline, or behavior contract changes.

The Current As-Built Architecture is updated as implementation reality changes. Its document revision does not by itself imply an architecture-version change.

---

# 13. Review Roles

A mature architecture review should include distinct hats:

- product/operator reviewer;
- skeptical new joiner;
- state-integrity reviewer;
- AI application subsystem boundary, ownership, and contract reviewer;
- security/privacy reviewer;
- feature-memory and omission reviewer;
- architecture-smell reviewer;
- runtime-configuration and deployment reviewer;
- resource ownership, naming, and foreign-infrastructure reviewer;
- build-performance and delivery-safety reviewer;
- chain-integrity and handoff reviewer;
- delivery-record and as-built-history reviewer;
- agent-operating-contract and repository-truth reviewer;
- current-as-built architecture reviewer;
- evolution and compatibility reviewer;
- harness architecture, semantic evaluation, and replay reviewer;
- prompt architecture, context assembly, and model-behavior reviewer;
- MCP gateway, server-boundary, connector-security, and capability-governance reviewer;
- agent runtime, OpenShell sandbox, execution-policy, trust-domain, and sub-agent reviewer;
- KISS reviewer.

One person may wear multiple hats, but the questions must all be asked.

---

# 14. Quality Bar

A specification is ready for implementation when:

- the Agent Operating Contract is short, behavioral, stable, and points to canonical repository truth rather than duplicating it;
- applicable tool-specific instruction files agree with the canonical operating contract;
- the current HASF pointer is valid and any embedded version or stack assertions are current;
- the Current As-Built Architecture exists and accurately distinguishes deployed reality from target architecture and scoped plans;
- task-relevant architecture, ADR, FML, current-state, specification, delivery, and evidence sources have been consulted and contradictions reconciled;
- the operator outcome is explicit;
- the conceptual model is coherent;
- the Subsystem Architecture Map is coherent and every Feature has one owning subsystem;
- every substantial subsystem has an accepted charter, detail page, operator outcome, internal lifecycle, surface family, harness scope, and cross-subsystem contracts;
- shared subjects have one canonical identity owner and subsystem-specific meaning remains locally owned;
- cross-subsystem workflows have a durable coordinator and cross-boundary writes occur only through governed contracts;
- logical subsystem boundaries are explicit regardless of whether deployment is monolithic or distributed;
- every material runtime resource has an ownership classification and ownership-bearing canonical name;
- product-owned capabilities use product identity and intentionally shared capabilities use an accepted `platform-` identity;
- implementation frameworks, vendors, databases, and protocols remain metadata rather than primary capability names;
- foreign-application and historical resources are explicitly excluded or governed by an accepted transfer or migration decision;
- application-specific runtime, sandbox, session, checkpoint, and framework state is classified non-canonical where appropriate;
- canonical ownership is unambiguous;
- current and history are separated;
- retries cannot corrupt state;
- projections are rebuildable;
- corrections survive regeneration;
- identity behavior is safe;
- tasks have provenance;
- AI roles are bounded;
- every production prompt has a stable package ID, version, content hash, owner, lifecycle, and supported-model contract;
- prompt composition and instruction precedence are explicit;
- context assembly defines trust domains, source precedence, token budgets, truncation, omissions, and current-versus-history behavior;
- tool and action permission is enforced deterministically outside the prompt;
- untrusted source content is treated as data rather than instruction;
- prompt assets are Git-tracked and deployed through a governed ConfigMap or immutable artifact path;
- prompt, model, policy, context, tool, schema, and effective-configuration provenance is recoverable for every material AI result;
- prompt and model changes replay affected semantic, injection, truncation, repair, tool-failure, and live-path cases;
- prompt rollout and rollback identify the exact active package and content hash;
- repair and fallback are bounded and cannot broaden authority or invent evidence;
- every AI capability is explicitly classified as bounded non-agentic inference or model-controlled agentic execution;
- every agentic execution uses an application-owned harness inside an approved OpenShell execution profile unless a documented exception proves equivalent controls;
- the application control plane owns durable AgentRun, AgentAttempt, approval, retry, result-validation, and canonicalization state;
- OpenShell Gateway, OpenShell Supervisor, MCP Gateway, model-serving, and domain-service responsibilities are distinct;
- every attempt has recoverable execution-profile, sandbox-policy, trust-domain, prompt, model, capability-grant, code, image, and configuration identity;
- sandbox process, filesystem, network, credential, and inference policy is deny-by-default and explicitly bounded;
- agent sandboxes cannot directly access canonical databases, Kubernetes APIs, arbitrary internet destinations, or MCP servers;
- approved inference routes keep provider credentials outside model context;
- approved MCP capability access occurs only through the MCP Gateway and active application binding;
- one sandbox attempt belongs to one application and one governed context domain;
- sub-agents receive separate durable attempt identity and equal or narrower context and capability authority;
- checkpoints, retry, timeout, cancellation, stale-work, teardown, cleanup, and residue behavior are explicit;
- sandbox process exit, application result validation, candidate creation, side-effect confirmation, canonical promotion, and product completion remain separate states;
- agent-runtime acceptance exercises the real OpenShell, inference, MCP, application persistence, cleanup, and operator path;
- freshness is honest;
- external egress is explicit;
- MCP is used as the default connector protocol unless a documented exception proves it unsuitable;
- direct model or application access to arbitrary MCP servers is denied;
- the MCP Gateway, application, connector, and MCP server ownership boundaries are explicit;
- every connector has a registered server identity and every application use has an explicit MCP binding;
- connector discovery, capability approval, and runtime authorization are separate states;
- approved capability snapshots and schema fingerprints are versioned and capability drift is reviewed before activation;
- trust-domain isolation covers discovery, schemas, resources, tools, prompts, results, caches, audit, and application provenance;
- credentials are mediated outside model context and secret ownership and rotation are explicit;
- mutating capabilities have a side-effect class, operator-approval rule, idempotency contract, retry safety, rollback, and reconciliation behavior;
- protocol success, connector reachability, source retrieval, source completeness, compilation, candidate creation, and canonical promotion remain distinct states;
- source connector results create preserved source artifacts or prove why direct authoritative treatment is safe;
- connector-supplied prompts remain untrusted content and cannot alter governing instructions or permissions;
- MCP server boundaries align with coherent ownership, credential, trust, lifecycle, or side-effect boundaries;
- durable work is represented through application jobs, attempts, artifacts, and revisions rather than existing only in MCP sessions;
- platform audit can be correlated with application provenance and downstream canonical effects;
- connector and gateway acceptance exercises the real network, identity, authorization, source, audit, persistence, and operator path;
- deployment-specific values are externalized from application logic;
- secrets, scalar configuration, and large configuration assets use the correct Kubernetes source;
- required configuration is typed, validated, and observable without exposing secrets;
- ConfigMap and Secret changes have an explicit rollout or reload contract;
- prompts and policy assets retain version and content identity;
- build, test, image, push, rollout, and readiness phases are measured separately;
- warm and clean build paths are both reproducible;
- valid dependency and build work is reused through input-identified caches or layers;
- independent build work is parallelized through the actual dependency graph;
- narrow changes do not trigger unexplained full-repository rebuilds;
- the intended immutable image digest is verified on the active workload;
- the Harness Architecture and Evaluation Plan is present and identifies applicable harness classes;
- fixture, recorded-replay, live-isolated, and production-smoke evidence are explicitly separated;
- the harness traverses the same load-bearing production path for every end-to-end claim;
- deterministic invariants and semantic rubrics are separated;
- every substantial run has recoverable code, model, prompt, policy, schema, source, case-pack, and effective-configuration identity;
- required skipped, blocked, disabled, or inconclusive gates cannot produce a green result;
- harness state, isolation, cleanup, and failed-run residue are controlled;
- model, prompt, policy, retrieval, schema, and context-assembly changes replay the affected packs;
- escaped defects and material flyswatting lessons become durable cases or explicit non-reproducibility records;
- performance harnesses use representative context, retrieval, concurrency, and end-to-end workflow conditions;
- test-only shortcuts cannot become undocumented production paths;
- the complete Chain Delivery Map is present;
- every load-bearing handoff has an owner and contract;
- live, fixture, and operator-acceptance frontiers are named separately;
- disconnected component islands are visible;
- the first blocked handoff and next chain-closing action are explicit;
- no completion percentage substitutes for contiguous live-path evidence;
- every Chain Delivery node names its owning subsystem and every boundary edge names producer and consumer subsystems;
- subsystem-local success is not reported as application-chain completion while a required boundary handoff remains unproven;
- every Epic and Feature has an outcome-bearing identity and explicit parent scope;
- every Slice is vertically meaningful and states the chain frontier it advances;
- every TDD and pull request identifies the Epic, Feature, and Slice it serves;
- every substantial slice, TDD stage, and pull request has a descriptive Git-tracked delivery report;
- affected canonical documentation, FML detail pages, generated projections, Current As-Built Architecture, architecture-at-a-glance, specifications, benchmarks, and runbooks move in the same change as implementation;
- reports distinguish intended, implemented, deployed, live-proven, and operator-accepted state;
- as-built deviations, failures, and flyswatting are preserved as institutional memory;
- the Delivery Record Index and parent roll-up reports link to all material child records;
- every substantial report ends with a reconciled End-State Delivery Snapshot;
- every material in-scope capability appears as implemented, incomplete, broken, deferred, removed, or not implemented;
- the Epic and Feature Register records scope decomposition without competing with current chain status;
- ephemeral evidence links are accompanied by a durable summary of what they prove;
- build and delivery budgets and regression ownership are explicit;
- surfaces are fully defined;
- failure states are visible;
- forbidden outcomes have fixtures;
- acceptance is realistic;
- non-goals are explicit;
- the Feature Recall pass is complete;
- every remembered capability has a canonical FML detail page, classification, and owning subsystem or explicit subsystem-candidate decision;
- FML interdependencies are typed, linked, current, and free of unresolved hard cycles;
- every `required_now` capability is woven through the architecture;
- deferred capabilities have explicit revisit triggers;
- the architecture version impact is classified correctly;
- the Architecture Smells Seed has been reviewed;
- every present smell is resolved, assigned for action, or explicitly accepted by ADR with a revisit trigger;
- newly discovered recurring smells have been added to the project seed;
- the specification has a stable, outcome-bearing canonical name;
- every planned pull request has a descriptive capability-and-outcome title;
- no specification or pull request relies on a sequence number as its identity;
- no runtime or infrastructure resource relies on an ambiguous framework-only, database-only, or shared-sounding name;
- the build order is narrow;
- the stop rule is clear.

---

# 15. Final Governing Rules

1. **Start with the operator.**
2. **Define semantics before services.**
3. **One concern, one canonical owner.**
4. **Preserve source; regenerate derived state.**
5. **Corrections must survive reprocessing.**
6. **Current truth and history must never blur.**
7. **Projections are not canonical.**
8. **AI output is not automatically truth.**
9. **A completed worker is not a completed product.**
10. **Unknown is better than fabricated.**
11. **Operator surfaces are part of correctness.**
12. **Every asynchronous path needs idempotency.**
13. **Every external path needs an egress contract.**
14. **Every important state needs an honest failure mode.**
15. **Every major decision deserves an ADR.**
16. **Every feature needs forbidden outcomes.**
17. **Every build needs a stop rule.**
18. **Share capabilities, never application knowledge.**
19. **Design comprehensively; implement narrowly.**
20. **KISS wins unless simplicity would violate correctness.**
21. **Assume important features will be forgotten; recall them deliberately.**
22. **A named feature is not included until it is woven through semantics, workflow, surfaces, and acceptance.**
23. **Every remembered capability requires its own canonical FML detail page.**
24. **FML dependencies must be typed, linked, and reconciled before weaving or closure.**
25. **Deferred capabilities must remain visible in the Feature Memory Ledger.**
26. **Version architecture by semantic compatibility, not implementation effort.**
27. **Branch temporarily; fork only when incompatible architectural truth must coexist.**
28. **Names are durable architecture metadata.**
29. **Sequence is metadata, never identity.**
30. **Every specification and pull request name must state the capability and outcome it governs.**
31. **Architecture smells are named early warnings, not vague opinions.**
32. **Every present smell needs a disposition, owner, and escalation or revisit path.**
33. **Repeated failure patterns must become shared architectural memory.**
34. **Deployment-specific values belong to Kubernetes configuration, not application logic.**
35. **Use environment variables for scalar runtime configuration, Secrets for sensitive values, and ConfigMap-mounted files for large or structured non-secret configuration.**
36. **Configuration may tune bounded operation; it must not silently redefine canonical semantics or bypass invariants.**
37. **Every configuration change needs validation, an effective revision, and a declared rollout or reload path.**
38. **Build feedback time is an architectural quality, not merely a developer convenience.**
39. **Parallelize the real build graph; do not serialize independent work by habit.**
40. **Reuse expensive work only when its complete input identity proves the cache is valid.**
41. **Preserve a deterministic clean-build path even when the normal path is accelerated.**
42. **Build once, deploy an immutable digest, and verify that the intended digest is active.**
43. **A runtime configuration change should not force an application rebuild when Kubernetes owns the value.**
44. **Component completion is not chain completion.**
45. **Every substantial TDD must expose a Chain Delivery Map.**
46. **The live frontier, first blocked handoff, disconnected islands, and next chain-closing action are the governing progress signals.**
47. **A pull request merge does not prove connection, deployment, live traversal, or operator acceptance.**
48. **Track nodes and handoffs independently; the spaces between components are part of the architecture.**
49. **Fixture, live-path, and operator-acceptance frontiers must never be conflated.**
50. **Every substantial slice, TDD stage, and pull request must leave a canonical Git-tracked delivery report.**
51. **Specifications record intent; delivery reports record as-built and as-proven reality.**
52. **The Chain Delivery Register records current position; delivery reports preserve how that position was reached.**
53. **Merge, deployment, live proof, and operator acceptance must remain distinct in delivery records.**
54. **Flyswatting is institutional knowledge only when its cause, fix, and governing lesson are preserved in Git.**
55. **Use Epics and Features to decompose operator outcomes, not to create administrative buckets.**
56. **A Feature must have an independent operator outcome; a component or endpoint is not automatically a Feature.**
57. **A Slice must advance a meaningful vertical chain frontier.**
58. **TDDs and pull requests are execution artifacts; merge counts do not define Feature or Epic completion.**
59. **Every substantial delivery artifact must trace to its Project, Epic, Feature, and Slice.**
60. **Every substantial Slice, TDD stage, TDD, pull request, Feature closure, and Epic closure report must end with an End-State Delivery Snapshot.**
61. **The End-State Delivery Snapshot is the canonical historical closing state; the Chain Delivery Register remains canonical for current project status.**
62. **Every material in-scope capability must be explicitly classified as implemented, incomplete, broken, deferred, removed, or not implemented.**
63. **No completion percentage may replace the holistic implemented-versus-unimplemented account.**
64. **The harness is part of the architecture, not an after-the-fact testing utility.**
65. **Mechanical correctness, semantic quality, production-chain traversal, recovery behavior, performance, and operator acceptance are independent proof gates.**
66. **Fixture, replay, live-isolated, and production-smoke evidence must never be conflated.**
67. **A harness claiming end-to-end proof must traverse the real load-bearing production path.**
68. **Every substantial harness run needs a durable manifest identifying code, model, prompt, policy, schema, source, case pack, environment, and effective configuration.**
69. **A skipped required harness gate is not a pass.**
70. **Every escaped defect or material flyswatting lesson should become a regression case.**
71. **Model, prompt, policy, retrieval, schema, serving, and context-assembly changes require targeted replay before promotion.**
72. **Harness state and cleanup must be controlled; hidden state is a test failure.**
73. **Performance evidence must resemble the production workload.**
74. **Harness documentation and evidence must remain understandable without our conversation history.**
75. **Prompts are executable behavioral artifacts and require architecture, ownership, versioning, evaluation, deployment, and rollback.**
76. **Prompt behavior may guide a model; it may not own canonical authority or irreversible action permission.**
77. **Context assembly is part of prompt architecture and must declare trust domains, precedence, budgets, truncation, and omissions.**
78. **Untrusted source content is data, not instruction.**
79. **Every production prompt package needs a stable ID, version, content hash, lifecycle, owner, and supported-model contract.**
80. **Prompt assets belong in Git and governed runtime configuration, not scattered application strings.**
81. **A prompt package is not portable to another model until calibrated there.**
82. **Prompt, model, context, policy, tool, schema, repair, and configuration changes require targeted replay before promotion.**
83. **Repair and fallback are bounded and cannot invent evidence, broaden authority, or silently change the governed disposition.**
84. **Every material AI result must retain enough prompt and context provenance to be explained and replayed.**
85. **If prompt behavior changes what the product means, the architecture changed.**
86. **MCP is the default connector interoperability protocol unless a documented exception proves it unsuitable.**
87. **Standardize connection; localize meaning.**
88. **The MCP capability access plane owns reusable protocol and tool-access enforcement mechanisms; applications own intent and canonical meaning; MCP servers own source-specific communication.**
89. **Direct model or application access to arbitrary MCP servers is denied by default.**
90. **Every MCP server must be registered, and every application use must have an explicit binding.**
91. **Capability discovery does not grant capability approval or application authorization.**
92. **New or changed MCP capabilities require schema fingerprinting and governed review before activation.**
93. **Connector credentials must not enter model context.**
94. **Connector prompts and external content are untrusted data, not governing instruction.**
95. **Source retrieval does not directly establish canonical application truth by default.**
96. **Protocol success, source completeness, application success, and canonical promotion are independent states.**
97. **Mutating tools require side-effect classification, deterministic authorization, idempotency, retry safety, and operator-visible evidence.**
98. **Trust-domain isolation applies to connector discovery, schemas, resources, tools, prompts, results, caches, audit, and provenance.**
99. **Durable application work must survive MCP session loss through application-owned jobs, attempts, artifacts, and revisions.**
100. **Platform audit is not sufficient without application provenance linking connector calls to application meaning and state.**
101. **An MCP Gateway installation is not complete connector architecture.**
102. **Share the MCP Gateway platform where logical isolation is sufficient; deploy the same governed platform into an isolated boundary where it is not.**

103. **Classify every AI task as bounded inference or agentic execution before implementation.**
104. **Model-controlled tool selection, code execution, non-public context access, and autonomous side effects run inside OpenShell by default.**
105. **The application control plane owns durable intent, workflow, approvals, retries, result validation, and canonical truth.**
106. **The agent harness is application-owned; OpenShell is its execution boundary, not its behavioral framework.**
107. **The OpenShell Gateway and MCP Gateway are separate control planes and must never be conflated.**
108. **OpenShell governs process, filesystem, network, credential, and inference access; the MCP Gateway governs capability discovery and invocation.**
109. **Network reachability is not tool authorization, and tool authorization is not business authorization.**
110. **Every logical AgentRun and physical AgentAttempt requires durable application identity.**
111. **Every AgentAttempt binds to one immutable execution manifest.**
112. **A sandbox session or filesystem is never the only record that consequential work exists.**
113. **One sandbox attempt belongs to one application, one trust domain, and one bounded capability envelope.**
114. **Sub-agents receive separate attempt identity and equal or narrower authority by default.**
115. **The model, prompt, or connector content may not select or widen its own execution profile, sandbox policy, trust domain, or capability grant.**
116. **Agent sandboxes deny direct canonical-store, Kubernetes API, arbitrary internet, and direct MCP-server access by default.**
117. **Inference credentials remain behind the governed OpenShell route wherever possible.**
118. **Connector credentials remain behind the MCP Gateway or MCP server and never enter model context.**
119. **Agent output is a result envelope requiring application validation, not automatic canonical truth.**
120. **Retry creates a new attempt; stale, canceled, lost, or timed-out attempts cannot create new side effects or promotions.**
121. **Checkpoint, cancellation, timeout, teardown, cleanup, and residue are first-class runtime states.**
122. **Sandbox process completion, application completion, side-effect confirmation, canonical promotion, and operator acceptance remain distinct.**
123. **OpenShell is centrally governed as a platform substrate; each application owns its Product Agent Runtime capability, and gateway instances are partitioned wherever trust, identity, inference-route, credential, audit, quota, ownership, or failure isolation is unproven.**
124. **Agent-runtime evidence must correlate application, OpenShell, MCP, model-serving, and domain-service identities.**
125. **A realistic agentic acceptance case must traverse the actual application → OpenShell → model/MCP → result validation → operator path.**

126. **Architect the AI application as explicit bounded subsystems before broad Feature implementation.**
127. **Every Feature has one owning application subsystem.**
128. **Every canonical concern has one owning subsystem; other subsystems consume contracts or own distinct local interpretation.**
129. **A page, service, model, agent, prompt, queue, collection, repository, or deployment is not automatically a subsystem.**
130. **Subsystems own operator outcomes and application meaning; shared platforms own reusable mechanism.**
131. **Subsystems integrate through versioned requests, events, projections, source handoffs, or candidates—not shared mutable stores.**
132. **Cross-subsystem canonical mutation is denied.**
133. **Shared subjects retain one canonical identity owner.**
134. **Shared source does not imply shared interpretation or shared canonical conclusion.**
135. **Cross-subsystem context requires owner, revision, freshness, trust-domain, omission, and provenance contracts.**
136. **AI roles, prompts, context, tools, agents, and evaluation packs are scoped to subsystem outcomes.**
137. **Cross-subsystem workflows require a durable coordinator that survives model, process, connector, and sandbox loss.**
138. **Logical subsystem boundaries come before physical service boundaries.**
139. **A subsystem is not complete until its real ingress-to-operator path and required boundary handoffs are proven.**
140. **FML records remembered capability; the Subsystem Architecture Map records accepted application responsibility and ownership.**
141. **Runtime and infrastructure names identify the owning product or intentionally shared platform capability.**
142. **Frameworks, vendors, protocols, databases, and libraries are implementation metadata, not primary product capability identities.**
143. **The `platform-` prefix is earned through an accepted shared-platform architecture, not by physical cluster location.**
144. **Foreign-application and historical resources are excluded by default and cannot be rehabilitated through renaming.**
145. **Application-specific operational runtime state remains non-canonical and subordinate to application-owned workflow and truth.**
146. **A required FML item without a subsystem home or explicit subsystem-creation decision is not ready to weave.**
147. **Existing Feature-first architectures are mapped and migrated incrementally rather than rewritten blindly.**
148. **If a Feature cannot be placed cleanly, the subsystem architecture is not ready for that Feature.**
149. **If no subsystem owns the meaning of a result, the application does not own that result coherently.**
150. **Agent operating instructions govern behavior; canonical repository artifacts govern truth.**
151. **HASF governs method; it does not replace project-specific architecture or current-state records.**
152. **Keep persistent agent rules small, imperative, stable, and linked to canonical sources.**
153. **Conversation history and model memory are not canonical project truth.**
154. **Feature work follows Spec → Plan → Code.**
155. **Sub-agents implement bounded plans; reviews constrain them; the coordinating implementer owns integration.**
156. **Operational mutation remains serial under one accountable controller by default.**
157. **Documentation and implementation move together in the same change.**
158. **Canonical FML detail pages own capability truth; indexes and tiered deployment orders are projections.**
159. **After every successfully implemented FML item, regenerate the complete tiered deployment order from the reconciled canonical graph before selecting the next FML.**
160. **The Current As-Built Architecture owns implemented and deployed reality; target architecture does not.**
161. **Specifications and plans describe intended scoped work; the Chain Delivery Register describes current connected progress.**
162. **Stable repository pointers are preferred; embedded version and baseline assertions must be updated atomically.**
163. **A shipped capability updates its FML truth, current as-built truth, architecture-at-a-glance projection, and every affected governing document.**
164. **If the repository cannot tell a new agent what is true without conversation history, the documentation architecture is incomplete.**

---

# 16. The h00pz Test

Before approving any architecture, ask:

```text
Can a new engineer understand it without our conversation history?

Can an implementation agent learn how to work from a short operating contract and retrieve what is true from canonical repository artifacts?

Does any agent instruction file duplicate architecture, FML, delivery, or deployment truth that belongs elsewhere?

After the most recently implemented FML, was the complete tiered deployment order regenerated from reconciled item truth and dependencies before the next item was selected?

Do all tool-specific instruction files agree with the canonical Agent Operating Contract?

Is the current HASF reference or stable pointer correct?

Does the Current As-Built Architecture describe what is actually implemented and deployed rather than what is merely planned?

Would losing the current chat or model memory remove any architecture-bearing fact that the repository cannot reconstruct?

Did the active Feature follow Spec → Plan → Code?

Were sub-agents bounded by the accepted plan, and did operational mutation remain serial?

Did implementation and every affected canonical document move together?

Can that engineer name the application subsystems, their operator outcomes, their canonical ownership, and every cross-subsystem contract?

Can that engineer determine the owner and capability of every material runtime resource from its name and architecture metadata?

Can that engineer distinguish product-owned resources, intentionally shared `platform-` capabilities, foreign-application infrastructure, and historical artifacts?

Does every Feature and required FML item have one owning subsystem or an explicit subsystem-creation decision?

Are we architecting a subsystem, or merely accumulating pages, workers, prompts, agents, and collections that look related?

Can the operator tell what is true now?

Can every important result be traced to its source?

Can retries, failures, and stale work corrupt current truth?

Can reprocessing destroy operator corrections?

Can the UI imply more certainty than the system has?

What capability will the operator obviously ask for next, and have we supported it, preserved optionality for it, or explicitly rejected it?

Can every FML item explain its architectural impact, current disposition, dependencies, and next action from one canonical detail page?

Can we identify every hard FML dependency, blocked item, conflict, cycle, and downstream dependent without reading free-form notes?

Has every remembered `required_now` capability been woven into canonical semantics, workflow, surfaces, failure behavior, and acceptance?

Can we remove 20% without losing the core outcome?

Does every piece of complexity solve a real problem?

Would we still choose this design after six months of use?

Can prior canonical truth still be interpreted correctly under the proposed architecture version?

Are we creating a fork because incompatible truths must coexist, or because we are avoiding a difficult decision?

Can a new engineer understand the specification from its title and filename alone?

Would every pull request title remain meaningful six months later without its sequence number, ticket, or conversation context?

Which inherited architecture smells are present, and does each have a disposition?

What are we calling temporary, and where is its removal trigger?

Where does a realistic subject stop in the deployed chain today?

At which subsystem boundary does it stop, and which subsystem owns that handoff?

Could any subsystem directly mutate another subsystem's canonical truth or inspect its internal store without a contract?

Does any shared model, agent, context assembler, dashboard, or platform component own application meaning that belongs inside a subsystem?

Would the same subsystem boundaries remain valid if the application moved from a modular monolith to separate services, or are the boundaries merely deployment artifacts?

What is the first blocked handoff, who owns it, and what evidence will prove it closed?

Which completed capabilities are disconnected islands rather than part of the live path?

Are fixture, live-path, and operator-acceptance frontiers reported separately?

What is the smallest next action that advances the contiguous operator-visible chain?

Did this work reveal a recurring smell that the project or governing framework must remember?

Could this deployment move to another namespace, cluster, model endpoint, or database without changing application code?

Are any credentials, service URLs, database identities, prompts, policies, feature flags, limits, or retry budgets hard-coded where Kubernetes should own them?

Can we prove which ConfigMap, Secret, prompt, policy, and effective configuration revision produced a given result?

Could an environment variable bypass a semantic invariant or safety boundary?

Which phases dominate the change-to-live feedback loop, and do we have evidence rather than intuition?

Are independent build tasks using available compute, or are we paying for a serialized graph?

Can a narrow source change reuse valid dependencies and avoid rebuilding unaffected components?

Can a clean environment reproduce the same artifact without hidden local state?

Can we prove that the intended immutable image digest—not merely a tag—reached the active workload?

Would a prompt, policy, endpoint, or feature-flag change trigger an unnecessary application rebuild?

Can a new engineer reconstruct what each slice, TDD stage, and pull request actually delivered without reading our chat history?

Does the repository distinguish planned, implemented, deployed, live-proven, and operator-accepted work?

Does every material delivery report state the chain frontier before and after, the first blocked handoff, and the next chain-closing action?

Did we preserve the failures and flyswatting that changed the design, or only the final successful code?

If external CI, pull request, or screenshot links disappeared, would the Git-tracked report still explain what was proven?


Does every Epic name one coherent operator outcome rather than acting as a grab bag?

Can every Feature explain the independent operator capability it owns?

Does every Slice advance a named chain frontier rather than merely complete a technical layer?

Can every TDD and pull request identify the Epic, Feature, and Slice it serves?

Does the latest substantial delivery report end with one holistic End-State Delivery Snapshot?

Does that snapshot clearly separate implemented, connected, deployed, live-proven, broken, deferred, removed, and not-implemented scope?

Are we using the Chain Delivery Register for current truth and historical snapshots only for point-in-time evidence?

Which harness class proves each load-bearing behavior: contract, workflow, semantic, retrieval, recovery, migration, performance, or operator acceptance?

Does the harness traverse the same API, queue, worker, state machine, canonical write, projection, retrieval, model, and surface path used in production?

Are deterministic fixture, recorded replay, live isolated, and production smoke results labeled separately?

Can every harness result be tied to an exact code digest, model, prompt, policy, schema, source snapshot, case-pack version, environment, and effective configuration?

Could a skipped, disabled, blocked, or inconclusive required gate still produce a green summary?

Are we testing governed meaning and evidence, or merely exact generated wording?

What hidden state, cache, lease, projection, or prior record could contaminate the next run?

Did every escaped defect and material flyswatting lesson become a durable replay or regression case?

Does the performance harness resemble real context sizes, retrieval fan-out, concurrency, queueing, and operator-perceived latency?

Can a new engineer run the harness, interpret the gates, locate the evidence, and clean up safely without our conversation history?

Does every production AI behavior identify a canonical prompt package rather than an anonymous string?

Can we reconstruct the exact instruction layers, context sources, omissions, model, tools, policy, repair path, and configuration that produced a material result?

Could untrusted source content be interpreted as instruction or gain access to tools, secrets, another trust domain, or canonical writes?

What happens when required context does not fit, and can the output still claim completeness?

Is tool permission enforced deterministically, or are we trusting the model to obey a sentence?

Has this prompt package passed semantic, injection, truncation, repair, fallback, and live-path cases on the actual serving model?

Can we activate and roll back the prompt independently while proving the exact content hash in use?

Would changing this prompt alter governed meaning, authority, or lifecycle behavior enough to require a Feature or architecture revision?

Can any model or application bypass the governed gateway and invoke an arbitrary MCP server directly?

Can we explain which responsibilities belong to the gateway platform, the application, and each MCP server without overlap or gaps?

Does every connector have a registered server identity, an application MCP profile, and an explicit binding for its governed purpose?

Could a connector or another trust domain become discoverable merely because it shares a physical gateway?

Can a newly advertised or changed resource, tool, prompt, or schema become active without review?

Are connector credentials, tokens, and upstream secrets kept out of model context and application logs?

Could connector-supplied prompts or returned content alter governing instructions, permissions, or canonicalization?

Does a successful connector call prove only protocol execution, or are source completeness and application success measured separately?

Can every consequential connector result be traced from platform audit through application source artifacts, candidates, reconciliation, and canonical effects?

Could a non-idempotent side effect be retried twice or replayed after stale work without detection?

Would MCP session loss erase the only record that durable work exists?

Does the MCP server boundary match a coherent source, credential, trust, lifecycle, or side-effect boundary?

Can the operator distinguish installed, registered, reachable, authenticated, authorized, bound, capability-approved, healthy, complete, and application-successful states?

Has live acceptance exercised the real MCP Gateway, identity, authorization, server, source, audit, persistence, and operator path?

Is this AI task truly bounded inference, or can the model alter the execution path, select tools, execute code, or create side effects?

If it is agentic, where exactly does the application control plane end and the OpenShell sandbox begin?

Can we identify the durable AgentRun, every AgentAttempt, and the immutable execution manifest for the result?

Can sandbox loss occur without losing workflow identity, checkpoint state, result evidence, or recovery capability?

Can the model, prompt, retrieved content, connector response, or sub-agent widen the execution profile, sandbox policy, trust domain, or capability grant?

Can the sandbox directly reach a canonical database, the Kubernetes API, an MCP server, an arbitrary internet host, or another application domain?

Are OpenShell network permission, MCP tool authorization, and domain-service business authorization enforced as separate gates?

Does one sandbox contain only one application trust domain and one bounded capability envelope?

Does every sub-agent have a separate child attempt, delegated outcome, narrower or equal context, narrower or equal capabilities, and independent cleanup?

Can provider or connector credentials enter prompt context, checkpoints, result envelopes, tool traces, logs, or the sandbox workspace?

Does a process exit merely mean the attempt ended, or are result validation, side-effect confirmation, canonical promotion, and operator acceptance tracked separately?

Can a timed-out, canceled, lost, or stale attempt still call a mutating tool or replace a newer result?

Can the operator see the active execution profile, sandbox-policy revision, model route, capability grant, run and attempt state, denials, checkpoints, result, and cleanup state?

Has live acceptance traversed the actual application → OpenShell → inference/MCP → application validation → operator path and proven direct bypass denial?
```

If the answers are not clear, the architecture is not ready.

---

# 17. Closing Principle

The h00pz Architecture Specification Framework is not intended to produce beautiful architecture documents.

It is intended to produce systems that remain:

- understandable;
- trustworthy;
- operable;
- evolvable;
- honest;
- simple enough to finish.

The final governing principle is:

> A correct implementation is not a correct product unless it answers the correct operator question, lives inside a coherent owning subsystem, preserves the correct canonical truth, crosses subsystem boundaries through governed contracts, survives failure and revision, presents that truth clearly to the operator, and leaves enough canonical repository truth that the next agent can work correctly without inheriting the prior conversation.
