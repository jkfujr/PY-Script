import os
import shutil
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

# 获取脚本执行目录
script_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(script_dir, 'log')

# 创建 log 文件夹
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 创建一个按天分割的日志记录器
log_filename = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")
handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=30, encoding="utf-8")
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# 录播文件夹
liverec_dir = r"F:\录播"
liverec_dir = liverec_dir.rstrip("\\") + "\\"

# 需要移动到的目录
newfile_dir = r"F:\AA"

def handle_event(event_data):
    event_type = event_data["EventType"]
    relative_path = event_data["EventData"].get("RelativePath")

    if event_type == "FileClosed" and relative_path:
        room_id = event_data["EventData"]["RoomId"]
        room_name = event_data["EventData"]["Name"]
        log_message = f"[Info] [录播姬] [{room_id}] {room_name} 文件关闭"
        logger.info(log_message)
        log_message = f"[Info] [脚本] [{room_id}] {room_name} 执行移动操作"
        logger.info(log_message)

        parent_folder = os.path.dirname(relative_path)
        newfile_parent_folder = os.path.join(newfile_dir, parent_folder)
        if not os.path.exists(newfile_parent_folder):
            try:
                os.makedirs(newfile_parent_folder)
            except OSError as e:
                error_msg = f"[Error] [脚本] 无法创建目录 {newfile_parent_folder}，错误信息：{str(e)}"
                logger.error(error_msg)
                return

        file_path = os.path.join(liverec_dir, relative_path)

        if os.path.isfile(file_path):
            try:
                shutil.move(file_path, newfile_parent_folder)
                log_message = f"[Info] [脚本] [{room_id}] {room_name} 成功移动视频文件 {file_path} -> {newfile_parent_folder}"
                logger.info(log_message)

                base_filename, _ = os.path.splitext(relative_path)
                xml_file_path = os.path.join(liverec_dir, f"{base_filename}.xml")
                jpg_file_path = os.path.join(liverec_dir, f"{base_filename}.cover.jpg")

                if os.path.isfile(xml_file_path):
                    shutil.move(xml_file_path, newfile_parent_folder)
                    log_message = f"[Info] [脚本] [{room_id}] {room_name} 成功移动弹幕文件 {xml_file_path} -> {newfile_parent_folder}"
                    logger.info(log_message)

                if os.path.isfile(jpg_file_path):
                    shutil.move(jpg_file_path, newfile_parent_folder)
                    log_message = f"[Info] [脚本] [{room_id}] {room_name} 成功移动封面文件 {jpg_file_path} -> {newfile_parent_folder}"
                    logger.info(log_message)

            except OSError as e:
                error_msg = f"[Error] [脚本] 无法移动文件，错误信息：{str(e)}"
                logger.error(error_msg)
        else:
            log_message = f"[Error] [脚本] 文件 {file_path} 不存在"
            logger.error(log_message)

    # 其他事件类型
    elif event_type == "SessionStarted":
        room_id = event_data["EventData"]["RoomId"]
        room_name = event_data["EventData"]["Name"]
        log_message = f"[Info] [录播姬] [{room_id}] {room_name} 录制开始"
        logger.info(log_message)
    elif event_type == "FileOpening":
        room_id = event_data["EventData"]["RoomId"]
        room_name = event_data["EventData"]["Name"]
        log_message = f"[Info] [录播姬] [{room_id}] {room_name} 文件打开"
        logger.info(log_message)
    elif event_type == "SessionEnded":
        room_id = event_data["EventData"]["RoomId"]
        room_name = event_data["EventData"]["Name"]
        log_message = f"[Info] [录播姬] [{room_id}] {room_name} 录制结束"
        logger.info(log_message)
    elif event_type == "StreamStarted":
        room_id = event_data["EventData"]["RoomId"]
        room_name = event_data["EventData"]["Name"]
        log_message = f"[Info] [录播姬] [{room_id}] {room_name} 直播开始"
        logger.info(log_message)
    elif event_type == "StreamEnded":
        room_id = event_data["EventData"]["RoomId"]
        room_name = event_data["EventData"]["Name"]
        log_message = f"[Info] [录播姬] [{room_id}] {room_name} 直播结束"
        logger.info(log_message)

# 接收POST请求
# http://IP:5000/
@app.post("/")
async def webhook(request: Request):
    content = await request.json()

    handle_event(content)

    return "事件处理完成"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, access_log=False)
