---
title: "Everything Is a Write Path"
slug: everything-is-a-write-path
date: 2026-09-09
draft: false
description: "I spent two days trying to justify burning Ansible to the ground and ended up designing something that makes it useful instead."
tags:
  - infrastructure
  - agents
  - ansible
  - aiops
categories:
  - Automation
image: everything-is-a-write-path.png
---

I started this week wanting to throw everything out.

I have a NetBox instance at home that I resent. I have Ansible playbooks I wrote and don't want to look at. I'd just finished building a certificate management system in Ansible on top of cert-manager, behind a firewall, with DNS01 challenges against a provider whose API I had to write myself. If you want a compact description of misery, that's it: an imperative push tool babysitting an asynchronous control loop it can't see into, polling `status.conditions` through Jinja, retrying until it either converged or I stopped caring.

So I went looking for the argument that agents would save me. What I found instead was that I'd misdiagnosed the problem for about six years.

## Ansible isn't rigid. It's impoverished.

I'd been saying "rigid" this whole time. Rigid would mean the tool constrains me to a sound model of the world. It doesn't. YAML lets me express any sequence of operations I want, in any order, with any amount of nonsense. That's not rigidity. That's a vocabulary with no words for the things that matter.

Here's what Ansible cannot say:

- What a resource is, as opposed to what to do to it
- Whether an operation is reversible
- What it costs to read something
- What happens on partial failure
- That it doesn't know

HCL has real types and still can't express the last one. Neither can NetBox. Neither can a Python script with an SSH key, which was my next instinct and which is a local optimum at best: you get speed and better authoring, and you still have no memory of the world between runs.

Every serious user of these tools ends up encoding the missing semantics in convention, comments, and tribal knowledge. That's the tell. When the entire community has agreed on unwritten rules the language can't express, the language is missing something.

## Three sources of truth, zero read paths

Look at what my customers actually run. Terraform for state. Ansible for config execution. ServiceNow for CMDB. Glue between them. Then, recently, a model and some MCP servers bolted across the top, and they call the result AIOps.

Those three systems disagree by construction, and the disagreement isn't sloppiness:

- Terraform knows what it created and nothing about what happened afterward.
- Ansible knows nothing at all between runs. It reports `changed: true` and forgets.
- ServiceNow knows what somebody typed, possibly during onboarding, possibly in 2019.

Not one of them observes anything. They are three write paths, each mistaking its own writes for reality, and the glue exists to copy assertions between them and hope.

Bolting a model onto that stack doesn't make it smarter. It makes it worse in a specific way. The model's job becomes reconciling three confidently-stated, mutually inconsistent versions of the world, and models are outstanding at producing a plausible synthesis. So you get a coherent narrative assembled from three wrong inputs, delivered fluently, with no signal that anything was in conflict.

The pre-AI version of this stack at least failed visibly when the glue broke. The AI version fails smoothly.

Here's the part it took me six years to say plainly: the read path is the hard half, and it always was. A write path is an assertion: do this thing. A read path has to answer "what is the current state of this?" for a system that was never built to be asked, that can only tell you what it was told rather than what it is, and that sometimes lies. There's no oracle. Every honest answer is assembled from partial, stale, occasionally fabricated reports. Writing is easy because you're asserting. Reading is hard because you're discovering, and discovery over infrastructure is genuinely underdetermined. That one asymmetry is under every complaint in this post.

## The vendors know. Their docs say so.

I went and read what everyone shipped this year, expecting to be annoyed by marketing. I was, but not the way I expected.

Ansible Automation Platform 2.7 added an MCP server in tech preview, Automation Orchestrator with AI agents and human oversight in a visual designer, and Lightspeed with bring-your-own-knowledge. Every one of those additions sits at the authoring or orchestration layer. Nothing touches state. The execution layer still knows nothing about the world between runs. Red Hat's bet is that Ansible becomes the actuator agents call, which is coherent, and which leaves the actuator unable to tell an agent whether the last action actually worked.

HashiCorp's Infragraph is sold as the trustworthy substrate for agentic operations. Then you read the documented limitations: syncs are triggered or scheduled rather than real-time, no drift detection, a subset of AWS resources, no custom nodes or edges. Fixed schema, periodic sync, partial coverage. That's a CMDB with a graph query language, and you can't extend it, which is the exact NetBox complaint I opened with.

