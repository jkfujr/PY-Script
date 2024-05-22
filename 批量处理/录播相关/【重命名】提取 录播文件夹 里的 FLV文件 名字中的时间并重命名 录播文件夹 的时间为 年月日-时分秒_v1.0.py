import os
import re
import datetime
import shutil

def rename_folders_with_flv(root_directory):
    # 遍历根目录和子文件夹
    for root, dirs, files in os.walk(root_directory):
        for foldername in dirs:
            # 只处理符合 "年月日_标题" 格式的子文件夹
            if not re.match(r'^\d{8}_', foldername):
                continue

            # 检查文件夹名是否已经以 "年月日-时分秒_" 开头
            if re.match(r'^\d{8}-\d{6}_', foldername):
                print(f"[Info] 跳过: {foldername} 已经是以时间开头的格式")
                continue

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

                        # 验证时间值是否合法
                        try:
                            flv_time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
                        except ValueError as e:
                            print(f"[Error] 跳过无效的时间值: {filename}, 错误: {e}")
                            continue

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

def merge_folders(root_directory):
    folder_info = []
    
    # 获取所有子文件夹信息
    for root, dirs, files in os.walk(root_directory):
        for foldername in dirs:
            match = re.match(r'^(\d{8})-(\d{6})_(.+)$', foldername)
            if match:
                date, time, title = match.groups()
                folder_info.append((datetime.datetime.strptime(date + time, '%Y%m%d%H%M%S'), title, os.path.join(root, foldername)))

    # 按日期时间排序文件夹信息
    folder_info.sort()

    # 合并符合条件的文件夹
    merged_folders = set()
    for i in range(len(folder_info) - 1):
        current_folder = folder_info[i]
        next_folder = folder_info[i + 1]

        current_time = current_folder[0].time()
        next_time = next_folder[0].time()

        # 判断是否符合合并条件
        if (current_folder[1] == next_folder[1] and
            datetime.time(22, 0) <= current_time <= datetime.time(23, 59) and
            datetime.time(0, 0) <= next_time <= datetime.time(2, 0)):
            
            # 合并文件夹
            for filename in os.listdir(next_folder[2]):
                src_file = os.path.join(next_folder[2], filename)
                dst_file = os.path.join(current_folder[2], filename)
                if os.path.exists(dst_file):
                    dst_file = os.path.join(current_folder[2], f"copy_{filename}")
                shutil.move(src_file, dst_file)
            
            os.rmdir(next_folder[2])
            print(f"[Info] 合并: {next_folder[2]} → {current_folder[2]}")
            merged_folders.add(next_folder[2])

    # 输出合并后的结果
    for folder in merged_folders:
        print(f"[Info] 已合并: {folder}")

# 调用函数并传入根目录
root_directory = r"E:\录播\黑桐亚里亚Official"
rename_folders_with_flv(root_directory)
merge_folders(root_directory)
