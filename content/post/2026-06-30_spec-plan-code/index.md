---
title: "Spec → Plan → Code: Slowing AI Down to Make It Faster"
slug: spec-plan-code
date: 2026-06-30
draft: false
description: "Coding agents write implementation before anyone agrees what to build. Forcing spec, then plan, then code makes decisions explicit and cuts costly rework."
tags:
  - ai
  - architecture
  - hasf
  - systems
  - agents
categories:
  - The Agentic SDLC
image: spec-plan-build.png
---

The single most impressive and most dangerous thing about a coding agent is how fast it will start writing code. You describe a vague notion of a feature, and before you've finished forming an opinion about what you actually want, there are files. Real, plausible, well-structured files, with tests, that do a thing. It feels like productivity, and sometimes it is, and sometimes it's the software equivalent of a contractor who starts pouring concrete while you're still deciding where the house goes.

I spent a while enjoying that speed before I noticed the bill. The code an agent produces in the first thirty seconds encodes a hundred small decisions that nobody agreed to, and every one of those decisions is now load-bearing, because the tests pass and it looks done. When it turns out the boundary was wrong, or the thing it built solves a problem I'd already solved elsewhere, I don't get to keep the speed. I pay it all back, with interest, unwinding a confident implementation of the wrong idea.

This post is about the discipline that got that time back, which sounds like it should be slower and is actually faster: force the work through specification, then planning, and only then code.

## The Agent's Superpower Is Also the Trap

It's worth being precise about what a coding agent is extraordinary at, because the fix isn't to use it less. It's genuinely brilliant at turning a well-specified, well-planned unit of work into correct code, quickly, including the parts I find tedious. That capability is real and I lean on it constantly.

The trap is that it's equally happy to turn a badly-specified, unplanned notion into code, at the same speed, with the same confidence. It doesn't pause at ambiguity the way a careful human sometimes does. It resolves the ambiguity, silently, by picking something reasonable and building it, and now the ambiguity has an implementation and a passing test and the appearance of a decision. The agent didn't do anything wrong. It answered the question I asked, which was "build me something like this," when the question I needed answered first was "what exactly is this, and where does it belong."

## Spec Is Where the Argument Happens

So the first stage is a specification, and its entire job is to be the place where the disagreements happen before there's any code to defend. A spec states what the thing is for, what it owns, where its boundaries are, what it must never do, and what "done" actually means, and it does all of that in prose that's cheap to change because changing it costs a paragraph rather than a refactor. This idea has been gathering a name lately, spec-driven development, and its crispest statement is probably Sean Grove's <a href="https://lawwu.github.io/transcripts/8rABwKRsec4.html" target="_blank" rel="noopener">"The New Code"</a>: the specification is the durable artifact and the code is closer to a build output, so keeping the code and throwing away the intent that produced it is backwards.

This is the same lesson as arguing before you write, moved up a level. Once code exists, everything after it bends to protect it, because throwing code away feels like waste even when it's the cheapest possible moment to throw it away. A spec has no such gravity. You can gut a spec, invert a boundary in it, or delete a whole section, and it costs nothing but the willingness to admit you were wrong on paper instead of in production. The specifications in pOS live in their own folder for exactly this reason, and a real one goes through several rounds of correction before a single line of implementation is planned. One spec I watched get scoped defined five separate ledger items with their boundaries drawn, and the arguing all happened there, in the cheap medium, where it belongs. One of those specs is reproduced in full here, the design for the first worker in pOS: <a href="https://github.com/h00pz/h00pz.github.io/blob/main/examples/pos-collection-worker-spec.md" target="_blank" rel="noopener">The Collection Worker</a>. It argues what the thing is, what it owns, and the one boundary it must never cross (it is position-blind, it never sees a holding), and it makes that whole case in prose, before there is any code to defend.

## Plan Is Where the Order Gets Decided

