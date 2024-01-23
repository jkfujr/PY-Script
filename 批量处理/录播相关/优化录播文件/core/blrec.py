# core/blrec.py

import os
import re
import logging
from collections import defaultdict
from datetime import datetime

def parse_folder_name(folder_name):
    pattern = r"(\d{8})-(\d{6})_(.+)\【(blrec-flv|blrec-hls)\】"
    match = re.match(pattern, folder_name)
    if match:
        date_str, time_str, title, suffix = match.groups()
        date = datetime.strptime(date_str + "-" + time_str, "%Y%m%d-%H%M%S")
        return date, title, suffix
    # else:
    #     logging.warning(f"[BLREC] 无法解析文件夹名：{folder_name}")
    return None, None, None

def should_process_folder(folder_name, social_folders, skip_folders):
    if folder_name in skip_folders:
        logging.debug(f"[BLREC] 跳过文件夹：{folder_name} (在跳过列表中)")
        return False
    if any(folder_name.startswith(social) for social in social_folders):
        logging.debug(f"[BLREC] 跳过社团文件夹：{folder_name}")
        return False
    return True

def merge_folders(folder_path_id, enable_move, social_folders, skip_folders):
    logging.debug("[BLREC] 开始合并文件夹")

    for id, paths in folder_path_id.items():
        source_path = paths["source"]
        if not os.path.exists(source_path) or not os.path.isdir(source_path):
            logging.warning(f"[BLREC] 源路径不存在或不是目录：{source_path}")
            continue

        while True:
            folders = defaultdict(list)
            for root, dirs, files in os.walk(source_path, topdown=True):
                dirs[:] = [d for d in dirs if should_process_folder(d, social_folders, skip_folders)]
                for folder_name in dirs:
                    folder_full_path = os.path.join(root, folder_name)
                    date, title, suffix = parse_folder_name(folder_name)
                    if date and title and suffix:
                        folders[(date.date(), title, suffix)].append((date, folder_full_path))

            merge_completed = False
            for key, folder_list in folders.items():
                if len(folder_list) > 1:
                    logging.debug(f"[BLREC] 发现可合并文件夹：{key}")
                    folder_list.sort(key=lambda x: x[0])
                    for i in range(len(folder_list) - 1):
                        time_diff = folder_list[i + 1][0] - folder_list[i][0]
                        if time_diff.total_seconds() <= 4 * 60 * 60:
                            merge_to_folder = folder_list[i][1]
                            for folder_to_merge in folder_list[i + 1:]:
                                logging.info(f"[BLREC] 合并: {folder_to_merge[1]} -> {merge_to_folder}")
                                merge_files(merge_to_folder, folder_to_merge[1])
                                try:
                                    os.rmdir(folder_to_merge[1])
                                    merge_completed = True
                                except Exception as e:
                                    logging.error(f"[BLREC] 删除文件夹失败：{folder_to_merge[1]}, 错误：{e}")
                    if merge_completed:
                        break
                else:
                    logging.info(f"[BLREC] 没有找到可以合并的文件夹组：{key}")

            if not merge_completed:
                break

def merge_files(target_folder, source_folder):
    if not os.path.exists(source_folder):
        logging.warning(f"[BLREC] 源文件夹不存在，无法合并: {source_folder}")
        return

    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)
        target_file = os.path.join(target_folder, filename)
        try:
            os.rename(source_file, target_file)
            logging.info(f"[BLREC] 文件移动：{source_file} -> {target_file}")
        except Exception as e:
            logging.error(f"[BLREC] 文件移动失败：{source_file} -> {target_file}, 错误：{e}")


def blrec_main(folder_path_id, enable_move, social_folders, skip_folders):
    merge_folders(folder_path_id, enable_move, social_folders, skip_folders)
