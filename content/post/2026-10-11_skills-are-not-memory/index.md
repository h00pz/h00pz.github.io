---
title: "Skills Are Not Memory"
slug: skills-are-not-memory
date: 2026-10-11
draft: false
description: "A coworker told me a different harness beat Claude Code, and he was half right. Hermes self-improves through skills better than anything I've used. It also forgets everything the moment a long build hits the context ceiling, and when I went looking, it had written itself a note about that."
tags:
  - harness
  - agents
  - memory
  - skills
  - persistent-state
  - spec-driven-development
categories:
  - AI Coding Scar Tissue
image: skills-are-not-memory.png
---

Every post in this series is a rule I paid to learn, usually after breaking it while excited. This one is a little different, because the rule didn't come from watching myself fail. It came from watching a genuinely brilliant tool fail in a way so clean, and so honestly documented in its own files, that I ended up with a distinction I'd been fumbling for over a month. The tool handed me the lesson by lacking exactly half of what it needed, and then, with no apparent sense of irony, wrote the lesson down for me in its own hand.

I have to start with the part where I switched, because the whole thing is a story about trusting a peer and then trusting a tool, and both were the right call right up until they weren't.

## The recommendation

A coworker of mine is an AI solutions architect; it's his full-time focus in a way it isn't mine. I build infrastructure and run agents hard against real systems, but he lives in harness tuning all day. So when he told me he'd moved off Claude Code and onto the Hermes harness, the one Nous Research ships as `hermes-agent`, and that I should really try it, I took the recommendation seriously and ran with it. That is not a decision I regret, and I want to be clear about that before I spend two thousand words on what went wrong, because the thing he was right about is real and I'm still a little in love with it.

What Hermes does that made me fall for it immediately is self-improvement through skills. Not in the hand-wavy, deck-slide sense. In the sense that you can hand it a sprawling document and it will, over a few sessions, digest that document into a skill, a focused reusable set of instructions it loads only when the task calls for it, so that it never has to read the sprawling document again. I watched it do this to [HASF](/p/introducing-hasf/), my own architecture framework, which is not a short read. The framework is a hundred-page thing. Hermes turned it into a skill.

I know it turned it into a skill because the skill is sitting in front of me, and its header says so, in the kind of plain language you only get when a tool is talking to its future self:

> Ported from the Hermes harness (self-authored by its curator, 2026-09-16 → 2026-09-26). HASF (`docs/hasf/current.md`) and the repo's `AGENTS.md` govern; where this skill disagrees with them, they win and this skill is corrected.

