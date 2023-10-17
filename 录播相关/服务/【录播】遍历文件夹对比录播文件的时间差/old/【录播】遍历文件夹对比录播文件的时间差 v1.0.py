import os
import csv
from datetime import datetime

folder_path = r"F:\Video\AAAAAAAAAA"

# 排除的文件夹名
excluded_folders = ["00", "000"]  

# 创建CSV文件并写入表头
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file_path = os.path.join(script_dir, "output.csv")

# 创建CSV文件并写入表头
with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["用户ID", "子文件夹名称", "开播时间差"])

# 遍历路径下的所有文件夹和文件
for root, folders, files in os.walk(folder_path):
    # 排除指定的文件夹
    folders[:] = [folder for folder in folders if folder not in excluded_folders]

    # 遍历所有文件夹
    for folder in folders:
        folder_path = os.path.join(root, folder)
        
        # 获取用户ID
        user_id = os.path.basename(folder_path)
        
        # 初始化时间差
        time_diff = None

        # 遍历子文件夹
        for sub_folder in os.listdir(folder_path):
            sub_folder_path = os.path.join(folder_path, sub_folder)

            # 如果是文件夹且符合指定的命名格式
            if os.path.isdir(sub_folder_path) and "_" in sub_folder and "【" in sub_folder and "】" in sub_folder:
                # 提取子文件夹中时间
                sub_folder_time = sub_folder.split("_")[0]
                
                # 初始化最早时间
                earliest_time = datetime.max
                
                # 初始化最早时间的文件名
                earliest_file_name = None

                # 遍历子文件夹中的文件
                for file in os.listdir(sub_folder_path):
                    file_path = os.path.join(sub_folder_path, file)
                    
                    # 如果是flv文件
                    if os.path.isfile(file_path) and file.endswith(".flv"):
                        # 提取文件名中的时间
                        file_time = file.split(".")[0]
                        file_time = file_time[:15]
                        
                        # 将时间字符串转换为datetime对象
                        file_time = datetime.strptime(file_time, "%Y%m%d-%H%M%S")
                        
                        # 比较时间，找到最早的时间和对应的文件名
                        if file_time < earliest_time:
                            earliest_time = file_time
                            earliest_file_name = file

                # 如果找到了最早时间的文件
                if earliest_file_name is not None:
                    # 提取最早时间的文件名中的时间
                    earliest_file_time = earliest_file_name.split("_")[0]
                    earliest_file_time = earliest_file_time[:15]
                    
                    # 将时间字符串转换为datetime对象
                    earliest_file_time = datetime.strptime(earliest_file_time, "%Y%m%d-%H%M%S")
                    
                    # 计算时间差
                    time_diff = earliest_file_time - datetime.strptime(sub_folder_time, "%Y%m%d-%H%M%S")
                    
                    # 将时间差转换为字符串
                    time_diff_str = str(time_diff)
                    
                    # 提取时、分、秒部分
                    hours, minutes, seconds = time_diff_str.split(":")
                    
                    # 格式化时间差
                    time_diff_formatted = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
                    
                    # 写入CSV文件
                    with open(output_file_path, mode='a', encoding='utf-8', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([user_id, sub_folder, time_diff_formatted])

print("写入完成")