Not because they're incompetent. Because the read path is genuinely the hard part, and the roadmap admits it out loud.

Everyone is shipping the reasoning layer. Nobody is shipping the observation layer. And I don't think that's stupidity. I think it's that reasoning generalizes across every customer and demos beautifully, while a trustworthy read path is per-system, unglamorous, never finished, and impossible to screenshot. There's no business model in it. So it doesn't get built, and the void gets filled by three products that answer a question nobody asked.

## Two workers

What came out of two days of arguing is smaller than what I set out to build, and I think that's the point.

**Worker one: the agentic explorer.** You point it at a class of thing. It pokes around: ports to PIDs to binaries to packages to config files to data directories to outbound connections. It figures out how to read that kind of system.

Its output is not a report about the host. Its output is a recipe: run these eight commands on machines like this one, and that tells you what you need to know. A human reads the recipe once, agrees it's sensible, and it goes into git.

Then the explorer is done. For that class of thing, it may never run again.

**Worker two: the deterministic collector.** It takes the promoted recipe, runs those exact commands, and turns raw output into structured records. A model sits in the middle only if the output is messy enough to need one, and for most things, a parser is fine. Every field points back at the command that produced it. Anything it couldn't determine is written down as unknown, with a reason: couldn't reach it, couldn't authenticate, command didn't exist, output made no sense.

That word, unknown, isn't one thing, and collapsing it is how a read layer lies about its own coverage. "Didn't answer" is transient, and you retry it. "Answered, but I couldn't authenticate" is a permission fact, and in a real estate that is most of your unknowns, not the exotic hardware. "Unreadable by construction, because the state lives in a BIOS nobody exposes" is permanent, and it should propagate up as a design constraint rather than a retry. A layer that can't tell unreachable from unauthorized from unreadable will misreport the shape of its own gap, and that gap is the number the whole thing exists to make honest.

That's a [deterministic sandwich](/p/the-deterministic-sandwich/), and it's the same pattern I've been using elsewhere for a year.

The critical rule: the explorer hands over raw captured output, not its own understanding. If it passes a summary of what it concluded, then worker two is just structuring a model's narrative and no amount of schema validation saves you. Pass the stdout and the command that produced it, and every field in the final record is checkable against evidence.

That rule kills one kind of variation. There's a second the schema alone doesn't touch. Variation in reporting is the same observed reality serialized differently run to run, `eth0` one night and "the primary interface" the next, and a typed schema plus a parser that drops anything malformed ends it outright. Variation in observation is worse: the model ran different commands this time, so it saw different things. One run reads `systemctl list-units`, the next reads `/etc/systemd/system`, and now you have two genuinely different pictures of the same unchanged host. A confidently complete record built from half the evidence passes every check you have. That is the whole reason the probe set is frozen config and not a model decision: the model never chooses what to look at, it only interprets what code already collected.

The frequency of the explorer is the health metric for the whole system. If it's running on every host every night, the design has failed and you're paying inference to rediscover things you already know.

And the frequency is more than a cost meter. If explorer runs drop toward zero and then spike, something in the estate grew a shape the probes don't fit, which is drift detection at the schema level, the thing none of the three systems can give you. The promotion in between is a gate, not a side effect. A candidate recipe is a proposal a human accepts before it goes into git, because otherwise the model quietly redefines what "interface" means on a Tuesday and every downstream consumer inherits the new meaning with no diff to show for it.

## Everything else is a claim

Once you have observations with provenance, the three-systems problem stops being a synthesis problem and becomes a differ.

There's a fork here worth naming, because the middle-ground framing pulls hard toward the wrong branch. Integrating these systems means making them agree: map the schemas, resolve the conflicts, keep them in sync. That's the glue I was trying to escape, relocated into my own code, dragging every one of their edge cases with it. Grounding them means being the layer that knows what's true and letting each system stay wrong in its own way. The test that separates the two: does the feature require me to know what ServiceNow's schema means? If yes, I'm integrating, and I've signed up for their nuance forever. An observation needs no such mapping. A differ needs only enough to know that two records describe the same thing.

ServiceNow says 32GB. Terraform says it built 16GB. The host reports 16GB. Nothing gets overwritten. Nothing gets auto-corrected. You publish the delta and let humans decide.

