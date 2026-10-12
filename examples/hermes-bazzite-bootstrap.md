# Bootstrapping the Hermes harness on Bazzite

Companion to [Skills Are Not Memory](/p/skills-are-not-memory/). This is the full
command set for standing up Nous Research's `hermes-agent` on an immutable Fedora
desktop (Bazzite / Kinoite 44), plus the `hindsight` memory provider in
`local_embedded` mode. Everything lives in `$HOME` — no `rpm-ostree` layering, no
`sudo`, nothing that needs a reboot.

## Why it's fiddly

- **Immutable base.** The OS root is read-only. You don't `pip install` into the
  system; there isn't a mutable system to install into. Userspace tooling comes
  from `brew`/`uv`/containers and lives under `$HOME`.
- **System Python is too new.** Hermes needs `>=3.11,<3.14`. Bazzite ships 3.14.
  `uv` solves this by fetching its own CPython — you never touch the system one.

## 1. Toolchain

```bash
# uv provides the Python + venv management; brew for the odd userspace binary.
# (uv may already be present via brew; install if not.)
command -v uv || brew install uv
```

## 2. Hermes source + venv

```bash
# Clone and pin to the same commit the remote harness runs, so local == remote.
git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
cd ~/.hermes/hermes-agent
git checkout 03b0c79          # main @ v0.21.3 at time of writing

# uv downloads CPython 3.11 itself — system 3.14 is too new for hermes.
uv venv ~/.hermes/venvs/hermes-dev --python 3.11

# Editable install with all extras (includes the memory providers).
VIRTUAL_ENV=~/.hermes/venvs/hermes-dev uv pip install -e ".[all]"

# Put a shim on PATH so `hermes` just works.
mkdir -p ~/.local/bin
ln -sf ~/.hermes/venvs/hermes-dev/bin/hermes ~/.local/bin/hermes
```

## 3. Configure Hermes

Fresh install: let the wizard write the config. It creates `~/.hermes/config.yaml`,
an empty `memories/`, and registers the built-in skills.

```bash
hermes setup        # interactive wizard; writes ~/.hermes/config.yaml
```

