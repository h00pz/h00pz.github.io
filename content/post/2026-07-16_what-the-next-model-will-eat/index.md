---
title: "What the Next Model Will Eat"
slug: what-the-next-model-will-eat
date: 2026-07-16
draft: false
description: "The harness you build for today's model is mostly debt. But seams, state, and ownership aren't scaffolding for a weak model; they're the shape of the problem."
tags:
  - ai
  - architecture
  - agents
  - systems
  - seams
categories:
  - AI Coding Scar Tissue
image: what-the-next-model-will-eat.png
---

There's a strong argument against almost everything I've written on this blog, and it deserves to be stated at full strength before I answer it, because I think it's half right and the half it gets right matters.

The argument goes like this. Every piece of structure you build around a model is scaffolding for the model you have today, and the model you have today is the worst one you'll ever use. A well-engineered harness in 2026 is a 2026 artifact. Bigger context windows already ate a lot of retrieval machinery, better tool-calling ate a lot of orchestration code, and the next release will eat whatever you're proudest of right now. So treat your scaffolding as a <a href="https://leehanchung.github.io/blogs/2026/05/08/hidden-technical-debt-agent-harness/" target="_blank" rel="noopener">90-day artifact</a>, build as little of it as you can, and before you add any component ask one question: if the next model is twice as good, does this become unnecessary? If the answer is yes, don't build it. The model is becoming a better architect than you, and <a href="https://corti.com/your-prompts-are-technical-debt-why-scaffolding-built-for-older-models-hinders-newer-ones/" target="_blank" rel="noopener">your job is to get out of its way</a>.

Underneath that is an older and heavier idea, <a href="https://www.econlib.org/econlog/learning-the-bitter-lesson-in-2026/" target="_blank" rel="noopener">Sutton's bitter lesson</a>: across the history of AI, general methods that ride raw computation have beaten hand-engineered human knowledge every time, and it hasn't been close. If that's true, then all my careful seams and rules are exactly the kind of human-curated structure the next wave of scale washes away.

I take this seriously, and I want to be honest that I've been burned by the thing it warns about. I have built retrieval machinery that a larger context window later made pointless. I have written prompt gymnastics to coax valid output out of a model that a better model produced for free. That work was scaffolding, it was debt, and deleting it felt great. So when someone says most of what people build around models is temporary, I don't argue. I've thrown away plenty of my own.

## Two Things Are Both Called Scaffolding

The mistake in the argument isn't its test. The test is good, and I use it now. The mistake is that "scaffolding" is being used for two completely different things, and only one of them is debt.

The first kind is structure that compensates for a limitation of the model. Prompt tricks that force valid JSON, retry loops that paper over flaky tool use, retrieval hacks that exist only because the context window was too small, elaborate instructions that talk a weak model through a task a strong one just does. Every bit of that is betting against the model, and it's a bad bet, because the model is the one thing in the system guaranteed to improve. This is the scaffolding the bitter lesson eats, and it should. Build as little of it as you can stand. The people building agents seriously say the same thing, from the other direction: Anthropic's own <a href="https://www.anthropic.com/engineering/building-effective-agents" target="_blank" rel="noopener">guidance for building agents</a> is to prefer deterministic code and simple composable patterns and to reach for autonomous machinery only when a task genuinely needs it. Minimizing this pile isn't a fringe position. It's the mainstream one.

The second kind isn't compensating for the model at all. It's encoding the shape of the problem. A seam that defines what crosses the boundary between two subsystems. A store that records what the system believed and when. A rule about who owns a piece of state so that two components can't both think they own it. A deterministic service wrapped around a probabilistic core so the probabilistic part can't reach the levers it shouldn't touch. None of that exists because the model is weak. It exists because the problem has structure that's true regardless of how smart the thing in the middle gets.

The test the harness-debt argument hands you is the exact tool for telling these apart, so let me actually run it, honestly, on my own work.

## Running the Test

If the next model is twice as good, does the prompt that coaxes it into valid JSON become unnecessary? Yes. Delete it. Scaffolding.

Does the retrieval layer I built for a small context window become unnecessary? Maybe. A bigger window might eat it, and one already did once. Mostly scaffolding, and I hold it loosely.

