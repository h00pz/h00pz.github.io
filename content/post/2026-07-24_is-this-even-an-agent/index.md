---
title: "Is This Even an Agent?"
slug: is-this-even-an-agent
date: 2026-07-24
draft: false
description: "Three agent runtimes in, the question that mattered wasn't which framework to use. It was whether the thing I kept calling an agent was one at all."
tags:
  - agents
  - agentic
  - workflows
  - workers
  - harness
categories:
  - AI Systems Engineering
image: is-this-even-an-agent.png
---

I have run PortfolioOS on three different agent runtimes now. It started on LangGraph, moved toward OpenShell, and ended up on one I wrote myself, and for most of that journey I thought the thing I was shopping for was a framework. I was comparing orchestration models and checkpointer implementations and sandbox boundaries, sure that somewhere in that space was the right way to run an agent. What I actually needed was to stop and ask a much dumber question, which is the one this post is about: of all the things I was calling agents, how many of them were agents at all? The answer, when I finally counted, was almost none, and that number is what reorganized the whole design.

This is the first of the deeper, more technical posts, so I'm going to show you the actual code at each stop, because the whole argument lives in the difference between what the three runtimes made me write.

## LangGraph, and Guardrails That Ate the Work

PortfolioOS v2 chose LangGraph.js, embedded directly in the application. Every meaningful piece of AI work was a `StateGraph`: nodes wired together, a state annotation threaded through them, a Mongo checkpointer persisting the run. Here's the shape of it, trimmed but real, from the v2 research spine:

```typescript
export interface BuildGraphOpts {
  capabilityRouter: CapabilityRouter
  modelRouter: ModelRouter
  checkpointer: BaseCheckpointSaver
  promptResolver: PromptResolver
  // testMode seam: tests pass a STUB SeedSectionMap so the
  // arch-violation guardrail lets them through.
  testMode?: boolean
  testModeStubSeedSectionMap?: SeedSectionMap
  // optional raw-response diagnostic file persistence dir.
  rawResponseLogDir?: string
  // operator-approved runtime tunables threaded into every model-call node.
  tunables?: Slice1Tunables
}
```

Look at what's accumulating in there. Every one of those optional fields is a guardrail, a seam, or a piece of containment machinery, and every one of them lives inside the application graph. `testMode` exists so an architecture-violation guardrail will let a test through. `tunables` threads operator-approved limits down into each model call. The graph wasn't just orchestrating the work, it was policing it, and the policing was growing faster than the work.

That's the part that eventually broke, and it broke as a mission problem before it broke as an architecture problem. My own words at the time, which I'll quote because they're the whole reason for the rotation: *the research workers were so guardrailed that they never did 100% of what I wanted.* The cage I'd built in the app to keep the agents safe had gotten so tight that it was strangling the capability I built them for. The agents weren't failing. They were succeeding at a smaller and smaller version of the job, because every failure I'd ever seen had turned into another `if` in the graph.

Two things were wrong, and only one of them was LangGraph's fault. The first is that agent orchestration was built *in the app*, a framework woven through the business logic. The second, and the one that actually hurt, is that agent *containment* was built in the app too. That's the wrong layer. I already run infrastructure-level defense: command-gate hooks, a sandbox, worker restrictions, a read-only cluster, credential isolation. Rebuilding all of that a second time as `if` statements inside a graph doesn't add safety, it adds a flyswatting surface, and it steals the complexity budget that should have gone to the mission.

## OpenShell, and the Number That Changed Everything

The next stop borrowed from Atlas, my personal-AI project, which had already run this exact rotation. Atlas's decision record says it in one line: *the agent space is OpenShell, not LangGraph.* OpenShell is not a LangGraph replacement, it's a different plane entirely. LangGraph is an orchestration framework that lives in your app. OpenShell is an execution substrate that lives under it: a gateway, a per-sandbox supervisor, and the sandbox itself, enforcing process, filesystem, network, and credential policy from outside the application. Containment moves out of the graph and into the substrate the operator already trusts. That's the right instinct, and I still believe it.

But rotating PortfolioOS toward it forced me to actually classify the work, unit by unit, and the classification is what stopped me cold. Of fifty-four declared units of AI work in the system, fifty-one were *workers*: fixed control flow, a bounded number of model calls, no autonomous looping. Only three genuinely let the model decide what to do next. Atlas, the project that inspired the whole rotation, was running *zero* autonomous agent loops in production. Everything was bounded.

An execution sandbox is exactly what you need for a genuine agent, the kind that plans its own steps and picks its own tools and might wander. It is enormous overkill for a worker that calls a model once to classify a headline. I'd been about to move fifty-one bounded workers into agent sandboxes because I'd been calling all of them agents. The framework question, "LangGraph or OpenShell," had quietly assumed the thing I most needed to check.

## The Real Question

So the question was never which agent framework to run. It was, for each unit of work, *is this even an agent?* And that turns out to have a precise, checkable answer, because the thing that makes something an agent isn't whether it uses a model. It's whether the model chooses the next step.

That distinction became the first thing I built in the runtime I finally wrote for v3. It's a classification gate, and its entire job is to make every unit of work declare which it is, and then check the declaration instead of trusting it:

