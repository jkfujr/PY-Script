import os
import asyncio
import yaml
import time
import requests
import threading
import urllib3
from gotify import push_gotify
from datetime import datetime
from core.BilibiliCookieMgmt import BilibiliCookieManager

# 禁用不安全请求的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BaseChecking:
    def __init__(self, config_path, service_key):
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        # 全局配置
        global_gotify_url = config['CONFIG']['PUSH']['GOTIFY'].get('GOTIFY_URL')
        global_gotify_token = config['CONFIG']['PUSH']['GOTIFY'].get('GOTIFY_TOKEN')
        global_push_enabled = config['CONFIG']['PUSH'].get('ENABLE', False)
        
        # 初始化cookie管理器
        self.cookie_manager = BilibiliCookieManager()
        
        # 服务配置（FOLLOW_CHECKING 或 ROOMID_CHECKING）
        server_config = config.get(service_key, {})

        # 使用 SERVER_xxx_CHECKING 里面的配置，如果没有则使用全局配置
        self.gotify_url = global_gotify_url
        self.gotify_token = server_config.get('PUSH', {}).get('GOTIFY', {}).get('GOTIFY_TOKEN', global_gotify_token)
        self.push_enabled = server_config.get('PUSH', {}).get('ENABLE', global_push_enabled)

    def get_bilibili_cookie(self):
        """获取新的B站cookie"""
        cookie = self.cookie_manager.get_cookie()
        if not cookie:
            print("[警告] 无法获取有效的B站cookie")
        return cookie

    async def send_gotify_notification(self, title, message, priority=5):
        if self.push_enabled and self.gotify_url and self.gotify_token:
            await push_gotify(self.gotify_url, self.gotify_token, title, message, priority)

