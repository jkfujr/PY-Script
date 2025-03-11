import requests
from typing import Optional

class BilibiliCookieManager:
    def __init__(self, api_url: str = "http://100.111.0.101:18000/api/cookie/random", 
                 api_token: str = "1145141919810"):
        self.api_url = api_url
        self.headers = {"token": api_token}

    def get_cookie(self) -> Optional[str]:
        """
        从API获取cookie并格式化
        返回格式化的cookie字符串或None(如果请求失败)
        """
        try:
            response = requests.get(self.api_url, headers=self.headers)
            if response.status_code != 200:
                print(f"[Cookie管理] 获取Cookie失败，状态码: {response.status_code}")
                return None

            data = response.json()
            if not data.get("cookie_valid", False):
                print("[Cookie管理] 获取的Cookie无效")
                return None

            # 提取所需的cookie值
            cookies = data.get("cookie_info", {}).get("cookies", [])
            cookie_dict = {
                cookie["name"]: cookie["value"] 
                for cookie in cookies 
                if cookie["name"] in ["DedeUserID", "DedeUserID__ckMd5", "SESSDATA", "bili_jct"]
            }

            # 格式化cookie字符串
            cookie_str = ";".join([f"{k}={v}" for k, v in cookie_dict.items()])
            return cookie_str

        except Exception as e:
            print(f"[Cookie管理] 获取Cookie时发生错误: {str(e)}")
            return None 