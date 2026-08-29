---
title: "Subagents Are Cheap. Coordination Is Expensive."
slug: subagents-cheap-coordination-expensive
date: 2026-07-10
draft: false
description: "Launching several agents is trivial, but each adds assumptions and sync cost. The bottleneck was never parallelism; it's ownership, sequencing, and state."
tags:
  - ai
  - architecture
  - agents
  - systems
  - seams
categories:
  - AI Scar Tissue
image: subagents-cheap-coordination-expensive.png
---

There's a specific kind of high you get the first time you fan a problem out across a handful of coding agents. One agent takes this package, another takes that one, a third goes off to write the tests, and for about ninety seconds it feels like you've discovered a cheat code for software. You are, in some literal sense, doing more work per minute than you could alone, and it is genuinely thrilling right up until they come back and you have to make the results fit together.

That second part is where the money actually is, and it took me an embarrassing number of collisions to understand it. Spawning a subagent is nearly free. It's a function call now. The expensive part, the part that doesn't get cheaper no matter how good the agents are, is coordinating what they produce, and I kept spending nothing on the cheap part while ignoring the bill for the expensive one.

This post is about that asymmetry, because it changes how you should design a system full of agents. The number of workers was never the constraint. The number of unresolved relationships between them is.

## Cheap Is Not the Same as Free

Let me be precise about what got cheap, because it's real. Launching another agent used to mean a person, a plan, and a week. Now it's an API call that returns in the time it takes to describe the task, and that collapse in cost is not nothing. It genuinely lets you attack a problem from several directions at once, and for the right kind of problem that's a real advantage.

The trap is reading "cheap to spawn" as "cheap to use," and those are wildly different numbers. A spawned agent that does bounded, well-defined work and hands back a clean artifact is close to free. A spawned agent turned loose on an underspecified task, sharing state with three others, is one of the most expensive things you can add to a system, because its cost isn't in the spawning. It's in every assumption it makes that another agent has to reconcile, every piece of state it touches that another agent also touches, and every bit of ordering nobody decided on purpose.

## What the Collisions Taught Me

I learned the true cost the way I learn everything, which is by watching it go wrong in my own coding agents. When I run several against a codebase at once, the failures they produce are a near-perfect catalog of coordination cost.

One baseline test run came back with forty-six failed suites, and not one of the failures was in the code. They came from a working tree a previous agent had left behind, whose files another agent's test command swept up and ran with the wrong configuration. Two workers had been operating in a space they both reached into, and the leftovers of one silently broke the other. Another time, the same implementer agent got launched twice, a minute apart, after a context reset, and the two instances raced each other in separate working trees, each half-aware the other existed and neither owning the outcome. Both agents were individually fine. What was expensive was that nobody had said, in advance, who owned what. Both agents individually fine and the pair of them wrong is the [locally correct, globally wrong](/p/why-we-threw-away-portfolioos-v2/) shape I keep running into, and here the piece left unspecified was ownership.

Every one of those was a coordination failure wearing the costume of a code bug, and none of them would have been fixed by better agents. They'd have been fixed, and eventually were, by deciding the coordination up front.

## The Four Things You're Actually Paying For

When I look at what coordination actually costs, it comes down to four things that have to be explicit, and every one of them is work you do whether you admit it or not. The first is ownership: which agent owns which piece of state or output, such that no two of them think they own the same thing. The second is artifacts: what each agent produces, in what defined shape, so the next one consumes a real object instead of reverse-engineering a side effect. The third is sequencing: what has to finish before what starts, because "run them in parallel" is a decision about dependencies whether or not you made it deliberately. The fourth is authoritative state: where the real version lives, so an agent reads truth rather than whatever another agent happened to leave lying around.

Those four are the entire bill. When they're explicit, adding an agent is genuinely cheap, because the new one slots into a defined position with a defined contract and can't collide with anything. When they're implicit, every agent you add multiplies the cost, because it becomes one more place for ownership to be contested, artifacts to be guessed at, sequencing to be assumed, and state to fork. The agents were cheap. The undefined relationships between them were the expense, and you pay for those relationships at runtime, as drift and collisions, if you refuse to pay for them at design time as decisions.

## The Cheapest Coordination Is a Written Packet

What actually made the agents composable wasn't smarter agents or better isolation, though isolation helped. It was giving each subagent a written packet and refusing to let it widen its own scope. The packet says what the agent is responsible for, what it receives, and what it must produce, and that's the whole contract. The agent's job is to satisfy the packet, not to decide what the job should have been, and that single constraint is what turns a pile of workers into a system.

The roles above the subagent are just as bounded. I supply the mission and the boundary calls, the main session works out the consequences and drafts and argues, and the subagent executes a defined packet. Each level has an explicit thing it does and an explicit thing it doesn't, and the coordination cost lives in getting those boundaries right, once, up front, rather than in untangling them afterward across every worker that guessed wrong.

## Optimize the Expensive Thing

The reason this matters practically is that it tells you where to spend your attention, and it's the opposite of where the excitement is. The exciting thing is fanning out more agents, and that's the cheap thing, the thing that's already solved. The boring thing is deciding ownership, defining the artifacts, ordering the work, and naming the authoritative state, and that's the expensive thing, the actual bottleneck, the part that determines whether ten agents give you ten times the output or ten times the mess.

So when I design a system full of agents now, I don't ask how to launch more of them, because that question answers itself for free. I ask what each one owns, what it produces, what has to come before it, and where the truth lives, because those are the questions that cost something, and the cost is going to be paid regardless. The only choice is whether I pay it deliberately, in a design, or accidentally, in a forty-six-suite failure that had nothing to do with the code and everything to do with two agents reaching into the same drawer.
