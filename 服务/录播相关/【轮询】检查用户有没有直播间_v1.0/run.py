import os
import time
import requests
import logging
import urllib3
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

# 禁用不安全请求的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
    when="midnight",
    interval=1,
    backupCount=5,
    encoding="utf-8",
    atTime=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
)
log_handler.suffix = "%Y-%m-%d.log"
log_handler.setFormatter(logging.Formatter(log_format))
logger = logging.getLogger()
logger.addHandler(log_handler)


def read_uid_file():
    uid_file_path = os.path.join(script_dir, "uid.conf")
    with open(uid_file_path, "r") as uid_file:
        return [line.strip() for line in uid_file]


uids = read_uid_file()

# Gotify URL&TOken
message_url = "https://100.111.200.21:18101/message?token=114514"


# 消息发送
def send_message(payload):
    try:
        response = requests.post(message_url, json=payload, verify=False)
        if response.status_code == 200:
            logger.info("[Gotify] 消息发送成功")
            return True
        else:
            logger.error(f"[Gotify] 消息发送失败，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"[Gotify] 消息发送失败，网络错误: {str(e)}")
        return False


# 重试函数
def retry_request(url, payload, max_retries=3, delay=10):
    retries = 0
    while retries < max_retries:
        if send_message(payload):
            return True
        else:
            retries += 1
            logger.info(f"[Gotify] 重试第 {retries} 次")
            time.sleep(delay)
    logger.error("[Gotify] 重试失败，放弃请求")
    return False


while True:
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

    new_uids = read_uid_file()
    if new_uids != uids:
        logger.info("[脚本] UID列表已更新, 重新加载UID列表")
        uids = new_uids

    url = "http://127.0.0.1:65301/room/v1/Room/get_status_info_by_uids"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0"
    }
    data = {"uids": uids}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            data = result.get("data", {})

            if not data:
                logger.info(f"[脚本] 暂无直播间信息 | 时间: {current_time_str}")

                payload = {
                    "message": f"暂无直播间信息\n时间: {current_time_str}",
                    "priority": 1,
                    "title": "[检查直播间信息] 暂无直播间信息",
                }
                retry_request(message_url, payload)

            else:
                for uid, room_info in data.items():
                    uname = room_info.get("uname", "N/A")
                    uid = room_info.get("uid", "N/A")
                    room_id = room_info.get("room_id", "N/A")
                    title = room_info.get("title", "N/A")

                    logger.info(
                        f"[脚本] [已发现直播间] UID: {uid} | 名称: {uname} | 直播间ID: {room_id} | 直播间标题: {title} | 时间: {current_time_str}"
                    )

                    payload = {
                        "message": f"UID: {uid}\n名称: {uname}\n直播间ID: {room_id}\n直播间标题: {title}\n时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}",
                        "priority": 7,
                        "title": f"[检查直播间信息] 已发现直播间",
                    }
                    retry_request(message_url, payload)

        else:
            error_message = f"[脚本] 请求失败，状态码: {response.status_code}"
            logger.error(error_message)
    except requests.exceptions.RequestException as e:
        logger.error(f"[脚本] 网络错误: {str(e)}")

    # 等待一小时
    # 3600秒 = 1小时
    time.sleep(3600)