import os
import time

folder_path = r"E:\下载\ayamy\youtube"

for folder_name in os.listdir(folder_path):
    if os.path.isdir(os.path.join(folder_path, folder_name)):
        try:
            timestamp = int(folder_name.split("_")[0])
        except ValueError as e:
            print(f"文件夹 {folder_name} 不符合条件： {e}")
            continue
        dt = time.strftime("%Y%m%d-%H%M%S", time.localtime(timestamp))
        new_folder_name = f"{dt}_{folder_name.split('_', 1)[1]}"
        os.rename(os.path.join(folder_path, folder_name), os.path.join(folder_path, new_folder_name))