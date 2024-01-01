import os
import subprocess
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import asyncio

app = FastAPI()

# 录播文件夹
liverec_dir = "\AA"

# 需要移动到的目录
newfile_dir = "\BB"


# 异步队列，用于记录待上传文件的数量
upload_queue = asyncio.Queue()

async def move_file(file_path, destination_folder):
    try:
        subprocess.run(["rclone", "move", file_path, destination_folder])
        print(f"[Info] 文件成功移动 {file_path} -> {destination_folder}")

        # 上传完成后打印队列数量
        print(f"[Info] 当前文件待上传队列数量: {upload_queue.qsize()}")

    except subprocess.CalledProcessError as e:
        error_msg = f"[Error] 无法移动文件，错误信息：{str(e)}"
        print(error_msg)

async def handle_event(event_data):
    event_type = event_data["EventType"]
    relative_path = event_data["EventData"].get("RelativePath")

    if event_type == "FileClosed" and relative_path:
        room_id = event_data["EventData"]["RoomId"]
        room_name = event_data["EventData"]["Name"]
        print(f"[Info] [录播姬] [{room_id}] {room_name} 文件关闭")
        print(f"[Info] [脚本] [{room_id}] {room_name} 执行移动操作")

        parent_folder = os.path.dirname(relative_path)
        newfile_parent_folder = os.path.join(newfile_dir, parent_folder)
        if not os.path.exists(newfile_parent_folder):
            try:
                os.makedirs(newfile_parent_folder)
            except OSError as e:
                error_msg = f"[Error] 无法创建目录 {newfile_parent_folder}，错误信息：{str(e)}"
                print(error_msg)
                return

        file_path = os.path.join(liverec_dir, relative_path)

        if os.path.isfile(file_path):
            # 添加视频文件到异步队列
            await upload_queue.put(move_file(file_path, newfile_parent_folder))

            # 构造弹幕文件和封面文件的路径
            base_filename, _ = os.path.splitext(relative_path)
            xml_file_path = os.path.join(liverec_dir, f"{base_filename}.xml")
            jpg_file_path = os.path.join(liverec_dir, f"{base_filename}.cover.jpg")

            # 添加弹幕文件到异步队列
            if os.path.isfile(xml_file_path):
                await upload_queue.put(move_file(xml_file_path, newfile_parent_folder))

            # 添加封面文件到异步队列
            if os.path.isfile(jpg_file_path):
                await upload_queue.put(move_file(jpg_file_path, newfile_parent_folder))
        else:
            print(f"[Error] 文件 {file_path} 不存在")



    # 其他事件类型
    elif event_type == "SessionStarted":
        room_id = event_data["EventData"]["RoomId"]
        room_name = event_data["EventData"]["Name"]
        print(f"[Info] [录播姬] [{room_id}] {room_name} 录制开始")
    elif event_type == "FileOpening":
        room_id = event_data["EventData"]["RoomId"]
        room_name = event_data["EventData"]["Name"]
        print(f"[Info] [录播姬] [{room_id}] {room_name} 文件打开")
    elif event_type == "SessionEnded":
        room_id = event_data["EventData"]["RoomId"]
        room_name = event_data["EventData"]["Name"]
        print(f"[Info] [录播姬] [{room_id}] {room_name} 录制结束")
    elif event_type == "StreamStarted":
        room_id = event_data["EventData"]["RoomId"]
        room_name = event_data["EventData"]["Name"]
        print(f"[Info] [录播姬] [{room_id}] {room_name} 直播开始")
    elif event_type == "StreamEnded":
        room_id = event_data["EventData"]["RoomId"]
        room_name = event_data["EventData"]["Name"]
        print(f"[Info] [录播姬] [{room_id}] {room_name} 直播结束")


# 接收POST请求
# http://IP:5000/
@app.post("/")
async def webhook(request: Request):
    content = await request.json()

    # 直接调用异步函数
    await handle_event(content)

    return PlainTextResponse("事件处理完成", status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, access_log=False)