```typescript
export function deriveWorkClass(facts: ControlFlowFacts): WorkClass {
  // THE class-defining signal: does the model pick the next step?
  return facts.modelPicksNextStep ? 'agentic' : 'worker';
}

export function classifyDeclaration(decl: WorkDeclaration): ClassificationResult {
  const derived = deriveWorkClass(decl.facts);

  // (1) you can't relabel an agent as a worker to dodge the budget.
  if (decl.declaredClass !== derived) {
    return { ok: false, reason: `class mismatch: declared '${decl.declaredClass}', derived '${derived}'` };
  }
  // (2) an agentic declaration MUST carry a budget, or it's rejected outright.
  //     "an agent without a budget is an outage waiting for a bad prompt."
  if (derived === 'agentic' && decl.budget === undefined) {
    return { ok: false, reason: 'an agentic declaration must carry a budget; none present' };
  }
  return { ok: true, class: derived };
}
```

The test is control flow, not model use. A worker that calls a model once to classify a headline is still a worker, because its shape is fixed before it runs. An agent's shape is not fixed: nothing before the run knows how many steps it will take. And the gate's sharpest rule is the one about relabeling. The expensive mistake isn't calling a worker an agent, it's the reverse, declaring a thing a worker when the model actually drives it, because then it runs with no budget, no sandbox, and no record, which is v2's LangGraph problem restated exactly. So the gate refuses to let a declaration lie about itself, and it refuses to admit an agent that hasn't said, up front, how much it's allowed to cost.

## The 94%: Workers That Look Like Kubernetes

Here's the architectural choice I'm proudest of, and it's almost aggressively unoriginal: the fifty-one workers don't run on anything I invented. They run the Kubernetes operator pattern, applied to AI work.

If you've written a Kubernetes controller, the shape is muscle memory: a control loop that claims a piece of work, holds a lease on it, heartbeats to keep the lease alive, does the work, and reports the result or releases it back. PortfolioOS's worker loop is that, and its defining property is a deliberate absence:

```typescript
export class WorkerLoop {
  // STATELESS across units. It holds NO database connection, ever.
  // Everything for one unit arrives in the lease payload or through a read.
  async runOnce(): Promise<RunOnceResult> {
    const lease = await this.client.claim(this.cfg.filter);   // claim
    if (!lease) return { kind: 'empty' };                     // nothing to do; back off
    const stopHeartbeat = this.heartbeatWhileWorking(lease);  // "long work is fine; silent work is not"
    try {
      const outcome = await this.cfg.work(lease.payload);     // one bounded unit
      return this.report(outcome);                            // complete | release | failure
    } finally {
      stopHeartbeat();
    }
  }
}
```

The worker holds no database connection. It talks to one API over HTTP, and everything it needs arrives in the lease. That one constraint is what makes the contract the API and the schema private, and it means relocating a worker into its own pod, or later into an agent sandbox, is a base-URL change rather than a rewrite. In v2 every module held its own database connection, so every schema quietly became everyone else's contract, and you couldn't move a worker without moving everything it knew about storage. The stateless loop is the fix, and it's a fix Kubernetes operators have been shipping for a decade. I didn't need an AI-native runtime for the boring 94%. I needed a reconciliation loop and the discipline to notice that's all it was.

## The 6%: When It Really Is an Agent

For the handful of units that genuinely let the model drive, the machinery earns its weight, and only there. A real agent gets a budget the classification gate already forced it to declare, and an enforcer that halts the loop the instant it crosses any dimension of that budget:

```typescript
return (ctx: StepContext): HaltReason | null => {
  if (ctx.stepIndex >= budget.maxSteps) return 'steps';           // the wander stops here
  if (cumulativeTokens(ctx.prior) > budget.maxTokens) return 'tokens';
  if (elapsedMs() > budget.maxWallClockMs) return 'wall-clock';
  return null;                                                    // clear to take the step
};
```

And because an agent's control flow isn't fixed, it gets the thing a worker never needs: an audit trail. One run record per invocation, and an append-only attempt record per step, capturing what the model actually did.

```typescript
interface AgentAttempt {
  runId: string
  stepIndex: number                          // the order the run proceeded in
  tool: ToolName
  args: Readonly<Record<string, unknown>>
  disposition: 'granted' | 'denied'          // denied = not in the run's resolved allow-list
  result: ToolResult
  tokensUsed: number
}
```

Two details in there carry most of the weight. The record is append-only, so re-reading a run returns the exact same sequence forever, because an agent you can't replay is an agent you can't trust. And `disposition` exists because the tools a run may use are resolved from its capability grant at the start of the run, never from what the model asks for mid-flight. A step can request a tool it wasn't granted, and the record shows that request, denied. Discovered is not the same as approved.

## Where This Still Bites

I want to be honest about the seam I haven't closed, because the whole design rests on a classification and the classification is a judgment I make. The gate checks that a declaration is internally consistent, that an agent carries a budget, that a worker doesn't secretly loop. What it can't check is whether *I* drew the line in the right place. A unit I've declared a bounded worker because it calls the model in a fixed order is one prompt change away from being something that quietly decides its own next step, and nothing in the type system will catch me the day I let that happen. The most dangerous unit in the system isn't the honest agent with its budget and its audit trail. It's the worker I've stopped watching because I filed it under boring.

And the three real agents, the 6%, are where every hard problem I've written about on this blog still lives, undiminished. The runtime around them is solved. What the model does with its budget, and whether I can trust the judgment it reached inside it, is not. But that's the point of separating them out. By proving that fifty-one of fifty-four units never needed to be agents at all, I get to spend the entire agent-shaped worry budget on the three that do. The answer to "which agent framework should I use" turned out to be to stop needing one for almost everything, and to build the boring reconciliation loop that the almost-everything actually wanted.
