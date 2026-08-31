---
title: "How Big Is a Model, Really?"
slug: how-big-is-a-model-really
date: 2026-08-31
draft: false
description: "24 GB sounded like a lot until a model took 21 of it just to boot. Parameter count tells you how big a model is, not how big your workload is."
tags:
  - model-selection
  - gpu
  - model-serving
  - slm
  - openshift
categories:
  - OpenShift and AI
image: how-big-is-a-model-really.png
---

I built my cluster around RTX 3090s because 24 GB of VRAM sounded like a lot of memory. The math I did in my head was the math everyone does: the model is some number of billion parameters, I'll quantize it, the weights will fit in 24 GB, and I'm done. That assumption lasted about five minutes into actually serving something, because it answers a question I thought was the important one and turns out to be almost beside the point. The weights fitting tells you the model can load. It tells you almost nothing about whether the thing you actually want to run can run.

This is the first post in a series about doing AI on OpenShift, and it starts with the question I got wrong first. My cluster is called Darkpool. It's three nodes, blade, deadpool, and logan, each with a single 24 GB RTX 3090, built for local, sovereign inference that stays on my hardware instead of quietly spilling into somebody's hosted API. And the first thing Darkpool taught me is that "how big is this model" is a much slipperier question than a parameter count, because the honest answer depends on what you're asking the model to do.

## Three Kinds of "Fits"

Once I started paying attention, the word "fits" split into three.

**Weight fit** is the one everybody computes: can the model's parameters, at whatever precision, become resident in VRAM? This is the sizing-calculator question, and it's real, but it's the floor.

**Context fit** is the next one: can the model hold the amount of prompt state your application actually hands it? Because a served model doesn't just store its weights. For every token in the current request it keeps a running store of attention state, the Key-Value cache, so it doesn't have to recompute the whole history on every new token it generates. That cache lives in VRAM, and it grows with the length of the context. Context isn't a setting. It's memory you're spending on top of the weights.

**Workload fit** is the one that actually decides whether a deployment works: can the card hold the weights, plus the context you need, plus room for the output, plus however many requests arrive at once, all at a latency you can live with? That's the question an OpenShift deployment cares about, and it's the one no paper spec answers.

A model that uses 21 GB of a 24 GB card technically fits. Operationally it can be useless, because there's no room left for the very context and concurrency that made you want the model in the first place. Weight fit is a green checkmark that lies to you.

## The Qwen Experiments

Darkpool's model story is really a sequence of me learning that lesson the expensive way.

The first model was **Qwen3-8B**, in FP8, and it earned its place by being the boring, validated thing that ran comfortably on a single 3090. FP8 there means the weights are stored as eight-bit floating-point numbers rather than the sixteen bits the model was trained in, which roughly halves the memory the weights take for a small, usually acceptable hit to precision. That's the first lever you reach for to make a model fit at all, and it's worth knowing it's a lever and not a free lunch. Every system needs one known-good bootstrap target before it starts getting clever, and this was mine: enough for mechanical extraction, small enough to leave real headroom, a floor I could build on.

Then I tried **Qwen3-14B**, also FP8, and it became my favorite example of the trap. At a 32K context its serving footprint sat around 21 GB of the 24. It fit. It also ate nearly the whole card to do it, which meant almost nothing left for longer context or a second concurrent request. And the part that actually stung: the extra parameters didn't move the needle on the semantic problems I cared about. It matched the little 8B on the exact failures that were the whole reason I might want a bigger model in the first place, including the Gold supersession trap. The infrastructure cost went up. The application value didn't. Both of those assumptions, "if it fits it's usable" and "bigger parameters buy better answers," broke in the same experiment.

Then I reached for **Qwen3.5-35B-A3B**, and the name itself is a lesson. It's a Mixture-of-Experts model: roughly 35 billion total parameters, but only about 3 billion active for any given token. It's tempting to read "A3B" as "sizes like a 3B model." It doesn't. The 3 billion is how much compute runs per token. All 35 billion parameters still have to be resident, because the model doesn't know in advance which experts a token will need. That's the difference between how much a MoE model computes and how much it has to keep in memory, and it's the reason that model pushed me off a single card and into sharding it across GPUs with a distributed runtime like vLLM on Ray.

Which surfaced the next misconception, worth stating flatly because it's seductive:

> A cluster with 72 GB of GPU memory across three cards does not behave like one 72 GB GPU.

Model parallelism has to be done by the inference engine. The weights get partitioned, and now attention and activations cross GPUs, and on Darkpool that means crossing a 10 GbE network, which becomes part of your inference latency whether you planned for it or not. A serving-orchestration layer on top doesn't magic three cards into one big transparent pool. The advertised parameter count tells you none of this.

## Then Gemma Broke My Mental Model

By this point I'd stopped hunting for one model to rule them all and started testing Gemma for specific jobs. A whole wave of those went by, a Gemma 3 12B, a Gemma 4 31B that led on structural reasoning, and the Gemma 4 26B that eventually became my judgment model. But the experiment that actually rewired how I think came from a narrow one. I needed a high-context compiler: something to read a large pile of material and shape it into structured evidence. Not to make decisions, not to recommend anything, just to ingest a lot and produce a clean artifact. I put a Qwen and a Gemma head to head for that bounded role, and **Gemma 4 12B** won, on numbers I didn't believe at first.

Running under llama.cpp, this one was Q4 quantized, a heavier compression than the FP8 above that squeezes each weight down to about four bits, shrinking the model further again and leaving even more of the card free for context. With flash attention on, reasoning off, and a single sequence, this is what the smaller model did:

| Gemma 4 12B (llama.cpp, Q4) | Result |
| --- | ---: |
| Context at ~9.7 GB | **128K tokens** |
| Context at ~10.2 GB | **222K tokens** |
| Needle-in-a-haystack recall | 100% |
| Decode throughput | ~65 to 86 tok/s |
| 144K-token prefill | ~49.6 sec |

Set that against the earlier data point: my Qwen comparison lane was using roughly 21.6 GB at a 96K context. So one model was brushing the ceiling of a 24 GB card at 96K, and another was sitting around 10 GB while running well past 128K. Same class of hardware. A "smaller" model, by parameter count, with dramatically better context economics.

That's the whole reveal, and it's why "how many parameters?" is the wrong opening question. Parameter count did not predict the thing I actually cared about, which was how much context I could carry and what it cost me to carry it. That number is set by the model, the quantization, the inference engine, and the KV-cache configuration together, and llama.cpp's memory behavior on this particular model is doing a lot of the work. The meaningful unit isn't "Gemma 12B." It's model plus quantization plus engine plus context config plus workload. Two deployments of nominally the same model can have completely different memory profiles, and the sizing table on a model card knows about exactly one of those factors.

The academic version of this point is worth a link, because it's the clearest statement of why the cache dominates: the vLLM team's <a href="https://arxiv.org/abs/2309.06180" target="_blank" rel="noopener">PagedAttention paper</a> reframes LLM serving as fundamentally a KV-cache memory-management problem. Different engine, same physics. Context is memory, and how well an engine packs that memory is most of the game.

## The Actual Timeline

None of this was the clean three-step story the sections above might suggest. It was a couple of months of testing, in waves, and the real log looks more like this:

| Date | Model | What I was testing | What happened |
| --- | --- | --- | --- |
| May 17 | Qwen3-8B (FP8) | single-3090 bootstrap, extraction | the baseline; fit comfortably, good at mechanical extraction |
| May 17–18 | Qwen3-14B (FP8) | does more VRAM buy better judgment? | ~21 GB at 32K, matched the 8B on the Gold trap, parked |
| May 18 | Qwen3.5-35B-A3B (FP8) | larger MoE deep-ingest and nuance | pushed me to distributed vLLM/Ray; total residency mattered despite ~3B active |
| May 18 | Qwen2.5-14B-Instruct-1M | long-context middle tier | huge advertised window, not the winner |
| May 18 | Gemma 3 12B | native long-context alternative | native 128K made it worth a serious look |
| May 24 | Gemma 4 31B | structural reasoning and judgment | the structural leader that wave |
| May 24 | Gemma 4 26B-A4B | faster Gemma alternative | promising, inconclusive at first |
| May 28 | Qwen3-8B + Gemma 4 26B-A4B (GGUF) | real evidence-ingest routing | a scar: Gemma passes were misrouted to Qwen until per-alias routing and provenance got fixed |
| June 10 | Gemma 4 26B | pairwise adjudication vs the thesis graph | clean, ten groups no failures; became the governed judgment model |
| June (later) | Gemma 4 12B | high-context compiler | the memory surprise, and ultimately the compiler choice |
| June/July | a Qwen comparison lane | long-context compiler | ~21.6 GB at 96K (exact checkpoint still to verify) |
| June/July | Gemma 4 12B (Q4-QAT GGUF) | maximum and practical long context | 128K at ~9.7 GB, 222K at ~10.2 GB, 100% recall; settled near 160K, ~144K in, ~16K out |

Three rough waves are visible in there. The first was just *how much model can I get onto a 3090*, which is how the 8B and then the 14B happened. The second was *which model is better at which job*, once the 8B and 14B tied on the Gold trap and Gemma started pulling ahead on nuance. The third was memory and context blowing up the simple sizing model entirely, where a 12B became the high-context compiler, the 26B became the adjudicator, and the 8B stayed the mechanical extractor. The coding-assistant, vision, and speech models I also ran through Darkpool are a different branch of the story, left out here on purpose.

## So, How Big Is a Model?

Line the experiments up and the question in the title falls apart in a useful way. Qwen3-8B is small and leaves room. Qwen3-14B is bigger and leaves almost none. The 35B MoE is enormous in memory and modest in compute. And a 12B ran more context on half the VRAM of a 14B. Every one of those is the same nominal "how big," and they answer completely differently, because size isn't a property of the weights. It's a property of the weights plus the quantization plus the engine plus the context you ask it to hold plus how many callers hit it at once.

So the honest answer to "how big is this model" is a question back: to hold what, on what, for how many people? Parameter count tells you how big the model is. It tells you nothing about how big the *workload* is, and the workload is the thing your GPU actually has to contain.

I'll flag one honesty about my own numbers before I hand off. The Gemma memory figures came out so close across 128K and 222K that I want to be careful I was reading actively-used VRAM and not a preallocated cache, and the exact Qwen checkpoint behind that 21.6 GB is the kind of thing I'd pin down before betting anything larger than a blog post on it. Real measurements still carry the method they were measured with, and I'm reporting these as what I saw, not as a benchmark I'd defend to three decimal places.

That leaves the question the Gemma result opened and didn't answer. If a 12B can carry two hundred thousand tokens of context, how much of that should I actually use? Because it turns out the amount of context your application needs, the amount your hardware can sustain, and the amount the model advertises are three different numbers, and confusing them is its own expensive mistake. That's the next post.