That extends further than I first thought. Bash history, package manager logs, systemd journal, cloud-init artifacts, and change management records are all evidence, of different grades. A yum transaction has an outcome. A `.bash_history` line has an intention and no exit code. A change record has intent, which nothing else has, and also a coverage lie in a specific direction: emergency and break-fix work bypasses the process entirely, so the change history looks tidiest exactly where the system is messiest.

The rule that holds all of it together: corroboration or hypothesis. History suggests someone installed a tarball; the filesystem confirms it or it stays a guess. Nothing enters the record as fact without an observation behind it.

Two useful things fall out of the differ that nobody currently produces: approved changes that never landed, and observed state with no change record at all. The second one is unapproved drift, and an auditor cares about that number a great deal.

There's a number under all of this that sells it, and you can produce it in a week against an estate you already run: what percentage of your CMDB fields are wrong. Nobody knows it. Everybody suspects it's bad. No vendor has any incentive to measure it, because the answer indicts the thing they sold you. The differ produces it as a byproduct, and it converts "nice to have" into a fact somebody has to answer for.

## Why this actually matters: backups

Here's the payoff that has a dollar figure attached.

Most people back up the entire virtual machine. 400GB of OS and packages to protect 12GB of data that matters, times the estate, times retention. The usual explanation is laziness: nobody wants to write the app profile.

I don't think that's the real reason. Even people who would write the profile face a worse problem: it's a claim about a system that's been drifting for four years, with no way to check whether it's still accurate short of an actual restore. So the profile gets written once during onboarding, rots immediately, and the VM image becomes the thing everyone trusts at 3am.

A derived profile can't rot. That's the whole argument, applied to DR instead of CMDB.

And DR is the one place in infrastructure planning with a real oracle: you can test a restore. Build it in a sandbox, boot it, run the app's health checks, diff against the original observations. Which means you can let a model generate the recovery automation (including generated Ansible nobody reads or maintains), because you're reviewing a test result, not a playbook.

The output I'd want most isn't the plan. It's the gap list. This file exists and nothing accounts for it. This service starts before that one and I can't tell you why. This mount points at storage I can't reach. A generated plan that boots is good. A generated plan plus twelve things nobody can account for is what a DR review has always been pretending to be.

## The part where I stop wanting to burn it down

Here's the reversal, and I'm still slightly annoyed by it.

Both workers can run in an Ansible execution environment. AAP already syncs projects from git, so the promotion gate is free. It already has inventory, credentials, RBAC, scheduling, and a per-run audit log. The collector needs no logic in YAML at all; it just runs commands and returns output, which is the version of Ansible I don't hate. The explorer needs an egress credential to a hosted model, passed as an environment variable, on a separate template with a separate approval.

The distribution is a collection, an EE definition, and a sample probe repo. Customer adds a project and two job templates. Nothing to procure, nothing in the network path.

So: I started wanting to replace the execution layer, the state layer, and the CMDB. I ended with a recipe format, a record schema, an unknown taxonomy, and two workers, running inside infrastructure people already have.

The reason those tools suck hasn't changed. They're write paths with no read path. Every complaint I opened with was a symptom of that one absence. But once you name the absence, replacing them stops being necessary, because the missing thing was never inside any of them.

## What I haven't solved

Two things, and I'd rather say them than pretend the design is finished.

**Type identity.** What makes two things the same type? A bonded NIC in hardware is genuinely different from a VM's virtio interface and a container's veth: three types, three recipes, fine. But the failure mode is drifting toward three hundred types because every exploratory run found something marginally different. Maximally malleable and completely unqueryable is worse than NetBox's rigidity. Get too specific and you get mush; too general and you've rebuilt the problem with extra steps.

**Run-to-run determinism.** Two collector runs against the same unchanged host must produce identical records. Not similar. Identical. If they don't, either the recipe is nondeterministic or a model is doing interpretation it shouldn't be doing. That's the gate everything else rests on, and it's testable in an afternoon.

Both are answerable at home, on one host, with a NetBox instance already sitting there waiting to be proven wrong.

Which is a strange place to end up after two days of arguing about where the industry is going: a falsifiable version of the whole thesis, and it fits in a weekend.
