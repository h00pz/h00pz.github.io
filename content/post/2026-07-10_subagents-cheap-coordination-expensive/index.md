---
title: "Subagents Are Cheap. Coordination Is Expensive."
slug: subagents-cheap-coordination-expensive
date: 2026-07-10
draft: false
description: "Launching several agents is trivial, but each adds assumptions and sync cost. The bottleneck was never parallelism; it's ownership, sequencing, and state."
tags:
  - subagents
  - multi-agent
  - agents
  - workers
  - model-routing
categories:
  - AI Coding Scar Tissue
image: subagents-cheap-coordination-expensive.png
---

There's a specific kind of high you get the first time you fan a problem out across a handful of coding agents. One agent takes this package, another takes that one, a third goes off to write the tests, and for about ninety seconds it feels like you've discovered a cheat code for software. You are, in some literal sense, doing more work per minute than you could alone, and it is genuinely thrilling right up until they come back and you have to make the results fit together.

That second part is where the money actually is, and it took me an embarrassing number of collisions to understand it. Spawning a subagent is nearly free. It's a function call now. The expensive part, the part that doesn't get cheaper no matter how good the agents are, is coordinating what they produce, and I kept spending nothing on the cheap part while ignoring the bill for the expensive one.

This post is about that asymmetry, because it changes how you should design a system full of agents. The number of workers was never the constraint. The number of unresolved relationships between them is.

## Cheap Is Not the Same as Free

Let me be precise about what got cheap, because it's real. Launching another agent used to mean a person, a plan, and a week. Now it's an API call that returns in the time it takes to describe the task, and that collapse in cost is not nothing. It genuinely lets you attack a problem from several directions at once, and for the right kind of problem that's a real advantage.

The trap is reading "cheap to spawn" as "cheap to use," and those are wildly different numbers. A spawned agent that does bounded, well-defined work and hands back a clean artifact is close to free. A spawned agent turned loose on an underspecified task, sharing state with three others, is one of the most expensive things you can add to a system, because its cost isn't in the spawning. It's in every assumption it makes that another agent has to reconcile, every piece of state it touches that another agent also touches, and every bit of ordering nobody decided on purpose.

## What the Collisions Taught Me

I learned the true cost the way I learn everything, which is by watching it go wrong in my own coding agents. I've told those collisions in detail [in an earlier post](/p/accidentally-multi-agent-wrong/): a baseline run that failed forty-six suites with nothing wrong in the code, because two agents reached into the same working tree, and the same implementer launched twice after a context reset, racing itself in two trees with neither instance owning the outcome. Both agents individually fine and the pair of them wrong is the [locally correct, globally wrong](/p/why-we-threw-away-portfolioos-v2/) shape I keep running into.

That earlier post was asking what was missing. This one is asking what it cost, because the answer reframes how you budget a system full of agents. Every one of those collisions was a coordination failure wearing the costume of a code bug, and none of them would have been fixed by better agents. They'd have been fixed, and eventually were, by paying for the coordination up front.

## The Four Things You're Actually Paying For

The [earlier post](/p/accidentally-multi-agent-wrong/) named the four things a multi-agent split has to make explicit before it deserves the name: ownership, artifacts, sequencing, and authoritative state. I won't re-argue them here. What matters for this post is that the same four are the line items on the bill. Ownership is paid when two agents believe they own the same output and someone has to untangle it. Artifacts are paid when the next agent reverse-engineers a side effect instead of consuming a defined object. Sequencing is paid when "run them in parallel" turns out to have been a dependency decision nobody made on purpose. Authoritative state is paid when an agent reads whatever another one left lying around instead of the truth.

Those four are the entire bill. When they're explicit, adding an agent is genuinely cheap, because the new one slots into a defined position with a defined contract and can't collide with anything. When they're implicit, every agent you add multiplies the cost, because it becomes one more place for ownership to be contested, artifacts to be guessed at, sequencing to be assumed, and state to fork. The agents were cheap. The undefined relationships between them were the expense, and you pay for those relationships at runtime, as drift and collisions, if you refuse to pay for them at design time as decisions.

Anthropic reported the same asymmetry from the other end of the scale. Building <a href="https://www.anthropic.com/engineering/multi-agent-research-system" target="_blank" rel="noopener">their multi-agent research system</a>, they found the subagents were the easy part and the coordination, the context handoff, and the token overhead were where the real engineering went, and they're blunt that whole classes of work, most coding among them, aren't worth splitting up at all. Cheap to spawn, expensive to coordinate, holds whether the agents are writing my code or researching a question.

## The Cheapest Coordination Is a Written Packet

The mechanism that made my agents composable is the same one that [earlier post](/p/accidentally-multi-agent-wrong/) landed on, the written packet that tells a subagent what it owns, what it receives, and what it must produce, with no license to widen its own scope. I won't re-explain it here beyond the part that matters for cost: a packet is you paying the coordination bill once, at design time, as a decision, instead of many times at runtime, as drift. The boundaries above the subagent are paid the same way, and getting them right once up front is cheaper than untangling them afterward across every worker that guessed wrong.

## Optimize the Expensive Thing

The reason this matters practically is that it tells you where to spend your attention, and it's the opposite of where the excitement is. The exciting thing is fanning out more agents, and that's the cheap thing, the thing that's already solved. The boring thing is deciding ownership, defining the artifacts, ordering the work, and naming the authoritative state, and that's the expensive thing, the actual bottleneck, the part that determines whether ten agents give you ten times the output or ten times the mess.

This even decides which model I point where. I run all of this through HADH, the h00pz Agentic Development Harness, and it routes work through an internal model router, with the split drawn on purpose. The coordinating main session runs on Opus, the expensive model, because coordination is the expensive judgment and the place a mistake costs the most. The bounded coding subagents run on GLM, which is cheaper and faster, because their work is exactly the kind of well-defined execution a smaller model handles fine once the packet has drawn its boundaries. It's the same asymmetry one layer down: spend the costly resource on the costly problem, which is the coordination, and let the cheap resource do the cheap, bounded thing, which is the code inside a packet that already decided what the code has to be. HADH gets a post of its own later, because the harness is where a lot of this stops being advice and starts being enforced.

So when I design a system full of agents now, I don't ask how to launch more of them, because that question answers itself for free. I ask what each one owns, what it produces, what has to come before it, and where the truth lives, because those are the questions that cost something, and the cost is going to be paid regardless. The only choice is whether I pay it deliberately, in a design, or accidentally, in a forty-six-suite failure that had nothing to do with the code and everything to do with two agents reaching into the same drawer.
