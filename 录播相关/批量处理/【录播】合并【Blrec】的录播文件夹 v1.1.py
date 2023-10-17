import os
import re
from collections import defaultdict
from datetime import datetime


def parse_folder_name(folder_name):
    # 使用正则表达式从文件夹名称中提取日期、标题和后缀信息
    pattern = r"(\d{8})-(\d{6})_(.+)\【(blrec-flv|blrec-hls)\】"
    match = re.match(pattern, folder_name)
    if match:
        date_str, time_str, title, suffix = match.groups()
        date = datetime.strptime(date_str + "-" + time_str, "%Y%m%d-%H%M%S")
        return date, title, suffix
    return None, None, None


def merge_folders(folder_paths):
    folders = defaultdict(list)

    # 遍历指定的多个文件夹路径
    for folder_path in folder_paths:
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for root, subfolders, files in os.walk(folder_path):
                for folder_name in subfolders:
                    folder_full_path = os.path.join(root, folder_name)

                    # 解析文件夹名称，获取日期、标题和后缀信息
                    date, title, suffix = parse_folder_name(folder_name)
                    if date and title and suffix:
                        # 将具有相同日期、标题和后缀的文件夹分组
                        folders[(date.date(), title, suffix)].append(
                            (date, folder_full_path)
                        )

    # 合并具有相同日期且时间差小于4小时的文件夹
    for _, folder_list in folders.items():
        if len(folder_list) > 1:
            folder_list.sort(key=lambda x: x[0])  # 按照日期进行排序
            for i in range(len(folder_list) - 1):
                time_diff = folder_list[i + 1][0] - folder_list[i][0]
                if (
                    time_diff.total_seconds() <= 4 * 60 * 60
                ):  # 判断时间差是否小于4小时（4 * 60 * 60秒）
                    merge_to_folder = folder_list[i][1]  # 使用第一个文件夹作为合并目标

                    # 将其他文件夹内容合并到目标文件夹
                    for folder_to_merge in folder_list[i + 1 :]:
                        print(f"[Info] 合并: {folder_to_merge[1]} -> {merge_to_folder}")
                        merge_files(merge_to_folder, folder_to_merge[1])
                        os.rmdir(folder_to_merge[1])  # 删除已合并的文件夹
                    break

    print("[Info] 全部完成")


def merge_files(target_folder, source_folder):
    # 将源文件夹中的文件移动到目标文件夹中
    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)
        target_file = os.path.join(target_folder, filename)
        os.rename(source_file, target_file)


if __name__ == "__main__":
    folder_paths = [
        r"F:\Video\PPPPPPPPPP",
    ]
    merge_folders(folder_paths)
