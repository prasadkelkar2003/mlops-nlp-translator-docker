import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="DevOps Translation Service")

MODEL_NAME = os.getenv("MODEL_NAME", "Helsinki-NLP/opus-mt-en-de")
translator = None

@app.on_event("startup")
def load_model():
    global translator
    translator = pipeline("translation", model=MODEL_NAME)

class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    source_text: str
    translated_text: str
    model: str

@app.get("/", response_class=HTMLResponse)
def index():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>ML Translation Service</title>
      <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 16px; color: #1f2328; }}
        textarea {{ width: 100%; height: 110px; padding: 10px; box-sizing: border-box; border-radius: 6px; border: 1px solid #d0d7de; font-size: 15px; }}
        button {{ background: #0969da; color: #fff; border: none; padding: 10px 18px; font-weight: 600; border-radius: 6px; cursor: pointer; margin-top: 10px; }}
        button:hover {{ background: #0858b8; }}
        .result {{ margin-top: 20px; padding: 14px; background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 6px; min-height: 40px; font-size: 15px; }}
        .badge {{ display: inline-block; font-size: 12px; background: #eaeef2; padding: 2px 8px; border-radius: 10px; color: #57606a; }}
      </style>
    </head>
    <body>
      <h2>English to German Translator</h2>
      <p>Model: <span class="badge">{MODEL_NAME}</span></p>
      <textarea id="srcText" placeholder="Enter English text to translate..."></textarea><br>
      <button onclick="runTranslation()">Translate</button>
      <h3>Translation:</h3>
      <div id="resultBox" class="result">Waiting for input...</div>

      <script>
        async function runTranslation() {{
          const text = document.getElementById('srcText').value;
          const resBox = document.getElementById('resultBox');
          if (!text.trim()) return;
          resBox.innerText = 'Translating...';
          try {{
            const res = await fetch('/translate', {{
              method: 'POST',
              headers: {{ 'Content-Type': 'application/json' }},
              body: JSON.stringify({{ text }})
            }});
            const data = await res.json();
            resBox.innerText = data.translated_text || JSON.stringify(data);
          }} catch (err) {{
            resBox.innerText = 'Error: ' + err;
          }}
        }}
      </script>
    </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "healthy", "model": MODEL_NAME}

@app.post("/translate", response_model=TranslationResponse)
def translate(req: TranslationRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")
    result = translator(req.text)
    return TranslationResponse(
        source_text=req.text,
        translated_text=result[0]["translation_text"],
        model=MODEL_NAME
    )
