---
title: "The Teeth Are in the Hooks"
slug: the-teeth-are-in-the-hooks
date: 2026-07-20
draft: true
description: "Every post in this series is a rule I've broken while excited. So I built a harness to hold the rules for me, and the enforcement must live in code, not prose."
tags:
  - ai
  - architecture
  - agents
  - systems
  - hasf
categories:
  - The Agentic SDLC
image: the-teeth-are-in-the-hooks.png
---

I have to start with an admission, because the whole post falls apart without it. I don't trust myself to follow my own rules. Every post in this series is, underneath, a rule I worked out the hard way and then broke anyway the next time I was excited about something. I know that specifying before building saves time, and I've still let a coding agent start writing files while I was "just exploring." I know coordination is the expensive part, and I've still fanned out three agents into the same working tree because it felt fast. Writing the rule down turns out to be the easy part. Following it, on a Tuesday, when the demo is close and the idea is hot, is the part I keep failing.

So at some point I stopped trying to be more disciplined and did the thing I actually believe in, which is to take the behavior I keep getting wrong by hand and move it into something that carries it for me. That something is a harness, and it has an unglamorous name, HADH, the h00pz Agentic Development Harness. This is the post I've been promising for a while, and it's less exciting than it sounds and more useful than it looks, which is about right for the thing that turns a pile of good intentions into a process that actually runs.

## What a Harness Is, Next to a Framework

There are two different jobs here and it took me too long to separate them. [HASF](/p/introducing-hasf/), the framework, governs the architecture: what the system is, what it owns, where the seams are, what's true. HADH, the harness, governs the workers building it: how work is performed, what an agent is allowed to do, how a change gets from an idea to a merged pull request. One is about the truth of the system. The other is about the conduct of the things editing it. Conflating them is how you end up with a giant prompt that tries to be architecture, rulebook, and to-do list at once, which is exactly the kind of thing a model reads and quietly ignores half of.

The effective harness for any given project isn't one file, it's a composition: a base contract that every project shares, a project profile that adapts it, and the project's own canonical documentation. The base contract is a single file, an <a href="https://github.com/h00pz/h00pz.github.io/blob/main/examples/hadh-agents.md" target="_blank" rel="noopener">AGENTS.md</a>, and it's the thing that actually ties the harness together: it names the method, the roles, where truth lives, and what the main session is and isn't allowed to do, in one place a model reads first. The base carries the method. The profile carries what's different about this repo. The documentation carries the truth. Keeping those three separate is the same one-owner-per-concern instinct from the rest of the series, applied to the agent's own operating instructions instead of to the application's state.

## The Thing I Got Wrong First

My first version of the harness was a big, serious document telling the agent who it was and what it wasn't allowed to do. It held a great deal of stern language about authority, about which decisions the agent didn't own, about the ten things it must never touch. It read like a contract because I thought a contract was what enforced behavior.

It made the agents worse. Measurably, consistently worse. The more control language I put in front of a model, the more it seemed to spend its attention negotiating with the framing instead of doing the work, and the operator finding that came out of it is one I'd put on the wall: more control language means more pain with agents. The stern document wasn't holding the line. It was just noise the model had to wade through, and it was degrading the thing it was supposed to govern.

The fix reorganized my whole understanding of what a harness is. The teeth were never in the prose. The teeth are in the hooks. A command gate that runs as code on every tool call, denies by default, and only allows an action if it resolves to something the agent's role is actually permitted to do, holds the line whether or not a single sentence of authority prose exists. A mode gate that decides what phase the work is in enforces the sequence regardless of what the instructions say. Once the hooks do the enforcing, the prose is free to stop threatening and go back to just describing the method, which is the only thing prose was ever any good at.

That's why the harness ships in three weights of the same contract, and the enforcement is byte-identical across all of them. The <a href="https://github.com/h00pz/h00pz.github.io/blob/main/examples/hadh-agents.md" target="_blank" rel="noopener">full one</a> still carries all the authority language I started with, the <a href="https://github.com/h00pz/h00pz.github.io/blob/main/examples/hadh-agents-lite.md" target="_blank" rel="noopener">lite one</a> strips it to a flow a small model can hold in twenty-odd lines, and the <a href="https://github.com/h00pz/h00pz.github.io/blob/main/examples/hadh-agents-process.md" target="_blank" rel="noopener">process one</a> in the middle keeps the whole method and drops every sentence of control language, because the hooks already hold every boundary those sentences were pretending to. You can lay the three side by side and watch the same process get quieter while the machine underneath it never changes. The prose is a dial. The hooks are the machine.

## Where the Advice Becomes Enforced

With the enforcement in code, the rest of this series stops being advice and starts being something the harness simply won't let you skip.

