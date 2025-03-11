import os
import re
import datetime
import shutil

def rename_folders_with_flv(root_directory):
    # 遍历根目录和子文件夹
    for root, dirs, files in os.walk(root_directory):
        for foldername in dirs:
            # 只处理符合 "年月日_标题" 或 "19700101-080000_标题" 格式的子文件夹
            if not re.match(r'^\d{8}_', foldername) and not re.match(r'^\d{8}-\d{6}_', foldername):
                continue

            # 检查文件夹名是否已经以 "年月日-时分秒_" 开头，跳过 "19700101-080000_" 的文件夹
            if re.match(r'^\d{8}-\d{6}_', foldername) and not re.match(r'^19700101-080000_', foldername):
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

# 检查文件夹
def check_folders(root_directory):
    date_dict = {}
    date_title_dict = {}
    date_title_hour_dict = {}
    hour_00_01_dict = {}

    for root, dirs, files in os.walk(root_directory):
        for foldername in dirs:
            date_match = re.match(r'^(\d{8})-\d{6}_', foldername)
            date_title_match = re.match(r'^(\d{8})-\d{6}_(.+)$', foldername)
            date_title_hour_match = re.match(r'^(\d{8})-(\d{2})\d{4}_(.+)$', foldername)
            hour_00_01_match = re.match(r'^(\d{8})-(\d{2})\d{4}_(.+)$', foldername)
            
            if date_match:
                date = date_match.group(1)
                if date not in date_dict:
                    date_dict[date] = []
                date_dict[date].append(foldername)

            if date_title_match:
                date, title = date_title_match.groups()
                if (date, title) not in date_title_dict:
                    date_title_dict[(date, title)] = []
                date_title_dict[date, title].append(foldername)

            if date_title_hour_match:
                date, hour, title = date_title_hour_match.groups()
                key = (date, title, hour)
                if key not in date_title_hour_dict:
                    date_title_hour_dict[key] = []
                date_title_hour_dict[key].append(foldername)

            if hour_00_01_match:
                date, hour, title = hour_00_01_match.groups()
                if hour in ['00', '01']:
                    if (date, hour) not in hour_00_01_dict:
                        hour_00_01_dict[(date, hour)] = []
                    hour_00_01_dict[(date, hour)].append(foldername)

    print("\n小时为00、01的文件夹:")
    for (date, hour), folders in hour_00_01_dict.items():
        print(f"日期 ({date}) 小时 ({hour}) 的文件夹: {folders}")

    print("同一天的文件夹:")
    for date, folders in date_dict.items():
        if len(folders) > 1:
            print(f"同一天 ({date}) 的文件夹: {folders}")

    print("\n同一天且标题相同的文件夹:")
    for (date, title), folders in date_title_dict.items():
        if len(folders) > 1:
            print(f"同一天 ({date}) 且标题相同 ({title}) 的文件夹: {folders}")

    print("\n同一天、标题相同且小时相同的文件夹:")
    for (date, title, hour), folders in date_title_hour_dict.items():
        if len(folders) > 1:
            print(f"同一天 ({date})、标题相同 ({title}) 且小时相同 ({hour}) 的文件夹: {folders}")

# 新增函数用于重命名FLV文件
def rename_flv_files(target_directory):
    for filename in os.listdir(target_directory):
        if filename.endswith(".flv"):
            try:
                # 找到最后一个下划线的位置
                last_underscore_index = filename.rfind('_')
                if last_underscore_index == -1:
                    print(f"[Error] 无法找到下划线: {filename}")
                    continue

                # 提取标题和时间部分
                title = filename[:last_underscore_index]
                date_time = filename[last_underscore_index + 1: -4]

                # 分割时间部分
                match = re.match(r"(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})", date_time)
                if not match:
                    print(f"[Error] 无法解析时间: {filename}")
                    continue
                
                year, month, day, hour, minute, second = match.groups()

                # 找到标题中的最后一个下划线，用于分割用户名和标题
                second_last_underscore_index = title.rfind('_')
                if second_last_underscore_index == -1:
                    print(f"[Error] 无法找到第二个下划线: {filename}")
                    continue
                
                # 获取真正的标题部分
                real_title = title[second_last_underscore_index + 1:]

                # 生成新的文件名
                new_filename = f"{year}{month}{day}-{hour}{minute}{second}_{real_title}.flv"
                old_file_path = os.path.join(target_directory, filename)
                new_file_path = os.path.join(target_directory, new_filename)
                
                # 重命名文件
                os.rename(old_file_path, new_file_path)
                print(f"[Info] 重命名: {old_file_path} → {new_file_path}")
            except Exception as e:
                print(f"[Error] 处理文件时出错: {filename}, 错误: {e}")


root_directory = r"E:\录播\紫海由爱Channel"
# 目录
check_folders(root_directory)
rename_folders_with_flv(root_directory)
merge_folders(root_directory)

# 文件
# rename_flv_files(root_directory)
