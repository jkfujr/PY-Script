import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import asyncio

app = FastAPI()

# 将HTML文件放置在一个名为"static"的目录下，并使用StaticFiles来提供服务
app.mount("/", StaticFiles(directory="static", html=True), name="static")

async def run_cmd(websocket: WebSocket, cmd_input: str):
    process = await asyncio.create_subprocess_exec(
        r"C:\jkfujr\Tools\BBDown\BBD.exe", cmd_input, 
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    while True:
        line = await process.stdout.readline()
        if line:
            await websocket.send_json({
                "progress": "正在下载...",
                "log": line.decode().strip()
            })
        else:
            break

    await websocket.send_json({
        "progress": "下载完成",
        "log": ""
    })

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            cmd_input = data['cmd']
            await run_cmd(websocket, cmd_input)
    except Exception as e:
        await websocket.send_json({
            "progress": "发生错误",
            "log": str(e)
        })
    finally:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=45678)