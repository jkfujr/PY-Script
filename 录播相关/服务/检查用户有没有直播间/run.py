import requests
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import time
import os

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 创建日志文件夹（如果不存在）
log_folder = os.path.join(script_dir, "logs")
os.makedirs(log_folder, exist_ok=True)

# 配置日志
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)
log_handler = TimedRotatingFileHandler(
    os.path.join(log_folder, "app.log"),
    when="midnight",  # 每天午夜分割
    interval=1,  # 分割频率（每天）
    backupCount=5,
    encoding="utf-8",
    atTime=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
)
log_handler.suffix = "%Y-%m-%d.log"  # 自定义日志文件名后缀
log_handler.setFormatter(logging.Formatter(log_format))
logger = logging.getLogger()
logger.addHandler(log_handler)

def read_uid_file():
    uid_file_path = os.path.join(script_dir, "uid.conf")
    with open(uid_file_path, "r") as uid_file:
        return [line.strip() for line in uid_file]

uids = read_uid_file()

while True:
    # 获取当前时间
    current_time = datetime.now()
    start_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # 打印脚本开始时间到日志
    logger.info(f"========== {start_time} ==========")
    logger.info("")


    # 检查uid.conf文件是否发生了更改
    new_uids = read_uid_file()
    if new_uids != uids:
        logger.info("uid.conf文件已更新，重新加载UID列表")
        logger.info("")
        uids = new_uids


    url = "http://127.0.0.1:65301/room/v1/Room/get_status_info_by_uids"
    headers = {"Content-Type": "application/json"}
    data = {"uids": uids}  # 使用从uid.conf文件中读取的UID数据

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            data = result.get("data", {})

            if not data:
                logger.info("暂无直播间")
                logger.info("")
            else:
                for uid, room_info in data.items():
                    uname = room_info.get("uname", "N/A")
                    uid = room_info.get("uid", "N/A")
                    room_id = room_info.get("room_id", "N/A")
                    title = room_info.get("title", "N/A")

                    log_uid_message = f"[user] UID: {uid}"
                    log_uname_message = f"[user] 名称: {uname}"
                    log_room_id_message = f"[user] 直播间ID: {room_id}"
                    log_title_message = f"[user] 直播间标题: {title}"

                    logger.info(log_uname_message)
                    logger.info(log_uid_message)
                    logger.info(log_room_id_message)
                    logger.info(log_title_message)
                    logger.info("")

            # 打印脚本结束时间到日志
            logger.info(f"========== END ==========")
            logger.info("")
        else:
            error_message = f"请求失败，状态码: {response.status_code}"
            logger.error(error_message)
    except requests.exceptions.RequestException as e:
        # 捕获网络错误，并打印错误消息
        logger.error(f"网络错误: {str(e)}")

    # 等待一小时
    # 3600秒 = 1小时
    time.sleep(3600)