class FOLLOW_CHECKING(BaseChecking):
    def __init__(self, config_path):
        super().__init__(config_path, 'SERVER_FOLLOW_CHECKING')
        self.data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
        self.file_path = os.path.join(self.data_dir, "follow_checking.txt")
        # 确保数据目录存在
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        # 其他初始化内容
        self.user_config = yaml.safe_load(open(config_path, "r", encoding="utf-8")).get('SERVER_FOLLOW_CHECKING', {}).get('USER', {})

    def ensure_file_has_header(self):
        """确保follow_checking.txt文件有表头"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                first_line = file.readline().strip()
                if first_line != "时间,UID,用户名,关注者UID,关注者用户名":
                    raise FileNotFoundError
        except FileNotFoundError:
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write("时间,UID,用户名,关注者UID,关注者用户名\n")

    async def fetch_and_update_followers(self, name, vmid):
        """从B站API获取关注者列表并更新follow_checking.txt"""
        url = "https://api.bilibili.com/x/relation/followings"
        params = {
            "vmid": vmid,
            "pn": 1,
            "ps": 20,
            "order": "desc"
        }

        # 每次请求前获取新cookie
        cookie = self.get_bilibili_cookie()
        if not cookie:
            return None

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Cookie": cookie
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # 如果状态码不是200，抛出HTTPError
            data = response.json()

            if data['code'] == 0:
                followers = data['data']['list']
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_followers = []

                # 读取现有 follow_checking.txt 中的关注者UID
                try:
                    with open(self.file_path, "r", encoding="utf-8") as follow_file:
                        existing_followers = {line.split(',')[3] for line in follow_file.readlines()[1:]}
                except FileNotFoundError:
                    existing_followers = set()

                with open(self.file_path, "a", encoding="utf-8") as follow_file:
                    for follower in followers:
                        mid = str(follower['mid'])
                        uname = follower['uname']
                        if mid not in existing_followers:
                            follow_file.write(f"{current_time},{vmid},{name},{mid},{uname}\n")
                            new_followers.append((mid, uname, current_time))

                return new_followers
            else:
                print(f"[新关注检查] API返回错误: {data.get('message', '未知错误')}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"[新关注检查] 网络请求失败: {str(e)}")
            return None
        except ValueError:
            print(f"[新关注检查] 解析响应失败")
            return None

    async def main_loop(self):
        """主循环，用于定期检查新关注者"""
        self.ensure_file_has_header()
        while True:
            all_new_followers = []

            for name, vmid in self.user_config.items():
                new_followers = await self.fetch_and_update_followers(name, vmid)
                if new_followers:
                    for mid, uname, current_time in new_followers:
                        message = f"{name}[{vmid}] 新关注\nUID: {mid}\n用户名: {uname}\n时间: {current_time}\n\n"
                        all_new_followers.append(message)

            if all_new_followers:
                for message in all_new_followers:
                    print(message)
                    await self.send_gotify_notification(f"[新关注检查] 有新关注", message, priority=5)

            else:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[新关注检查] 暂无新关注 | {current_time}")

            await asyncio.sleep(3600)

class ROOMID_CHECKING(BaseChecking):
    def __init__(self, config_path):
        super().__init__(config_path, 'SERVER_ROOMID_CHECKING')
        self.data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
        self.uid_file_path = os.path.join(self.data_dir, "roomid_checking.conf")
        # 确保数据目录存在
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # 读取多个 API 配置
        server_config = yaml.safe_load(open(config_path, "r", encoding="utf-8")).get('SERVER_ROOMID_CHECKING', {})
        self.api_urls = list(server_config.get('RECHEMEAPI', {}).values())

    def read_uid_file(self):
        with open(self.uid_file_path, "r") as uid_file:
            return [line.strip() for line in uid_file]

    def remove_uid_from_file(self, uid_to_remove):
        """从 roomid_checking.conf 中移除指定的 UID"""
        with open(self.uid_file_path, "r") as uid_file:
            lines = uid_file.readlines()

        with open(self.uid_file_path, "w") as uid_file:
            for line in lines:
                if line.strip() != uid_to_remove:
                    uid_file.write(line)

    def check_room_id_exists(self, room_id):
        """调用多个API检查 room_id 是否存在"""
        if not self.api_urls:
            print("[直播间检查] 未配置任何录播姬API，跳过检查。")
            return False

        for api_url in self.api_urls:
            try:
                response = requests.get(api_url, verify=False)
                response.raise_for_status()
                data = response.json().get("data", [])
                for item in data:
                    if item.get("roomId") == room_id:
                        return True
            except requests.exceptions.RequestException as e:
                print(f"[直播间检查] API请求失败: {str(e)}")
                continue

        return False

    async def check_room_status(self):
        uids = self.read_uid_file()

        while True:
            current_time = datetime.now()
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

            new_uids = self.read_uid_file()
            if new_uids != uids:
                print("[直播间检查] UID列表已更新, 重新加载UID列表")
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
                        print(f"[直播间检查] 暂无直播间信息 | {current_time_str}")
                    else:
                        for uid, room_info in data.items():
                            room_id = room_info.get("room_id", "N/A")
                            uname = room_info.get("uname", "N/A")
                            title = room_info.get("title", "N/A")

                            if self.check_room_id_exists(room_id):
                                print(f"[直播间检查] 直播间 {room_id} 已存在于 API 数据中，移除对应 UID: {uid}")
                                self.remove_uid_from_file(uid)
                            else:
                                message = (
                                    f"UID: {uid}\n名称: {uname}\n直播间ID: {room_id}\n"
                                    f"直播间标题: {title}\n时间: {current_time_str}"
                                )
                                print(f"[直播间检查] 已发现直播间 {message}")
                                await self.send_gotify_notification("[直播间检查] 已发现直播间", message, priority=7)

                else:
                    print(f"[直播间检查] 请求失败，状态码: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"[直播间检查] 网络错误: {str(e)}")

            time.sleep(3600)

def run_follow_checking():
    follow_checker = FOLLOW_CHECKING("config.yaml")
    asyncio.run(follow_checker.main_loop())

def run_roomid_checking():
    room_checker = ROOMID_CHECKING("config.yaml")
    asyncio.run(room_checker.check_room_status())

if __name__ == "__main__":
    follow_thread = threading.Thread(target=run_follow_checking)
    roomid_thread = threading.Thread(target=run_roomid_checking)
    # 启动线程
    follow_thread.start()
    roomid_thread.start()
    # 等待线程完成
    follow_thread.join()
    roomid_thread.join()