The second stage is a plan, which turns an agreed spec into an ordered sequence of implementable slices with their dependencies made explicit. This matters more than it sounds, because "build the spec" is not an instruction, it's a wish. A plan decides what gets built first, what has to exist before what, and where the natural seams in the work are, and it does that while there's still nothing to unwind if the order turns out to be wrong.

In practice this is a committed document with a real identity, not a mental note. A plan gets written, reviewed, and committed with its own hash before the build task that implements it is even created, and each slice knows what it depends on. When implementation reveals that the plan was wrong, and it sometimes does, the plan gets corrected and re-committed, and only then does the code follow. The order is a decision you make deliberately, in a medium where changing your mind is free, rather than a thing that emerges by accident from whatever the agent happened to write first. The <a href="https://github.com/h00pz/h00pz.github.io/blob/main/examples/pos-collection-worker-plan.md" target="_blank" rel="noopener">plan that implements that spec</a> shows the shape I mean: it opens by authoring the ledger item on its own pull request, then walks an ordered set of slices, each one a failing test, then an implementation, then a commit, and each naming what it depends on. The order is settled on the page before it is anywhere near the code.

## Code Is the Cheap Part, Once the Rest Is Done

By the time you reach code, the interesting decisions are already made, which is the whole point. The agent is now doing the thing it's genuinely best at: implementing a bounded, well-specified, well-ordered slice, against a definition of done it can be held to. There's a ledger tracking which slices are complete, and each one gets checked off as it lands and is proven, so the work has a shape and a memory rather than being a pile of files that appeared.

The result is that code stops being where the architecture gets decided by accident and goes back to being what it should be: the mechanical, verifiable execution of decisions that were made on purpose, earlier, more cheaply. The agent's speed is still there. It's just pointed at the part of the problem where speed is safe.

## When the Discipline Can't Be Skipped

Left to my own willpower, I skip steps, especially the mapping, and especially when I'm excited about an idea. So I built a harness to run this process for me, HADH, the h00pz Agentic Development Harness, and in it spec-plan-code isn't a habit I maintain, it's a thing the tooling enforces whether I feel like it or not. Each unit of work moves through its stages on separate branches, ideation, then build, then fix, with one transition per pull request, so I can't quietly fold "decide what this is" into "write it" and pretend they were the same step. And the gate that lets an item become buildable is mechanical: the harness refuses to promote it until its boundaries, dependencies, and impacts are actually mapped, and it fails the regeneration outright if they aren't. The check is done by a machine and the judgment stays with me, which is exactly the split I want.

That last part is the whole trick, and it's the same move as writing the spec down instead of holding it in my head. The behavior I keep getting wrong by hand, skipping the argument, skipping the ordering, letting the code decide, is precisely the behavior I stop trusting myself to get right and hand to HADH to carry. The discipline survives my worst days because it stopped depending on my best ones. HADH is a whole story of its own, the machinery that makes all of this enforceable rather than aspirational, and it gets its own post later in this series.

## The Math of Slowing Down

The reason this feels like a paradox and isn't is that the time you save by skipping the spec and the plan is real, and so is the time you lose paying for it later, and the second number is bigger. A wrong decision caught in a spec costs a paragraph. The same wrong decision caught in a plan costs a re-order. Caught in code, it costs a refactor and every downstream thing that was built on top of it. Caught in production, it costs an incident, a diagnosis, and the same refactor anyway, now with pressure. The cost of a mistake goes up by a rough order of magnitude at every stage it survives, which is <a href="https://en.wikipedia.org/wiki/Barry_Boehm" target="_blank" rel="noopener">Barry Boehm</a>'s defect-cost-escalation curve from decades of software research arriving again with a coding agent attached, and spec-plan-code is just a machine for catching mistakes as early and as cheaply as possible.

None of this makes the agent slower at the thing it's fast at. It makes me slower at the thing I'm reckless at, which is committing to an architecture by accident because the code appeared before the decision did. Spec, then plan, then code isn't a way of restraining a coding agent. It's a way of making sure that when I finally let it run, at full speed, it's building the right thing, in the right order, and the fast part of the process lands on the part of the problem that was actually ready for it.
