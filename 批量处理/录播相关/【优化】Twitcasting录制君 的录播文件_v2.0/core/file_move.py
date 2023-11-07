import os
import shutil
import sys


file_path = sys.argv[1]

# 获取当前目录
current_dir = os.getcwd()

def process_files():
    folder_contents = os.listdir(file_path)

    for folder_name in folder_contents:
        folder_path = os.path.join(file_path, folder_name)
        subfolder_path = os.path.join(folder_path, "twitcasting")

        if os.path.isdir(folder_path):
            os.makedirs(subfolder_path, exist_ok=True)

            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    shutil.move(item_path, subfolder_path)

            print(f"[Info] 处理完成: {folder_name}")

    print("")
    print("[Info] 已完成 所有弹幕与录播文件 移动操作")

process_files()
