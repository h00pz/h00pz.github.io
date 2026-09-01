#!/usr/bin/env python3
"""
OpenAI-compatible multimodal server for google/gemma-4-12B-it (text + image + audio).

Serves /v1/chat/completions accepting OpenAI-style multimodal content:
  - {"type": "text", "text": ...}
  - {"type": "image_url", "image_url": {"url": "data:image/...;base64,..." | "http(s)://..."}}
  - {"type": "input_audio", "input_audio": {"data": "<base64>", "format": "wav|mp3|flac"}}

Runs gemma4_unified via transformers (git-main). vLLM can't load this arch yet.

Env:
  MODEL_PATH     weights dir (default /mnt/models)   -- KServe mounts here
  QUANT          4bit | 8bit | none                  (default 4bit)
  MAX_MODEL_LEN  max context tokens                  (default 262144)
  KV_CACHE       quantized | dynamic                 (default quantized -> int4 KV via quanto)
  HOST, PORT
"""
import os, io, csv, time, uuid, base64, logging
from typing import List, Optional, Union, Dict, Any

import torch
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("gemma4-mm")

MODEL_PATH    = os.environ.get("MODEL_PATH", "/mnt/models")
QUANT         = os.environ.get("QUANT", "4bit").lower()
MAX_MODEL_LEN = int(os.environ.get("MAX_MODEL_LEN", "262144"))
KV_CACHE      = os.environ.get("KV_CACHE", "quantized").lower()
HOST          = os.environ.get("HOST", "0.0.0.0")
PORT          = int(os.environ.get("PORT", "8080"))
SERVED_NAME   = os.environ.get("SERVED_MODEL_NAME", "gemma-4-12b")

app = FastAPI(title="gemma-4-12b multimodal")
STATE: Dict[str, Any] = {}


# --------------------------------------------------------------------------- load
def load_model():
    from transformers import AutoModelForMultimodalLM, AutoProcessor, BitsAndBytesConfig

    log.info("loading processor from %s", MODEL_PATH)
    proc = AutoProcessor.from_pretrained(MODEL_PATH)

    kwargs: Dict[str, Any] = {"device_map": "cuda"}
    if QUANT == "4bit":
        kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True,
        )
    elif QUANT == "8bit":
        kwargs["quantization_config"] = BitsAndBytesConfig(load_in_8bit=True)
    else:
        kwargs["dtype"] = torch.bfloat16

    log.info("loading model quant=%s", QUANT)
    t0 = time.time()
    model = AutoModelForMultimodalLM.from_pretrained(MODEL_PATH, **kwargs)
    model.eval()

    # The processor emits fp32 pixel/audio features, but the vision/audio norms are
    # bf16 -> cast all float inputs to this dtype before generate (else it crashes).
    vdt = model.model.embed_vision.patch_ln1.weight.dtype
    log.info("model loaded in %.1fs, VRAM=%.1fGB, feature dtype=%s",
             time.time() - t0, torch.cuda.memory_allocated() / 1e9, vdt)

    STATE.update(model=model, proc=proc, vdt=vdt)


def gen_config():
    """Generation kwargs incl. optional quantized KV cache for max context."""
    cfg: Dict[str, Any] = {}
    if KV_CACHE == "quantized":
        # int4 KV via quanto -> halves/quarters KV cache so full 256k fits at 4-bit weights
        cfg["cache_implementation"] = "quantized"
        cfg["cache_config"] = {"backend": "quanto", "nbits": 4}
    return cfg


# --------------------------------------------------------------------------- OpenAI schema
class ChatMessage(BaseModel):
    role: str
    content: Union[str, List[Dict[str, Any]]]

class ChatRequest(BaseModel):
    model: Optional[str] = SERVED_NAME
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.95
    stream: Optional[bool] = False


