---
title: "How I Accidentally Built a Multi-Agent System Wrong"
slug: accidentally-multi-agent-wrong
date: 2026-06-11
draft: false
description: "Adding more agents feels like decomposition, but splitting responsibilities without defining contracts only distributes ambiguity across more components."
tags:
  - ai
  - architecture
  - agents
  - systems
  - seams
categories:
  - AI Scar Tissue
image: cover.png
---

Adding a second agent feels like progress. The first one was doing too much, so you split its job, hand half of it to a new agent, and stand back to admire a system that now looks properly decomposed. There are two boxes where there was one, each with a smaller responsibility, and the diagram is cleaner. It feels like the moment an architecture matures from a script into a system.

I've done this more than once, and it took me a while to see that most of the time I wasn't decomposing anything. I was taking an ambiguous job and spreading the ambiguity across more components, which is a different operation entirely and a much worse one. A single confused agent is at least confused in one place. Several agents sharing an undefined boundary are confused in the spaces between them, where nobody is looking.

This post is about the difference between splitting a system and merely multiplying it. It's also about how I learned, mostly from my own coding agents, which one I was actually doing.

## Decomposition and Distribution Are Not the Same Thing

Real decomposition reduces the total ambiguity in a system. You take a job, find a genuine seam inside it, and cut there, so that each side of the cut has a clear responsibility and a defined thing that crosses between them. After the cut, each piece is easier to reason about than the whole was, because the boundary carries a real contract and each side can ignore the other's internals.

Distribution does the opposite while looking identical on the diagram. You take a job whose boundaries were never defined, split it anyway, and hand the pieces to separate agents. Nothing about the ambiguity has been resolved, because you never did the work of deciding what each piece owns or what crosses between them. All you have changed is the number of places the confusion can live, and you have increased it. The job is exactly as underspecified as before, except now the underspecification is spread across a coordination boundary, where it is harder to see and much harder to debug.

The tell is that the split produced no new contract. If cutting a job in two didn't force you to write down what one side may assume about the other, you didn't decompose it. You just made two copies of the same unanswered question.

## The Symptoms Showed Up as Collisions

I learned this most vividly not in the financial system but in the agents I use to build it. When I run several coding agents against a codebase at once, the failures they produce are a near-perfect illustration of distributed ambiguity, because they're concrete and they're mine.

One baseline test run failed forty-six suites, and none of the failures were in the code. They came from a working tree that a previous agent had left behind, whose files were being picked up by another agent's test command, which used the wrong configuration for them. Two agents had been operating in a space they both reached into, and the residue of one silently broke the other. On another occasion the same implementer agent was launched twice, a minute apart, after a context reset, and the two instances raced each other in two separate working trees, each half-aware that the other existed and neither owning the outcome.

Nothing in either case was a code bug. Both were coordination failures, the exact thing that appears when you have multiple workers and no explicit account of who owns what, when, and where. The agents weren't wrong individually. The system that arranged them had never said what each one was responsible for, so they collided in the gaps. It's the [locally correct, globally wrong](/p/why-we-threw-away-portfolioos-v2/) shape again, made of processes this time instead of data: every agent behaving correctly, the whole confused, and the error living in the space nobody was told to own.

## What Was Actually Missing

Every one of those collisions came down to the same four things being left implicit, and I now think of them as the minimum any multi-agent arrangement has to make explicit before it deserves the name. The first is ownership: which agent owns which piece of state or output, such that no two of them believe they own the same thing. The second is state: where the authoritative version lives, so that an agent reads truth rather than whatever another agent happened to leave lying around. The third is sequencing: what must finish before something else begins, because "run them in parallel" is a decision about dependencies whether or not you made it on purpose. The fourth is outputs: what each agent is expected to produce, in what shape, so that the next agent consumes an artifact rather than reverse-engineering a side effect.

When those four are explicit, adding an agent really is decomposition, because the new agent slots into a defined position with a defined contract. When they're implicit, adding an agent is just distribution, and each new worker becomes another place for ownership to be contested, state to fork, sequencing to be assumed, and outputs to be guessed at. The number of agents was never the point. The number of undefined boundaries was.

## A Second Agent Can't Fix an Undefined Boundary

The seductive thing about adding agents is the belief that intelligence will cover for the missing structure, that if each agent is capable enough it will figure out the coordination on its own. This is the same mistake as expecting a large context window or a clever prompt to compensate for absent architecture, and it fails the same way. A second agent handed an unclear job doesn't clarify the job. It simply has an unclear job too, and now the two of them have to agree, implicitly, about a boundary that was never drawn.

This is where multi-agent systems quietly turn into the thing [an earlier post in this series](/p/artifacts-not-conversations/) warned about: a collaboration that runs on natural-language handoffs and shared mutable space, where assumptions drift because nothing pins them down. The agents pass work between themselves, each interprets the previous one a little differently, and the system as a whole ends up confidently acting on something none of them actually established. More capable agents don't slow that drift. They make it more articulate.

## Isolation Helps, but It Is Not Coordination

The fix for my colliding coding agents was, in the immediate sense, isolation. Give each agent its own working tree so that one can't trample the other's files, and the trampling stops. That's real and worth doing, and it removed the specific class of failure where leftover residue from one agent broke another.

But isolation only prevents interference. It doesn't produce coordination, and the two are easy to confuse. Two agents in separate worktrees can no longer corrupt each other's files, and they can still both believe they own the same output, still assume an ordering that doesn't hold, still produce results that the integrating step can't reconcile. Isolation removes the accidental collisions. It does nothing about the missing contracts, because a contract is a positive statement about who owns what, and a wall between two agents isn't that statement. Getting isolation and calling the coordination problem solved is how you end up with agents that no longer break each other and still can't be composed into a correct result.

## The Bounded Subagent

What actually worked was giving the subagents contracts, and the shape of that contract is worth stating because it is small. In the working pattern I settled on, a subagent executes against a written packet and doesn't get to widen its own scope. The packet is the contract. It says what the subagent is responsible for, what it receives, and what it must produce, and the subagent's job is to fulfill it, not to decide what the job should have been.

That one constraint, the refusal to let a worker expand its own boundary, is what turns a pile of agents into a system. The roles above the subagent are just as bounded: I supply the mission and the boundary calls, the session works out consequences and drafts and argues, and the subagent executes a defined packet. Each level has an explicit responsibility and an explicit thing it doesn't do. When I skipped that and simply launched agents at a problem, I got collisions. When the packet defined the boundary first, the same agents composed cleanly, because the ambiguity had been resolved before they ran rather than distributed among them to sort out at runtime.

## What Multi-Agent Systems Actually Require

None of this is an argument against multiple agents. It's an argument that the agents are the cheap part, and the coordination is the expensive part, which is a theme this series keeps returning to from different directions. Launching another worker costs almost nothing now. Deciding what it owns, where its authoritative state lives, what must precede it, and what artifact it produces is the actual work, and it is work you do whether or not you admit it, because leaving it undone doesn't remove it. It just moves it to runtime, where it shows up as drift and collisions instead of as a design decision.

So when I look at a multi-agent design now, I don't count the agents and feel reassured by the decomposition. I look for the four things that make decomposition real, which are ownership, state, sequencing, and outputs, and if I can't find them stated explicitly, I know what I'm actually looking at. It isn't a decomposed system. It's a single ambiguous job wearing several costumes, and the extra agents aren't helping. They are just giving the confusion more places to hide.
