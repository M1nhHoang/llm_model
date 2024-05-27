import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, Response, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from typing import List

from service import send_messages

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    with open("static/index.html", encoding="utf-8") as f:
        html_content = f.read()

    return HTMLResponse(content=html_content, status_code=200)


@app.get("/static/{file_type}/{file_name}")
async def get_file(file_type: str, file_name: str):
    file_path = f"static/{file_type}/{file_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return Response(status_code=404)


@app.post("/chat/")
async def chat(messages: List[dict] = []):
    if not messages:
        return {"error": "messages is required"}

    return StreamingResponse(send_messages(messages), media_type="text/event-stream")
