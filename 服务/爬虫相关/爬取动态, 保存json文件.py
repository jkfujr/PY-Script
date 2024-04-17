import requests
import json
import os
from datetime import datetime
import time
import random

# 用户UID
UID = "401480763"

# 路径
DIR = "C:\\jkfujr\\Desktop\\AA\\"

# Cookie的SESSDATA字段，填你自己的
SESSDATA = "114514"

def save_json(data, index, offset=None):
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    
    # 当前时间
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 构造文件名
    if index == 1:
        file_name = f"{DIR}[{now}]_{index}.json"
    elif offset:
        file_name = f"{DIR}[{now}]_{index}_{offset}.json"
    else:
        file_name = f"{DIR}[{now}]_{index}.json"
    
    # 保存文件
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"已保存文件: {file_name}")

def fetch_data(UID):
    index = 1
    url = f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid={UID}'
    print("开始获取第一页数据...")
    
    while True:
        print(f"正在请求 URL: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'cookie': f'SESSDATA={SESSDATA}'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("成功获取数据...")
            if 'code' in data and data['code'] == -352:
                print("叔叔风控，暂停30秒后重试...")
                time.sleep(30)
                continue
            offset = data['data'].get('offset', None)
            save_json(data, index, offset)
            index += 1
            
            # 没有下一页就退出循环
            if not offset:
                print("已到达最后一页，退出循环...")
                break

            # 下一页的请求链接
            url = f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid={UID}&offset={offset}'
            
            # 随机1到3秒请求
            sleep_time = random.uniform(1, 3)
            print(f"随机 {sleep_time:.2f} 秒...")
            time.sleep(sleep_time)
        else:
            print(f'请求失败: {response.status_code}')
            break

fetch_data(UID)