Does the outbox that keeps a store and a queue from tearing apart on a failed write become unnecessary? No. A perfect model does not fix a [dual write](/p/architecture-after-agents/); a half-completed write is a systems problem, and the fix is a decades-old pattern that has nothing to do with intelligence. Durable.

Does the [bitemporal store](/p/persistent-state-beats-agent-memory/) that can tell me what the system believed last Tuesday become unnecessary? No. A smarter model still can't reconstruct a past belief from a chat log it wasn't keeping. That's a property of the data architecture, not the reasoning. Durable.

Does the [seam](/p/the-seam-is-the-product/) between one subsystem and the next become unnecessary? No. Two perfect models collaborating through a shared, unstructured, mutable medium still drift, because the drift comes from the medium, not from a lack of intelligence at the ends of it. Durable.

Does the [supersession gate](/p/the-gold-trap-small-models-are-not-interchangeable/) that refuses to ship a recommendation once its own falsifier has fired become unnecessary? No. A better model can be argued out of a supersession the same way a worse one can; the gate holds because it's deterministic and doesn't have an opinion. Durable.

Notice the pattern. The things that pass the test, the ones a better model deletes, are all compensating for the model. The things that fail it, the ones that survive every release, are all about ownership, state, boundaries, and consequences. The bitter lesson is real, and it is pointed at the first pile. It has nothing to say about the second.

## Capability Is Not Operability

The deeper reason the bitter lesson doesn't reach the second pile is that it's an argument about how you get *capability*, and seams and state aren't capability. They're operability. They're what it takes to run a system that touches real money and real consequences without lying to you about what it did.

Sutton's canonical example proves the point better than my counterargument does. AlphaZero threw away every hand-coded chess heuristic and learned to play from scratch, and it demolished the systems built on human knowledge. But AlphaZero still runs inside a program that owns the rules of chess, the board representation, and a move validator it does not get to hallucinate. The bitter lesson ate the chess *strategy*. It did not eat the requirement that a move be legal, that the board have one authoritative state, and that an illegal move be rejected by something that isn't the model. Nobody proposes letting the network invent whether its rook can teleport, and a system that moves money needs at least that much rigor about what its workers are allowed to do.

This is the category error underneath the whole debate. "The model will get smarter" is true. "Therefore the system needs no architecture" does not follow, any more than a better chess player needs no board. Confusing the intelligence with the system it runs inside is exactly the mistake that [built the version of PortfolioOS I threw away](/p/why-we-threw-away-portfolioos-v2/): I let the model be the architecture, and the architecture is the part that has to still be standing when the model underneath it gets replaced.

Which is the whole point of [treating the model as replaceable](/p/the-model-is-not-your-architecture/) in the first place. The reason I can swap the model without redesigning the application is precisely that the durable structure isn't scaffolding for that model. It would be there for any model, including a perfect one, because it's holding the shape of the problem, not holding up a weak reasoner.

## Where I Might Be Wrong

I want to end this honestly, because the argument I'm answering has a real edge and I don't get to wave it away.

The boundary between the two piles moves, and it moves in the direction that's bad for me. Bigger context genuinely did eat some of my retrieval. Better tool-calling genuinely did eat some of my orchestration. I can't promise that something I currently file under durable architecture won't turn out, two releases from now, to have been compensating for a limitation I couldn't see because I'd never used a model without it. I've been wrong about that boundary before and I'll be wrong about it again, so I run the twice-as-good test on everything now, and I delete what fails, and it usually stings a little because I was proud of it.

What I can say is narrower and, I think, survivable. The specific things this whole series is about, the seams, the authoritative state, the explicit ownership, the deterministic services around probabilistic cores, and the definition of done you can prove against reality, have kept passing the test through every model release I've lived through. I haven't yet watched a model absorb one of them, because none of them were ever about the model. This isn't me betting against better models. It's the opposite. It's the architecture I build *so that* a better model is a drop-in upgrade instead of a rebuild, which is only possible if the architecture was never propping the old one up to begin with. Build as little scaffolding as you can. Then build the seams, because those aren't scaffolding, and the next model isn't going to save you from having to draw them.
