FROM python:3.10-slim

WORKDIR /app

# Minimal build tooling
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Optimize size: pull lightweight CPU PyTorch wheel (~180MB) instead of full CUDA stack (~4GB)
RUN pip install --no-cache-dir torch==2.4.1 --extra-index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Pre-fetch model weights into the image layer during build
ENV TRANSFORMERS_CACHE=/app/model_cache
ENV MODEL_NAME=Helsinki-NLP/opus-mt-en-de
RUN python3 -c "from transformers import pipeline; pipeline('translation', model='Helsinki-NLP/opus-mt-en-de')"

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
