import os
import re
import datetime

root_directory = r"E:\下载\乙夜かろり_karory"

# 遍历根目录和子文件夹
for root, dirs, files in os.walk(root_directory):
    for foldername in dirs:
        folder_path = os.path.join(root, foldername)

        oldest_flv = None
        oldest_flv_time = None

        # 遍历文件夹内的文件
        for filename in os.listdir(folder_path):
            if filename.endswith(".flv"):
                flv_file = os.path.join(folder_path, filename)

                # 正则表达式匹配文件名中的时间部分
                match = re.match(r".*?(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2}).*?", filename)
                if match:
                    year, month, day, hour, minute, second = match.groups()
                    flv_time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

                    # 判断是否为最早的文件
                    if oldest_flv_time is None or flv_time < oldest_flv_time:
                        oldest_flv = flv_file
                        oldest_flv_time = flv_time

        # 如果没有找到有效的 .flv 文件，则跳过该文件夹的处理
        if oldest_flv is None:
            continue

        # 生成新的文件夹名称
        new_folder_name = oldest_flv_time.strftime('%Y%m%d-%H%M%S_') + foldername.split('_', 1)[-1]

        # 生成新的文件夹路径
        new_folder_path = os.path.join(os.path.dirname(folder_path), new_folder_name)

        # 对文件夹进行重命名
        os.rename(folder_path, new_folder_path)
        print(f"[Info] 重命名: {folder_path} → {new_folder_path}")