[Spec, then plan, then code](/p/spec-plan-code/) isn't a habit I maintain anymore, it's a gate. Work moves through its stages on separate branches, ideation, then build, then fix, with one state transition per pull request, so I can't quietly fold deciding what a thing is into writing it. And the moment an item tries to become buildable, the harness runs a mechanical check and refuses to let it through unless its boundaries, its dependencies, and its impacts are actually mapped. The regeneration fails if they aren't. The judgment about whether the mapping is good stays mine. The refusal to proceed on an unmapped item is the machine's, and the machine doesn't get excited on a Tuesday.

The [coordination cost](/p/subagents-cheap-coordination-expensive/) is spent deliberately, too, right down to which model does what. The harness routes work through an internal model router, and the split is drawn on purpose: the coordinating main session runs on the expensive model because coordination is the expensive judgment, and the bounded coding subagents run on a cheaper, faster one because their work is well-defined execution inside a packet that already decided what the code has to be.

The subagents come in roles, and the roles are where the packet gets its teeth. An explorer and a verifier are read-only: they search, read, and check, and the gate simply won't let them change a file, because finding something and deciding to act on it are different jobs and only one of them is theirs. An implementer can build and run tests inside the repo, and still can't commit, push, deploy, or read a secret, because landing a change and merging it are also different jobs with different owners. These aren't a description of roles, they're real files: the <a href="https://github.com/h00pz/h00pz.github.io/blob/main/examples/hadh-explorer.md" target="_blank" rel="noopener">explorer</a>, <a href="https://github.com/h00pz/h00pz.github.io/blob/main/examples/hadh-implementer.md" target="_blank" rel="noopener">implementer</a>, and <a href="https://github.com/h00pz/h00pz.github.io/blob/main/examples/hadh-verifier.md" target="_blank" rel="noopener">verifier</a> definitions each pin a model, a list of tools the role can't touch, and the command-gate hook wired to the role's own name. Each role is a deny-by-default allowlist, computed in a hook, so a subagent that reaches past its role for a command it wasn't granted doesn't get talked out of it by a paragraph. The gate refuses the call and hands the need back up to the session that's actually allowed to make it. That's a [guardrail that's actually earned](/p/guardrails-you-havent-earned/), because it's enforced by something you can break on purpose and watch fail, not by a sentence asking the agent nicely.

The two tiers even remember differently, on purpose. The coordinating session's knowledge lives in claude-mem, the running record of what got decided and what broke across every past session, so the expensive judgment doesn't start from zero every morning. The workers' knowledge of the code lives in Graphify, a queryable graph of the repository that a subagent can ask for structure, paths, and explanations before it ever browses files by hand. You can see it written into the role files: an explorer is told to query Graphify before it reads broadly and to check claude-mem before re-solving something that already failed once. The main session accumulates the memory, the agents navigate the map, and neither one is allowed to treat either as canonical truth, because the truth still lives in the repository where the rest of this series keeps insisting it belongs.

## Is the Harness Just Scaffolding?

I have to hold this post to the same test I [held everything else to](/p/what-the-next-model-will-eat/), because a harness is the most scaffolding-shaped thing I've ever built, and if anything is going to be eaten by a better model, surely it's this.

Some of it, yes. The stern control-language document was scaffolding for a weaker model and for a weaker understanding of my own, and I deleted it, and the agents got better. If the next model needs less coaxing, less prompt structure, less hand-holding through a task, then the parts of the harness that provide those things should shrink, and I'll be glad to delete them the way I was glad to delete the last batch. Build as little of that as you can.

But the hooks aren't that. A command gate that stops a worker from pushing to production isn't compensating for a dumb model, it's encoding a boundary that has to exist no matter how smart the worker gets, because the smarter the worker, the more capable it is of confidently doing the wrong irreversible thing. The gate that blocks an unmapped item from being built isn't waiting for models to improve, it's enforcing that a decision got made before it got implemented, which is a property of the process, not of the reasoner. The enforcement is operability, not capability, and the bitter lesson has nothing to say about it. A better model makes the harness's prose thinner. It doesn't make the harness's hooks unnecessary, any more than a better driver makes the brakes optional.

## What It's Actually For

I want to be honest about how young and how personal this is. HADH is mine, its profiles are thin, and there are still behaviors I re-derive by hand because I haven't gotten around to teaching the harness to carry them yet. It's not a product, it's the accumulated set of things I got tired of getting wrong, wired into hooks so I'd stop getting them wrong the same way twice. Some of what's in it today will turn out to be scaffolding, and I'll delete it, and it'll sting a little, and that's fine.

What it's for is the gap between knowing the rule and following it, which is the gap this entire series lives in. I can write a post about specifying before building, and mean every word, and still not do it when I'm excited. The harness is what stands in that gap. It's the machine that follows my own rules on the days I won't, and the thing I learned building it is that the machine works exactly to the degree that its authority lives in code rather than in the story I tell the agent about who's in charge. The rules were the easy part. The teeth were always going to be the hard part, and the teeth are in the hooks.