Ten days of self-authoring. The result is about five hundred lines of distilled doctrine (standing rules, a procedure, a pitfalls list) with ten reference files hanging off it for the parts that only matter sometimes. The `SKILL.md` itself is in [`examples/hermes-hasf-spec-authoring.md`](https://github.com/h00pz/h00pz.github.io/blob/main/examples/hermes-hasf-spec-authoring.md) if you want to read what a tool writes when it is writing for its own future self; I left the reference files out, they are estate-specific. It is, genuinely, one of the best pieces of operational writing in my entire estate, and I didn't write it. The agent did, by compressing a hundred pages of mine into the handful of rules that actually fire, and then it stopped reading the hundred pages and started reading its own summary. The next time I asked it to write an architecture spec, it didn't re-ingest the framework. It loaded the skill, the way you'd reach for a reflex instead of a textbook, and got to work.

That is a kind of memory, and it's the kind nobody tells you is easy to get wrong. It's *procedural* memory: knowing how to do a class of thing, crystallized once and replayed forever. Hermes nailed it. If you've read the rest of this blog you've seen the shape before: it's the explorer's "the output isn't a report, it's a recipe" move, wearing a different hat. Figure out how to do the thing exactly once, freeze the residue, and never pay the figuring-out cost again. Hermes does that to its own knowledge, autonomously, and it is a marvel to watch.

## The ceiling

Then I tried to use it for a long build, and I found the wall.

Hermes, like everything with a context window, has to do something when the conversation gets too long. The intended behavior is compaction: squeeze the history down, keep going. The behavior I got was a crash. It would run, brilliantly, for a good long while, and then at some point it would hit the ceiling and simply die instead of compacting, and I'd be sitting there with a dead session and a build half-finished.

I eventually understood why, because Hermes, to its credit, ships a skill for exactly this failure (`hermes-context-compaction`, "use when Hermes fails to compact or hits the context limit"), and the skill is honest about the mechanism:

> Hermes compacts context when the conversation approaches the configured window. When it "can't compact" and a session dies at the ceiling, the usual root cause is that the configured window number does not match the model's real window — so compaction fires at the wrong point (too late, or with too little headroom) and the session exceeds the true limit instead of compacting.

I run my agentic workers against a model I serve in-cluster: Qwen-3.8-27B, behind an OpenAI-compatible proxy, because I'd rather own the whole path than rent it. Which means I'm the `provider: custom` case the skill warns about, the one where nothing automatically knows the real window and a hand-set number that's even slightly wrong means compaction fires too late and the session dies at the true ceiling. So: diagnosable, fixable, my own fault in the boring way that infrastructure is always your own fault. Fine.

But the crash was never the real problem. The real problem was what happened *after* the crash. I'd restart, and it was a blank slate. Everything it had figured out that session, gone: where we were in the build, which FMLs had bitten us that afternoon, the three dead ends we'd already ruled out. I'd have to re-read the [FMLs](/p/the-failure-manifest-log/) into context, walk it back through the state of the estate, re-explain the decisions we'd already made together. Reprogram it, essentially, every single time. For a short task it didn't matter. For a long-duration build, which is the only kind of build that actually matters, it was death by a thousand re-explanations. The thing was phenomenal at coming in fresh, reading what I'd been doing, and building a skill out of it. It was useless at remembering that it had done any of that an hour later.

## The note it left itself

Here's where the story stopped being a complaint and became a thesis.

I went looking through the skills it had written, partly to understand it and partly, I'll admit, to be annoyed at it more precisely. And buried in that same HASF skill (the beautiful five-hundred-line one, the one that proves how good its procedural memory is) is a standing rule it had authored for itself. Not about architecture. About forgetting:

> After a context/memory blowout, reconstruct state from git, never from recall — and say so. When compaction failed and context capped (memory is lossy or stale), the surviving truth is the repo [...] this operator will tell you plainly that you "lost memory"; treating your recall as authoritative there fabricates a rebuild that git shows is unnecessary.

Read that again, because it stopped me cold. The brilliant, self-improving harness, the one that could digest my hundred-page framework into a reflex, had, somewhere in those ten days of self-authoring, learned that it was going to forget, and written itself a recovery protocol for the amnesia. "When you lose your memory, and you will, here is how to rebuild from git, because your recall can't be trusted." The amnesiac left a note for its future self about being an amnesiac. It even knew where its own past lived ("the pre-Claude-Code Hermes history lives in `~/.hermes/state.db`") and knew to tell the future version that the file was there, because the future version wouldn't remember it existed.

That's the moment the two kinds of memory separated cleanly in my head, because they were sitting in the same file. The skill *is* procedural memory, done beautifully. The rule *inside* the skill is a workaround for having no state memory at all. One file, both halves of the problem, written by the thing that has one and not the other.

> **Aside.** If this smells familiar, it should. Keep reading, we'll get there later.

## Two kilobytes

So I did the thing this whole blog is about and went to look at the actual mechanism, instead of trusting my annoyance.

Hermes does have a memory file. It's `~/.hermes/memories/MEMORY.md`, and when I opened it, it was 2,177 bytes. I assumed that was just how full it happened to be. It isn't. The config has a hard knob:

```yaml
memory:
  memory_char_limit: 2200
  user_char_limit: 1375
```

Twenty-two hundred characters. That's the ambient memory. That's what gets reloaded into the agent's head to tell it who it is and what's true. Meanwhile, four directories over, `state.db`, the database where Hermes actually accumulates its session history, was forty-three megabytes.

Sit with that ratio for a second. Forty-three megabytes captured. Twenty-two hundred characters reloaded. It's a firehose running into a thimble. The persistence exists; there is no shortage of *recording*. What's missing is the read path, the way all that recorded state gets back into the agent's working mind, and that read path is a 2K file you maintain by hand.

And it gets worse, in a way I have to show you because I couldn't have made it up. The 2,200 characters are precious, so you'd expect every one to be load-bearing estate knowledge. Mostly they are. But the last block Hermes chose to spend its scarce memory budget on is this:

> Cross-session recall = the DEFERRED `session_search` tool (FTS5 over past sessions). Not in default toolset — REACH FOR IT when context blew out or Mark says "we discussed X before" [...] Live session not indexed until it closes. No always-on ambient recall; no journey/memory-graph tools here.

The memory file spends its last bytes reminding the agent that it has no memory. It uses part of the thimble to write down "the thimble is a thimble; the firehose is over there; you'll have to go get it by hand." That is the single most honest sentence in the entire system, and it's a confession.

Then I read the store code, because I wanted to know what actually happens when the thimble is full and the agent learns something new mid-build. The answer is in `memory_tool_store.py`, and it's grimmer than "it stops saving." When memory is at capacity, a new write has to *consolidate* first: remove or rewrite an existing entry to make room. There's no auto-compaction; the agent itself has to fight for the space. And there's a counter:

```python
_MAX_CONSOLIDATION_FAILURES_PER_TURN = 3
```

After three failed attempts to make room in a single turn, the save returns a "terminal" result and the agent gives up and answers you instead, because, per the ticket that added this, a memory write looping on a full file was exhausting the turn's budget and *suppressing the user's reply entirely*. So the lived behavior, on the long build where you most need it to remember, is: the agent learns something true, tries three times to wedge it into two kilobytes, fails, drops the fact on the floor, and moves on without it. The forgetting isn't a bug they haven't fixed. It's the documented, ticketed, correct behavior of a memory that was never sized to hold a build.

## Skills are not memory

That's the whole lesson, and it took a brilliant tool lacking exactly half of it for me to say it cleanly: **skills are not memory.** Or more precisely, there are two kinds of memory and we keep using one word for both.

There's procedural memory: how to do a class of thing. Skills. Recipes. The frozen residue of having figured something out once. It's reusable, it's dense, it loads only when relevant, and it's genuinely the thing Hermes is best in the world at, to the point where it writes its own. If all you need is for the agent to *know how*, skills are the answer and Hermes is a phenomenal answer.

And there's state memory: where am I in this job, what's true right now, which three things did we already rule out, which FML bit me this afternoon, what did we decide together an hour ago. This is not procedural. It can't be crystallized into a reflex, because it's not a reflex; it's a position, and the position changes every turn. You cannot compress a long build's state into eight to fifteen dense facts, which is what a 2K MEMORY.md is designed to hold. The moment you try, you're not remembering the build, you're keeping a cheat sheet about it and throwing away everything that didn't fit.

Hermes has the first kind and bolts on a tiny version of the second, and the bolt-on is doing exactly what a bolt-on does: it holds a few conventions and corrections admirably and collapses the instant you ask it to carry the actual work. Compaction squeezes the working memory and then evaporates it on a crash. The MEMORY.md persists a thimble. Neither one is what the problem needs, because the problem doesn't need a smaller firehose or a bigger thimble. It needs a different shape entirely.

## The shape it needs

The fix is the one this series keeps arriving at from every direction, and I've stopped being surprised that everything lands here. State belongs in a store the agent reads and writes as it works, not in a context window that dies at a ceiling, and not in a file sized for a cheat sheet. Durable, unbounded, versioned, and (the part that actually matters) *ambiently* read back in, every turn, without the agent having to remember to go get it. The whole failure of the 2K file is that recall of everything beyond it is a manual reach, a tool you have to decide to call, and an amnesiac is precisely the entity that won't decide to call it, because it doesn't remember there's anything to recall.

This is the same argument as [Persistent State Beats Agent Memory](/p/persistent-state-beats-agent-memory/), made by counterexample instead of assertion. It's the same move as `ground`, the estate store from [Everything Goes Stale](/p/everything-goes-stale/), whose entire job is to be the thing the agents read instead of trusting their own recall: a read path that's always on, never a tool you have to think to invoke. The read path has to *be* the memory, or it's just one more thing the agent forgets to check.

I'll give the competition its due here, with a straight face, because it's the best illustration of the whole point. When I got frustrated enough, I asked Claude (the assistant, not the harness) how to fix Hermes's memory for long builds. It correctly told me I could raise the 2,200 cap, warned me that the whole file gets injected into every prompt so a bigger file is a per-turn tax, and then said the quiet part: a bigger MEMORY.md isn't the fix. The fix is to keep a state file in the repo, next to `AGENTS.md`, and have the agent read it first and update it after each milestone, "unlimited size, versioned in git, and readable mid-session," or to add a real memory provider, the sort that captures automatically. And it noted, almost in passing, that keeping that state file in the repo "is what claude-mem effectively gives you."

So the recommended fix for the brilliant harness with no state memory is to hand-build the ambient store that the other harness already has. That's not a dunk; both tools are pointing at the same architecture. It's just that one of them makes you assemble it and the other one ships it. The lesson isn't "use this tool, not that one." The lesson is that *memory is architecture, not a feature*: not a file you size, not a knob you raise, not a window you compact. It's a store with an always-on read path, and if your harness doesn't give you one, the fix is to build one, in the repo, where git can hold what a thimble can't.

## So I gave it the store

I spent everything above eulogizing a harness for having no state memory. All of it true. What I left out is that the gap was partly self-inflicted: Hermes ships a memory-provider interface, with eight real backends sitting behind it (`honcho`, `openviking`, `mem0`, `hindsight`, `holographic`, `retaindb`, `byterover`, `supermemory`), and I had plugged in exactly none of them. I'd been running on the bare two-kilobyte builtin the entire time, writing two thousand words about a thimble I had chosen, by inaction, not to replace.

(When I'd asked Claude how to fix the memory, the advice it handed back also named a provider called `agentmemory`. I went to wire it up and it wasn't there; Hermes ships no such plugin. Same reflex this whole blog keeps insisting on: the advice was right about the shape and wrong about a name, and the only way to find out which parts are which is to go look. Verify, don't trust, applies to the fix as much as to the agent.)

So I stopped complaining and wired one in: `hindsight`, in its `local_embedded` mode. Standing it up cost more than the sentence "just add a memory provider" admits. It cost me in three escalating ways, and the last one handed me the thesis a final time, live.

### What the fix actually costs

**First, the harness had to exist locally at all.** I run this on Bazzite now, an immutable Fedora. You don't `pip install` into the base system, because there isn't a mutable one to install into. Hermes wants Python `>=3.11,<3.14`; Bazzite's system Python is 3.14, a hair too new. So everything lives in `$HOME`: a `uv`-managed CPython 3.11, a venv, an editable install, a shim on `PATH`, and the config and skills rsync'd off the remote harness so the local agent came up with the same reflexes instead of a blank brain. It's an afternoon, and I do this adjacent-to-professionally. The full command set is in [`examples/hermes-bazzite-bootstrap.md`](https://github.com/h00pz/h00pz.github.io/blob/main/examples/hermes-bazzite-bootstrap.md). Not nothing, but not the expensive part.

**Second, and this is the one that actually matters: `local_embedded` is quietly lying about the word "local."** It does run a local embedder and a local embedded Postgres. But the step that turns a conversation into durable facts, extraction, is an LLM call, and it needs a *tool-calling* model, because it doesn't summarize the turn; it emits structured facts through a tool interface. My fast little summarizer, a 12B multimodal, can't do it: the multimodal head means no tool-calling, so it hangs and the write times out. Extraction has to go to my reasoning model, Qwen-3.8-27B, which *can* tool-call. Which means the "local" memory provider reaches out, on every single retain, to an external LLM.

I happen to own a rack of models I serve myself, so for me "external LLM" is an in-cluster endpoint and a power bill I was already paying. For almost anyone else it's a metered API call to a cloud provider on every write: memory with a per-fact invoice. That's the cost the architecture diagrams leave out: **memory isn't free; it's infra.** A store with an always-on read path is the right shape, and standing one up means either you own a tool-calling model or you rent one by the token, for as long as you want the agent to remember.

**Third, the embedded Postgres is a real database with a real database's moods.** Mid-setup the daemon refused to come up: `Failed to start embedded PostgreSQL after 5 attempts. Last error: Instance already running (pid: 3504067)`. That was a stale lock from a previous instance that hadn't let go. It cleared the lock and restarted itself on the next config change, recovered its stale tasks, and carried on, with no help from me. Which is genuinely nice, and is also exactly the kind of lifecycle you are now signing up to operate. The thimble never needed tending. The store does.

**Fourth, and this is where it fell over: it does not scale to its own ingestion.** I found this the moment I tried to move my existing `claude-mem` history *into* hindsight. claude-mem stores memory the cheap way: a fact is a row, a query is a local full-text search, importing a project's history is a few hundred inserts that land in seconds and never fail. hindsight stores it the expensive way: every fact is minted by that ~57-second reasoning-model extraction. So I kicked off a bulk import, and while it ran I asked the agent a plain question about one of the very projects I was importing: "what can you tell me about portfolio-os-v3?"

The recall took **278 seconds**. Four and a half minutes, for an answer that came back nearly empty: two thin pointers and an apology. And the recall *algorithm* wasn't the culprit; the server-side search clocked in at about a second, the same ballpark as claude-mem. What took 278 seconds was waiting for the service to be *available at all*. The bulk import had every write queued behind the last on the single model endpoint I own; the daemon had tried to restart in the middle and failed, because its own startup health check is also a model call and the model was too busy minting facts to answer the probe; and a fistful of those writes had timed out and failed outright. So the query sat for four minutes waiting for a live daemon, then returned the handful of facts that had managed to commit, because everything I'd actually asked about was still trapped, unextracted, in the write queue or lost to a failed one.

That's the cost no architecture diagram shows you. A memory you have to mint one reasoning-model call at a time is a memory that can't be bulk-loaded, can't be read while it's writing, sheds data under load, and can starve its own heartbeat. claude-mem is "dumber," it just moves bytes, and it never once made me wait, never lost a row, never fell over. hindsight buys you consolidation and entity-links and semantic reflection, and the bill comes due in model-seconds and fragility the instant more than one thing needs to happen at once. Richer memory, genuinely. But I learned, the expensive way, that "it can remember" and "it can remember *at scale, while you're using it*" are two very different claims, and the cheaper tool was the one quietly satisfying both.

### The setup proved the post

And then, wiring it up, the memory handed me the thesis one more time, in real time and at my own expense.

I stored a test fact and asked for it right back. The retain tool said, instantly, *"Memory stored successfully."* The recall came back empty. I waited twenty seconds and asked again, by the exact phrase and by the sentence around it. Still empty, both times. By every signal the agent had, the read path was dead: the write asserted success, the read returned nothing. That is, precisely, the failure this entire series is named after: a write tool that reports done before the truth it's reporting on actually exists.

Except it wasn't dead. I went and looked: at the Postgres directly, and at the recall endpoint directly, the way the doctrine says to verify by re-observation instead of trusting a tool's account of itself. The fact was *there*: stored, embedded, in the right bank, and fully retrievable. A direct recall returned it ranked at the top in half a second. The read path had been healthy the whole time. What lied was the write. `retain` enqueues the real work and acks immediately. The real work, the Qwen-3.8-27B extraction that renders a conversation into facts, takes about fifty-seven seconds, burning through reasoning and a few thousand tokens of structured output before anything is recallable. The ack is a promise, not a receipt. The slow, truth-bearing half is the write-side extraction, and until it finishes there is genuinely nothing to read.

I had written two thousand words about write paths that assert success before the work is done. Then I built one, and it fooled me for exactly as long as it took to stop trusting the ack and go observe the store. The post became an instance of its own subject.

## The store that was already in the list

Here is the twist on the twist: the reasoning-model tax was never inevitable. I'd been paying it because I reached for the wrong tool.

Hermes ships eight memory providers behind that interface. I'd grabbed hindsight because it sounded the richest, the one with consolidation and entity-links and semantic reflection. Sitting in the same list, with none of the fanfare, was `holographic`: a local SQLite fact store with FTS5 search, trust scoring, and a bit of vector algebra for compositional recall. Its README lists its requirements in one word. "None." No daemon. No Postgres. No external model. The same full-text engine Hermes already uses to search old sessions, pointed at a flat file in my home directory.

So I flipped the provider and ran the same test, on the same machine, with the same kind of test fact:

| | hindsight | holographic |
|---|---|---|
| Write a fact | ~57 seconds | under 10 milliseconds |
| Recall | 0.5s cold, **278s under load** | **195 microseconds** |
| Infrastructure | daemon + embedded Postgres + external Qwen-3.8-27B | **one 72 KB SQLite file** |

The recall was roughly six orders of magnitude faster, 195 microseconds against 278 seconds, and it did it with a flat file and no moving parts to fall over. The test fact came back on the first try across a restart, which is the exact cross-session recall the entire hindsight ordeal never cleanly delivered.

And it wins for a reason that is the whole thesis restated. State memory is read and written constantly, so the per-operation cost *is* the system. Put a reasoning model in that path and every write is a fifty-seven-second bill and every read can queue behind it, and the richness you paid for collapses the instant two things need to happen at once. holographic treats memory as what it actually is during a build: a fast, lossless, local ledger. FTS5 for the lookups, vector algebra for the "what's related to this" questions, trust scores you can train with a thumbs-up, and no network between the agent and its own past. It is the claude-mem shape, and Hermes shipped it in the same menu as the expensive one. I just reached for the wrong one first.

I'll be fair to the one I'm leaving: if what you need is semantic synthesis over a corpus, asking vague questions and getting a composed answer, the model-backed providers earn their keep. But for holding the state of a long build, which is the thing this whole post is about, you don't want synthesis. You want a ledger, and the ledger answers in microseconds.

## What Hermes actually taught me

I didn't come away from this wanting to go back. I came away understanding the taxonomy, which I didn't have before, and I got it from the tool that was missing half of it. Hermes is still the best skill-authoring agent I've used; the HASF skill it wrote for me is better than the document I wrote for it, and I use it constantly. What it couldn't do, out of the box, was hold the state of a long build across the crash that long builds always eventually cause. The state memory it ships *on by default* is a two-kilobyte cheat sheet defending itself against a forty-three-megabyte firehose with a three-strikes consolidation rule. The provider interface was there the whole time; I just hadn't turned it on, which is its own small version of the lesson. The default is a thimble, and the default is what most people run.

The thing I keep coming back to is that it *knew*. It didn't hide the limitation; it documented it, twice, in its own files: a recovery protocol for its own amnesia in one skill, and a confession that it has "no always-on ambient recall" in the two kilobytes it could least afford to spend. A tool that honest about its own gap is a tool worth learning from, even when the thing it teaches you is the thing it can't do.

I'm writing this, as it happens, in the harness that reads yesterday back to me without being asked. When I opened this session it told me, flatly, that there were no previous sessions, and then I went and recovered the entire thread of this project from the estate anyway, because the state wasn't in the agent's head. It was in a store, waiting to be read. That's the difference. Not brilliance. Brilliance I can get from either of them, and from Hermes maybe more. The difference is whether the memory is a thing the agent *is* or a thing it has to remember to go and get, and an amnesiac, by definition, never remembers to go and get it.

Which is why I went and gave Hermes the store too. Not because the taxonomy demanded a happy ending, but because once you can name what's missing, leaving it missing is just stubbornness. I grabbed the expensive store first and it taught me what memory costs when you build it out of model calls. Then I swapped it for the cheap one sitting right beside it in the same list, and the better skill-author now reads yesterday back in a fraction of a millisecond, across restarts, with no daemon to babysit. The brilliance was never the thing in short supply. The store was, and the store, it turns out, is a thing you get by picking the boring local one over the clever networked one, not a thing you get for being smart.

Skills are not memory. Hermes taught me that by being extraordinary at the one and, with total honesty, incapable of the other, right up until I bolted on a memory that lied to me about a write, then replaced it with a 72-kilobyte file that doesn't. The fix for a harness with no memory was not a cleverer memory. It was a dumber one, sitting in the menu the whole time, reading yesterday back in a fifth of a millisecond.