# --------------------------------------------------------------------------- content mapping
def _decode_image(url: str):
    from PIL import Image
    if url.startswith("data:"):
        b64 = url.split(",", 1)[1]
        return Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")
    if url.startswith(("http://", "https://")):
        import urllib.request
        with urllib.request.urlopen(url, timeout=20) as r:
            return Image.open(io.BytesIO(r.read())).convert("RGB")
    return Image.open(url).convert("RGB")  # local path


def _decode_audio(item: Dict[str, Any]):
    import soundfile as sf, librosa
    data = item.get("data") or item.get("audio")
    if isinstance(data, str) and data.startswith(("http://", "https://")):
        import urllib.request
        with urllib.request.urlopen(data, timeout=30) as r:
            raw = r.read()
    elif isinstance(data, str) and not data.startswith("/"):
        raw = base64.b64decode(data)          # base64 payload
    else:
        raw = open(data, "rb").read()         # local path
    wav, sr = sf.read(io.BytesIO(raw), dtype="float32")
    if wav.ndim > 1:
        wav = wav.mean(axis=1)                # mono
    if sr != 16000:
        wav = librosa.resample(wav, orig_sr=sr, target_sr=16000)
    return wav


def to_processor_messages(messages: List[ChatMessage]) -> List[Dict[str, Any]]:
    """Map OpenAI content -> gemma4 processor content."""
    out = []
    for m in messages:
        if isinstance(m.content, str):
            out.append({"role": m.role, "content": [{"type": "text", "text": m.content}]})
            continue
        parts = []
        for c in m.content:
            t = c.get("type")
            if t == "text":
                parts.append({"type": "text", "text": c.get("text", "")})
            elif t in ("image_url", "image"):
                url = c["image_url"]["url"] if t == "image_url" else c.get("image")
                parts.append({"type": "image", "image": _decode_image(url)})
            elif t in ("input_audio", "audio"):
                payload = c.get("input_audio", c)
                parts.append({"type": "audio", "audio": _decode_audio(payload)})
        out.append({"role": m.role, "content": parts})
    return out


# --------------------------------------------------------------------------- endpoints
@app.get("/health")
def health():
    return {"status": "ok" if "model" in STATE else "loading"}


@app.get("/v1/models")
def models():
    return {"object": "list", "data": [{"id": SERVED_NAME, "object": "model", "owned_by": "local"}]}


@app.post("/v1/chat/completions")
def chat(req: ChatRequest):
    if "model" not in STATE:
        raise HTTPException(503, "model still loading")
    model, proc, vdt = STATE["model"], STATE["proc"], STATE["vdt"]
    try:
        conv = to_processor_messages(req.messages)
        inputs = proc.apply_chat_template(
            conv, add_generation_prompt=True, tokenize=True,
            return_dict=True, return_tensors="pt",
        ).to(model.device)
        for k, v in list(inputs.items()):                     # dtype fix
            if torch.is_tensor(v) and torch.is_floating_point(v):
                inputs[k] = v.to(vdt)
        n_prompt = inputs["input_ids"].shape[1]
        do_sample = (req.temperature or 0) > 0
        with torch.inference_mode():
            out = model.generate(
                **inputs, max_new_tokens=req.max_tokens,
                do_sample=do_sample, temperature=req.temperature, top_p=req.top_p,
                **gen_config(),
            )
        text = proc.decode(out[0][n_prompt:], skip_special_tokens=True).strip()
        n_out = out.shape[1] - n_prompt
    except Exception as e:
        log.exception("generation failed")
        raise HTTPException(500, f"{type(e).__name__}: {e}")

    return {
        "id": "chatcmpl-" + uuid.uuid4().hex[:24],
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model or SERVED_NAME,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": text},
                     "finish_reason": "stop"}],
        "usage": {"prompt_tokens": n_prompt, "completion_tokens": n_out,
                  "total_tokens": n_prompt + n_out},
    }


if __name__ == "__main__":
    load_model()
    log.info("serving on %s:%d  quant=%s kv=%s max_len=%d", HOST, PORT, QUANT, KV_CACHE, MAX_MODEL_LEN)
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
