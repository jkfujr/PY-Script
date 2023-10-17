import os
import re
from datetime import datetime, timedelta


folder_path = r"E:\下载\mana\youtube\2019"


# 定义重命名函数
def rename_file(folder_path, filename):
    match = re.search(r"(\d{8}_\d{6}).*\.(.*?)$", filename)
    if match:
        utc_time_str = match.group(1)
        file_extension = match.group(2)

        # 检查文件扩展名是否在指定的类型中
        if file_extension in ["mp4", "flv"]:
            # 转换为UTC时间
            utc_time = datetime.strptime(utc_time_str, "%Y%m%d_%H%M%S")

            # 转换为中国标准时间（CST）
            cst_time = utc_time + timedelta(hours=8)

            # 构建新的文件名
            new_date_part = cst_time.strftime("%Y%m%d")
            new_time_part = cst_time.strftime("%H%M%S")
            new_filename = new_date_part + "-" + new_time_part + filename[15:]

            # 构建新的文件路径
            old_filepath = os.path.join(folder_path, filename)
            new_filepath = os.path.join(folder_path, new_filename)

            # 重命名文件
            os.rename(old_filepath, new_filepath)

            # 打印老文件名和新文件名
            print(f"重命名文件: {filename} -> {new_filename}")
    else:
        # 文件名中没有对应的时间格式
        print(f"无法处理的文件名: {filename}")


for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
        rename_file(folder_path, filename)