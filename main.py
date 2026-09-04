import os
import io
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw, ImageFont
import requests

app = FastAPI()

# Разрешаем запросы из WebApp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Отдаем наш фронтенд (index.html)
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# 2. Генерация мема с водяным знаком
@app.get("/generate")
async def generate(text: str):
    # Берем базовый фоновый шаблон мема (или создаем новый)
    img_url = f"https://pollinations.ai/p/{requests.utils.quote(text)}?width=600&height=400&seed=42"
    resp = requests.get(img_url)
    img = Image.open(io.BytesIO(resp.content)).convert("RGB")

    # Добавляем водяной знак в угол
    draw = ImageDraw.Draw(img)
    watermark = "Made in @YourMemeBot"
    
    # Рисуем подложку и текст водяного знака
    draw.rectangle([(10, 360), (220, 390)], fill=(0, 0, 0, 180))
    draw.text((15, 365), watermark, fill=(255, 255, 255))

    # Возвращаем готовый JPEG
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    return StreamingResponse(img_byte_arr, media_type="image/jpeg")
