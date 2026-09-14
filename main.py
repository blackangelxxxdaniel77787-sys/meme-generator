from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import urllib.parse
import os

app = FastAPI()

# Отдача index.html
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/generate")
async def generate(topic: str = Form(...), file: UploadFile = File(None)):
    try:
        # Кодируем текст для безопасности URL
        safe_topic = urllib.parse.quote(topic)
        # Ссылка на Pollinations AI с подсказкой для мема
        prompt = f"meme {safe_topic}"
        image_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=800&height=600&nologo=true"
        
        return JSONResponse({"image_url": image_url})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
        
