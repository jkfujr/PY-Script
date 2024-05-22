import os
import time
import shutil
import requests
import subprocess
import schedule
from datetime import datetime

# 优化脚本路径，使用当前脚本所在目录
script_path = os.path.join(os.path.dirname(__file__), 'optimize.py')

# 文件夹路径配置
folder_path_id = {
    "AAA": {"source": r"F:\Video\录播\综合", "target": r"F:\Video\AAAAAAAAAA"},
    "PPP": {"source": r"F:\Video\录播\P家", "target": r"F:\Video\PPPPPPPPPP"},
}

# 打印统计信息的函数
def print_statistics(folder_path_id, total_folders, moved_folders, failed_folders, failed_folder_names):
    for folder_id, paths in folder_path_id.items():
        source_directory = paths["source"]
        target_directory = paths["target"]
        
        processed_folders = total_folders[folder_id] - moved_folders.get(folder_id, 0) - failed_folders.get(folder_id, 0)
        moved_folders_source = moved_folders.get(folder_id, 0)
        failed_folders_source = failed_folders.get(folder_id, 0)
        failed_folder_names_source = failed_folder_names.get(folder_id, [])
        
        print(f"\n[统计] 源路径: {source_directory}")
        print(f"[统计] 处理前: {total_folders[folder_id]}, 处理后: {processed_folders}")
        print(f"[统计] 移动成功: {moved_folders_source}, 移动失败: {failed_folders_source}")
        if failed_folders_source > 0:
            print("移动失败的文件夹:", ", ".join(failed_folder_names_source))
        try:
            target_folders = [folder for folder in os.listdir(target_directory) if os.path.isdir(os.path.join(target_directory, folder))]
            print(f"[统计] 目标路径文件夹: {', '.join(target_folders)}")
        except FileNotFoundError:
            print(f"[统计] 目标路径 {target_directory} 不存在")
    print()

# 请求API获取数据
def fetch_recording_status():
    api_url = "http://127.0.0.1:11111/api/data"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json().get("data", [])
        return {item["name"]: {"recording": item["recording"], "streaming": item["streaming"]} for item in data}
    except requests.exceptions.RequestException as e:
        print("[API] 请求API失败:", e)
        return {}

# 确保目录存在
def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"[目录] 创建目标目录: {directory_path}")
        except Exception as e:
            print(f"[目录] 创建目录 {directory_path} 失败: {e}")

# 移动文件夹操作
def move_folders():
    # 初始化统计信息
    total_folders = {folder_id: 0 for folder_id in folder_path_id.keys()}
    moved_folders = {folder_id: 0 for folder_id in folder_path_id.keys()}
    failed_folders = {folder_id: 0 for folder_id in folder_path_id.keys()}
    failed_folder_names = {folder_id: [] for folder_id in folder_path_id.keys()}

    # 请求API获取录制状态
    recording_status = fetch_recording_status()

    print("\n[移动] 开始移动录播文件")
    for folder_id, paths in folder_path_id.items():
        source_directory = paths["source"]
        target_directory = paths["target"]

        # 确保目标目录存在
        ensure_directory_exists(target_directory)

        # 更新源目录下的文件夹总数
        total_folders[folder_id] = len([item for item in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, item))])
        print(f"\n[移动] 开始处理目标路径 {target_directory}, 总共有 {total_folders[folder_id]} 个文件夹")

        for folder_name in os.listdir(source_directory):
            if not os.path.isdir(os.path.join(source_directory, folder_name)):
                continue  # 确保只处理文件夹

            source_folder_path = os.path.join(source_directory, folder_name)
            target_folder_path = os.path.join(target_directory, folder_name)
            
            print(f"\n[移动] 开始处理用户文件夹 {folder_name}")

            folder_status = recording_status.get(folder_name)
            if folder_status and (folder_status["recording"] or folder_status["streaming"]):
                print(f"[移动] 用户文件夹 {folder_name} 正在直播或者录制中，跳过移动")
                continue

            if not os.path.exists(target_folder_path):
                try:
                    shutil.move(source_folder_path, target_folder_path)
                    print(f"[移动] 已成功移动文件夹 {folder_name} 到 {target_directory}")
                    moved_folders[folder_id] += 1
                except Exception as e:
                    print(f"[移动] 移动文件夹 {folder_name} 到 {target_folder_path} 失败: {e}")
                    failed_folders[folder_id] += 1
                    failed_folder_names[folder_id].append(folder_name)
            else:
                try:
                    for item in os.listdir(source_folder_path):
                        shutil.move(os.path.join(source_folder_path, item), target_folder_path)
                    os.rmdir(source_folder_path)
                    print(f"[移动] 已合并文件夹 {folder_name} 到 {target_directory}")
                    moved_folders[folder_id] += 1
                except Exception as e:
                    print(f"[移动] 合并文件夹 {folder_name} 失败: {e}")
                    failed_folders[folder_id] += 1
                    failed_folder_names[folder_id].append(folder_name)

    # 删除空的用户文件夹
    for source_directory in [paths["source"] for paths in folder_path_id.values()]:
        for folder_name in os.listdir(source_directory):
            folder_path = os.path.join(source_directory, folder_name)
            if os.path.isdir(folder_path) and not os.listdir(folder_path):
                os.rmdir(folder_path)

    # 调用优化脚本
    try:
        print("\n[调用] 开始优化录播文件")
        subprocess.run(["python", script_path], check=True)
        print("[调用] 优化完成")
    except subprocess.CalledProcessError as e:
        print(f"\n[调用] 运行脚本失败: {e}")

    # 统计信息
    print_statistics(folder_path_id, total_folders, moved_folders, failed_folders, failed_folder_names)

# 定时任务
def schedule_jobs():
    # 设置定时任务
    schedule.every().day.at("00:00").do(move_folders)
    schedule.every().day.at("06:00").do(move_folders)
    schedule.every().day.at("12:00").do(move_folders)
    schedule.every().day.at("18:00").do(move_folders)

    while True:
        schedule.run_pending()
        time.sleep(1800)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n[计划] 当前时间:", current_time)
        if schedule.jobs:
            next_run_time = schedule.next_run().strftime("%Y-%m-%d %H:%M:%S")
            print("[计划] 下次运行时间:", next_run_time)
        else:
            print("[计划] 没有待执行的定时任务。")

# 主线程启动
if __name__ == "__main__":
    print("程序开始运行")
    print()
    move_folders()
    schedule_jobs()
