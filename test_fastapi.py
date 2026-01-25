# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
STATIC_DIR = Path("static")
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# 数据模型
class RequestItem(BaseModel):
    url: str
    request_data: str
    picture_filepath: str


@app.get("/api/requests")
async def get_requests():
    """获取requests_data.json数据"""
    json_path = "requests_data.json"

    # 如果文件不存在，创建示例数据
    if not Path(json_path).exists():
        sample_data = [
            {
                "url": "https://api.example.com/data",
                "request_data": '{"key": "value", "action": "get"}',
                "picture_filepath": "static/sample1.jpg"
            },
            {
                "url": "https://api.example.com/upload",
                "request_data": '{"file": "image.png", "size": 1024}',
                "picture_filepath": "static/sample2.jpg"
            }
        ]
        with open(json_path, 'w') as f:
            json.dump(sample_data, f, indent=2)

    with open(json_path, 'r') as f:
        data = json.load(f)
    return data


@app.get("/api/image/{filepath:path}")
async def get_image(filepath: str):
    """获取图片文件"""
    return FileResponse(filepath)

if __name__ == "__main__" :
  uvicorn.run("test_fastapi:app", host="127.0.0.1", port=8000, log_level="info")