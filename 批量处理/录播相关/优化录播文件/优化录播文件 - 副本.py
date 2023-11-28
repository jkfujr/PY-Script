import os
import shutil
import re
from collections import defaultdict
from datetime import datetime

# 移动文件夹
def move_folder(source, target):
    if not os.path.exists(target):
        print(f"移动文件夹：{source} -> {target}")
        shutil.move(source, target)
    else:
        print(f"目标文件夹已存在，合并内容：{source} -> {target}")
        for item in os.listdir(source):
            source_item_path = os.path.join(source, item)
            target_item_path = os.path.join(target, item)
            if os.path.exists(target_item_path):
                print(f"目标位置已存在同名项，跳过：{target_item_path}")
                continue
            print(f"移动项：{source_item_path} -> {target_item_path}")
            shutil.move(source_item_path, target_item_path)
        try:
            os.rmdir(source)
            print(f"源文件夹已清空，已删除：{source}")
        except OSError:
            print(f"源文件夹未完全清空，未删除：{source}")

# 合并文件夹
def merge_folders(main_folder, folders_to_merge):
    print(f"合并文件夹: {main_folder} <- {folders_to_merge}")
    for folder in folders_to_merge:
        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            target_item_path = os.path.join(main_folder, item)
            print(f"将 {item_path} 移动到 {target_item_path}")
            shutil.move(item_path, target_item_path)
        os.rmdir(folder)

# 处理用户文件夹
def process_user_folder(user_folder_path):
    print(f"处理文件夹: {user_folder_path}")
    subfolders = os.listdir(user_folder_path)

    # 逻辑1: 只有一个子文件夹
    if len(subfolders) == 1:
        source_user_folder_path = os.path.join(source_path, user_folder)
        target_user_folder_path = os.path.join(target_path, user_folder)
        move_folder(source_user_folder_path, target_user_folder_path)

    # 逻辑2: 有多个子文件夹
    elif len(subfolders) >= 2:
        subfolder_info = defaultdict(list)

        for subfolder in subfolders:
            subfolder_path = os.path.join(user_folder_path, subfolder)
            if os.path.isdir(subfolder_path):
                time_info = re.search(r'(\d{8}-\d{6})', subfolder).group()
                subfolder_info[time_info].append(subfolder)

        # 逻辑2.1.1: 子文件夹日期时间一样但标题不一样
        merge_logic_result = process_merge_logic(user_folder_path, subfolder_info)

        # 逻辑2.1.2: 合并后只剩下一个子文件夹，执行逻辑1
        if len(os.listdir(user_folder_path)) == 1:
            source_user_folder_path = os.path.join(source_path, user_folder)
            target_user_folder_path = os.path.join(target_path, user_folder)
            move_folder(source_user_folder_path, target_user_folder_path)
# 处理合并逻辑
def process_merge_logic(user_folder_path, subfolder_info):
    for time_info, subfolder_list in subfolder_info.items():
        if len(subfolder_list) >= 2:
            print(f"子文件夹日期时间一样但标题不一样: {time_info}")
            print(f"子文件夹列表: {subfolder_list}")

            # 存储FLV文件的时间和文件名的映射关系
            flv_time_mapping = {}

            # 遍历同日期时间的子文件夹，找出FLV文件的时间并存储到映射中
            for subfolder in subfolder_list:
                subfolder_path = os.path.join(user_folder_path, subfolder)
                flv_files = [f for f in os.listdir(subfolder_path) if f.endswith('.flv')]

                if flv_files:
                    flv_files.sort(key=lambda f: datetime.strptime(re.search(r'(\d{8}-\d{6})', f).group(), "%Y%m%d-%H%M%S"))
                    max_date_flv = flv_files[-1]
                    flv_time_mapping[subfolder] = datetime.strptime(re.search(r'(\d{8}-\d{6})', max_date_flv).group(), "%Y%m%d-%H%M%S") if max_date_flv.endswith('.flv') else None

            # 找到时间最大的FLV所在的子文件夹
            max_date_folder = max(flv_time_mapping, key=flv_time_mapping.get)

            print(f"时间最大的FLV所在的子文件夹: {max_date_folder}")

            # 获取子文件夹路径
            main_subfolder_path = os.path.join(user_folder_path, max_date_folder)

            # 合并其他日期时间一样但标题不一样的子文件夹
            merge_folders(main_subfolder_path, [os.path.join(user_folder_path, subfolder) for subfolder in subfolder_list if subfolder != max_date_folder])

            # 删除合并后的空主子文件夹
            if not os.listdir(main_subfolder_path):
                os.rmdir(main_subfolder_path)
            
            return True  # 合并逻辑执行成功

    return False  # 未执行合并逻辑

source_path = r'F:\Video\AAAAAAAAAA'
target_path = r'F:\Video\AAAAAAAAAA\000'

# 遍历用户文件夹
for user_folder in os.listdir(source_path):
    # 跳过文件夹
    if user_folder in ["000"]:
        continue

    user_folder_path = os.path.join(source_path, user_folder)
    if not os.path.isdir(user_folder_path):
        continue

    # 检查是否是社团文件夹
    is_social_folder = user_folder in ["NIJISANJI", "HOLOLIVE", "VSPO"]

    # 如果是社团文件夹，进入下一层文件夹
    if is_social_folder:
        for sub_user_folder in os.listdir(user_folder_path):
            sub_user_folder_path = os.path.join(user_folder_path, sub_user_folder)
            if not os.path.isdir(sub_user_folder_path):
                continue

            process_user_folder(sub_user_folder_path)

    # 如果不是社团文件夹，直接处理
    else:
        process_user_folder(user_folder_path)

# 删除空文件夹
if not os.listdir(source_path):
    os.rmdir(source_path)
