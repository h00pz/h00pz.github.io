# Multimodal gemma-4-12b serving image (text + vision + audio)
# vLLM can't load gemma4_unified (arch newer than its transformers 4.57); this uses
# transformers git-main (5.16.dev), proven working in-cluster on an RTX 3090.
#
# Base = the RHOAI vLLM CUDA image ONLY for its known-good torch 2.10 + CUDA stack.
# We do NOT use vLLM here; the transformers upgrade will print a dependency-conflict
# warning against the base's pinned transformers 4.57 — that is expected and benign.
FROM registry.redhat.io/rhaii/vllm-cuda-rhel9@sha256:ad06abf3bb5235ebb5b2df84cd1b9fd09e823f0ff2eebfc82bb4590275ccfe0b

USER 0
WORKDIR /app

# transformers must come from git main (PyPI tops out at 5.5.4, which lacks gemma4_unified).
# tokenizers>=0.23.1 is only on public PyPI (the RHOAI mirror caps at 0.22.2), so pin the
# index to pypi.org for this layer. PIN the transformers commit for reproducible builds.
ARG TRANSFORMERS_REF=main
RUN pip install --no-cache-dir --index-url https://pypi.org/simple/ \
      "git+https://github.com/huggingface/transformers.git@${TRANSFORMERS_REF}" \
      "tokenizers>=0.23.1,<0.24" \
      "bitsandbytes==0.49.2" \
      "torchvision==0.25.0" \
      "accelerate==1.13.0" \
      "librosa==0.11.0" \
      soundfile pillow numpy \
      "optimum-quanto" \
      "fastapi==0.115.*" "uvicorn[standard]==0.34.*" "pydantic==2.*"

COPY serve.py /app/serve.py

# KServe's storage-initializer mounts the model at /mnt/models
ENV MODEL_PATH=/mnt/models \
    QUANT=4bit \
    MAX_MODEL_LEN=262144 \
    KV_CACHE=dynamic \
    HOST=0.0.0.0 \
    PORT=8080 \
    HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1

EXPOSE 8080
USER 1001
ENTRYPOINT ["python3", "/app/serve.py"]
