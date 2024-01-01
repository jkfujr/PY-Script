import requests
import qrcode
import re
import time

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69'

def get_login_key_and_login_url():
    url = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    data = response.json()
    login_key = data['data']['qrcode_key']
    login_url = data['data']['url']
    return login_key, login_url

def verify_login(login_key):
    while True:
        url = 'https://passport.bilibili.com/x/passport-login/web/qrcode/poll'
        headers = {'User-Agent': user_agent}
        params = {'qrcode_key': login_key}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if data['data']['url']:
            cookie = {item.split("=")[0]: item.split("=")[1] for item in response.headers['Set-Cookie'].split(';')}
            live_buvid = get_live_buvid()
            cookie['LIVE_BUVID'] = live_buvid
            cookie_content = ";".join([f"{key}={value}" for key, value in cookie.items()])
            with open('cookie.txt', 'w') as f:
                f.write(cookie_content)
            print("扫码成功，cookie如下，已自动保存在当前目录下 cookie.txt 文件:")
            print(cookie_content)
            break
        time.sleep(3)

def get_live_buvid():
    url = 'https://api.live.bilibili.com/gift/v3/live/gift_config'
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    set_cookie = response.headers['Set-Cookie']
    pattern = r'LIVE_BUVID=(AUTO[0-9]+)'
    live_buvid = re.search(pattern, set_cookie).group(1)
    return live_buvid

def is_login():
    url = 'https://api.bilibili.com/x/web-interface/nav'
    try:
        with open('cookie.txt', 'r') as f:
            cookie_str = f.read()
    except FileNotFoundError:
        return False, None, None, None

    pattern = r'bili_jct=([0-9a-zA-Z]+);'
    csrf = re.search(pattern, cookie_str).group(1)
    headers = {'User-Agent': user_agent, 'Cookie': cookie_str}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['code'] == 0, data, cookie_str, csrf

def login():
    while True:
        is_logged_in, data, cookie_str, csrf = is_login()
        if is_logged_in:
            uname = data['data']['uname']
            print(f"{uname}已登录")
            return cookie_str, csrf
        print("未登录，或cookie已过期，请扫码登录")
        input("请最大化窗口，以确保二维码完整显示，回车继续")
        login_key, login_url = get_login_key_and_login_url()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=4,
        )
        qr.add_data(login_url)
        qr.make(fit=True)
        qr_data = qr.get_matrix()
        for r in qr_data:
            print("".join(["██" if b else "  " for b in r]))
        print("若依然无法扫描，请将以下链接复制到B站打开并确认(任意私信一个人,最好是B站官号，发送链接即可打开)")
        print(login_url)
        verify_login(login_key)

if __name__ == '__main__':
    login()