You start with the shipped skill library. Project-specific skills you add yourself
(for example the Hermes-authored HASF spec-authoring skill in
[`examples/hermes-hasf-spec-authoring.md`](https://github.com/h00pz/h00pz.github.io/blob/main/examples/hermes-hasf-spec-authoring.md)),
and the agent writes more as it digests your work.

> **Already running Hermes on another machine?** You can clone its reflexes instead
> of redoing the wizard: rsync its config, skills, and memory across. Skip the
> multi-gig venv and the large `state.db` — both are machine-local and rebuild
> fresh. This is the shortcut I used off my own remote; it is not a requirement,
> and it only helps if *you* already have a harness to copy from.
> ```bash
> REMOTE=you@your-existing-hermes-host     # your box, not mine
> rsync -av $REMOTE:~/.hermes/config.yaml  ~/.hermes/
> rsync -av $REMOTE:~/.hermes/skills/      ~/.hermes/skills/
> rsync -av $REMOTE:~/.hermes/memories/    ~/.hermes/memories/
> # NOT copied: ~/.hermes/venvs (rebuilt above), ~/.hermes/**/state.db (starts fresh)
> ```

## 4. Auth

Register a credential for the `anthropic` provider. The Claude Pro/Max login is
OAuth, **not** an API key: Hermes stores it as a pooled OAuth credential and opens
a browser for you to sign in.

```bash
hermes auth add anthropic --type oauth   # opens a browser; sign in with Claude Pro/Max
hermes auth status anthropic             # confirm it registered
hermes -z "say hi"                       # smoke test; should return a completion
```

(Prefer an Anthropic API key? `hermes auth add anthropic --type api-key`. Then the
gotcha below does not bite, because a key *can* be handed to a subprocess.)

> **Gotcha that matters later:** Pro/Max is OAuth, not a key. Any *subprocess*
> that wants its own API key — notably hindsight's extraction LLM — cannot borrow
> this credential. It has to point at a model you control. See step 6.

## 5. Memory provider: `holographic` (recommended)

This is the one to use for holding build state. It is a local SQLite fact store
with FTS5 search, trust scoring, and HRR vector algebra for compositional recall.
Its README lists requirements in one word: "None." No daemon, no Postgres, no
external model, nothing on the network between the agent and its own past. Writes
land in under 10ms; recall is in the microseconds. It is the `claude-mem` shape,
native to Hermes.

Set it as the provider in `~/.hermes/config.yaml`:

```bash
hermes config set memory.provider holographic
```

Recommended config under `plugins.hermes-memory-store` in `config.yaml`:

```yaml
plugins:
  hermes-memory-store:
    db_path: ~/.hermes/memory_store.db   # default; SQLite file, created on first write
    auto_extract: "true"        # change from default false — ambient capture at session end
    default_trust: 0.5          # neutral prior; fact_feedback trains it up/down
    min_trust_threshold: 0.3    # recall noise gate; drop to 0.0 in the first sessions
    hrr_dim: 1024               # HRR vector width (NumPy optional); fine as-is
    hrr_weight: 0.3             # rerank blend (FTS 0.4 / Jaccard 0.3 / HRR 0.3)
    temporal_decay_half_life: 0 # days; 0 = off. Set 30–90 once you have volume
```

The two that matter:

- **`auto_extract: "true"`** is the difference between ambient and manual. Off
  (the default), facts land only when the agent explicitly calls `fact_store add`,
  which an amnesiac forgets to do. On, it regex-extracts prefs/decisions/project
  facts at session end. The extraction is regex, not an LLM, so it is instant and
  free; there is no cost reason to leave it off.
- **`temporal_decay_half_life`** is a freshness knob: fresher facts outrank stale
  ones. Start at 0 to see raw recall, then set 30–90 days once the store has volume.

There is **no char limit** here (the builtin `memory.memory_char_limit: 2200`
thimble does not apply to a provider store); it is unbounded SQLite.

Verify directly, with no password, no daemon, and no endpoint:

```bash
sqlite3 ~/.hermes/memory_store.db "select count(*) from facts;"
# Time a recall (expect sub-millisecond):
sqlite3 ~/.hermes/memory_store.db ".timer on" \
  "select f.fact_id, substr(f.content,1,70) from facts_fts fts \
   join facts f on f.fact_id = fts.rowid where facts_fts match 'your query';"
```

## 6. Memory provider: `hindsight` (the heavy alternative)

Use this only if you need semantic synthesis over a corpus, not build state. It is
far more expensive: every fact is minted by a reasoning-model extraction (~57s),
and the service is a daemon + embedded Postgres + an external tool-calling LLM. It
does not scale to bulk ingestion and can starve its own health check under load
(measured here: 278s recall while a bulk import saturated the one model endpoint).
Prefer `holographic` unless you specifically need the synthesis.

`local_embedded` runs a local embedder (bge-small) + cross-encoder reranker and a
**local embedded Postgres** (pgvector), but fact *extraction* is an LLM call that
needs a **tool-calling** model. Point it at a model you serve.

`~/.hermes/hindsight/config.json` (the load-bearing fields):

```json
{
  "mode": "local_embedded",
  "llm_provider": "openai_compatible",
  "llm_model": "qwen3-8-27b",
  "llm_base_url": "https://qwen3-8-27b-model-serving.apps.darkpool.h00pz.co/v1",
  "bank_id": "hermes",
  "recall_budget": "mid"
}
```

Notes learned the hard way:

- **The extraction model must support tool-calling.** hindsight emits structured
  facts through a tool interface; it does not summarize. A multimodal model
  (e.g. a 12B-MM) typically has no tool-calling and will hang → the retain times
  out. A reasoning model that tool-calls (Qwen-3.8-27B) works.
- **Extraction is slow.** A real turn extracts in ~55–60s on Qwen-3.8-27B (reasoning +
  a few thousand output tokens). `retain` is async — it acks immediately and the
  work finishes in the background. Do not judge recall until the queue drains.
- **The embedded Postgres has a lifecycle.** It can idle out (idle-timeout 300s)
  and can refuse to start on a stale lock ("Instance already running (pid …)").
  The daemon self-recovers on the next config-change restart; the data lives under
  `~/.pg0/instances/hindsight-embed-<profile>/`.

## 7. Verify hindsight by re-observation, not by the ack

The `retain` tool says "Memory stored successfully" the instant it enqueues —
before extraction has run. To actually confirm the store works, look at it
directly instead of trusting the tool:

```bash
# Count what landed (password is in ~/.pg0/instances/.../instance.json):
PGPASSWORD=hindsight ~/.pg0/installation/*/bin/psql \
  -h 127.0.0.1 -p 5432 -U hindsight -d hindsight \
  -c "select count(*), count(embedding) from memory_units;"

# Hit the recall endpoint directly (bank must match config bank_id):
curl -s -X POST \
  http://127.0.0.1:9177/v1/default/banks/hermes/memories/recall \
  -H 'content-type: application/json' \
  -d '{"query":"<something you just stored>","budget":"mid","max_tokens":2048}'
```

If the fact is in `memory_units` with an embedding and the recall endpoint returns
it, the store is healthy — any "empty" result from the agent's own recall tool
right after a write is extraction latency, not a dead read path.
