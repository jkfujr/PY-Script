# core/recheme.py

import os
import re
import logging
from collections import defaultdict
from datetime import datetime

# 移动操作
from .move import move_folder


# 录播姬录播处理，合并文件夹
def merge_folders(main_folder, folders_to_merge, recheme_skip_substrings):
    if not folders_to_merge:
        logging.warning(f"[录播姬] 未找到可合并的文件夹: {main_folder}")
        return

    logging.debug(f"[录播姬] 合并文件夹: {main_folder} <- {folders_to_merge}")
    for folder in folders_to_merge:
        if any(substring in folder for substring in recheme_skip_substrings):
            logging.debug(f"[录播姬] 跳过文件夹：{folder}")
            continue

        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            target_item_path = os.path.join(main_folder, item)
            logging.debug(f"[录播姬] 将 {item_path} 移动到 {target_item_path}")
            move_folder(item_path, target_item_path)

        os.rmdir(folder)


# 处理文件夹
def process_user_folder(
    id, user_folder, enable_move, folder_path_id, recheme_skip_substrings
):
    logging.info(f"[录播姬] 开始处理文件夹: {user_folder}")
    source_path = folder_path_id[id]["source"]
    target_path = folder_path_id[id].get("target")

    if not target_path and enable_move:
        logging.warning(f"[录播姬] 未提供目标路径，移动操作被禁用: {source_path}")
        enable_move = False

    user_folder_path = os.path.join(source_path, user_folder)

    if not os.path.exists(user_folder_path):
        logging.error(f"[录播姬] 文件夹不存在，无法处理: {user_folder_path}")
        return

    while True:
        subfolders = os.listdir(user_folder_path)
        if len(subfolders) == 0:
            break

        # 逻辑1: 只有一个子文件夹
        if len(subfolders) == 1:
            source_user_folder_path = os.path.join(source_path, user_folder)
            target_user_folder_path = os.path.join(target_path, user_folder)
            if enable_move:
                move_folder(source_user_folder_path, target_user_folder_path)
            break

        # 逻辑2: 有多个子文件夹
        subfolder_info = defaultdict(list)
        for subfolder in subfolders:
            if any(substring in subfolder for substring in recheme_skip_substrings):
                logging.debug(f"[录播姬] 跳过文件夹：{subfolder}")
                continue
            subfolder_path = os.path.join(user_folder_path, subfolder)

            # 匹配日期
            match = re.search(r"(\d{8}-\d{6})", subfolder)
            if match:
                time_info = match.group()
                subfolder_info[time_info].append(subfolder)
            else:
                logging.debug(f"[录播姬] 子文件夹命名不符合规则，跳过：{subfolder}")

        if not subfolder_info:
            break

        # 逻辑2.1: 合并操作
        merge_completed = False
        for time_info, subfolder_list in subfolder_info.items():
            if len(subfolder_list) >= 2:
                merge_logic_result = process_merge_logic(
                    id,
                    user_folder,
                    {time_info: subfolder_list},
                    folder_path_id,
                    recheme_skip_substrings,
                )
                if merge_logic_result:
                    merge_completed = True
                    break

        if not merge_completed:
            break

    logging.info(f"[录播姬] 处理完成文件夹: {user_folder}")


# 获取有效的子文件夹，并记录调试日志
def get_valid_subfolders(subfolder_list, skip_substrings):
    valid_subfolders = [
        subfolder
        for subfolder in subfolder_list
        if not any(skip_str in subfolder for skip_str in skip_substrings)
    ]
    logging.debug(f"[录播姬] 有效子文件夹筛选结果：{valid_subfolders}")
    return valid_subfolders


# 处理FLV文件，并记录调试日志
def process_flv_files(subfolder_list, user_folder_path):
    flv_time_mapping = {}
    for subfolder in subfolder_list:
        subfolder_path = os.path.join(user_folder_path, subfolder)
        flv_files = [f for f in os.listdir(subfolder_path) if f.endswith(".flv")]
        if flv_files:
            flv_files.sort(
                key=lambda f: datetime.strptime(
                    re.search(r"(\d{8}-\d{6})", f).group(), "%Y%m%d-%H%M%S"
                )
            )
            max_date_flv = flv_files[-1]
            flv_time_mapping[subfolder] = datetime.strptime(
                re.search(r"(\d{8}-\d{6})", max_date_flv).group(), "%Y%m%d-%H%M%S"
            )
    max_date_folder = (
        max(flv_time_mapping, key=flv_time_mapping.get) if flv_time_mapping else None
    )
    logging.debug(f"[录播姬] FLV文件处理结果：{max_date_folder}")
    return max_date_folder


# 处理合并逻辑
def process_merge_logic(
    id, user_folder, subfolder_info, folder_path_id, recheme_skip_substrings
):
    logging.debug(f"[录播姬] 开始处理合并逻辑，用户ID：{id}, 用户文件夹：{user_folder}")
    source_path = folder_path_id[id]["source"]
    user_folder_path = os.path.join(source_path, user_folder)

    for time_info, subfolder_list in subfolder_info.items():
        valid_subfolders = get_valid_subfolders(subfolder_list, recheme_skip_substrings)
        if not valid_subfolders:
            logging.debug(f"[录播姬] 没有有效的子文件夹，跳过当前时间信息：{time_info}")
            continue

        max_date_folder = process_flv_files(valid_subfolders, user_folder_path)
        if not max_date_folder:
            logging.debug(f"[录播姬] 找不到有效的FLV文件，跳过：{time_info}")
            continue

        main_subfolder_path = os.path.join(user_folder_path, max_date_folder)
        if any(
            substring in main_subfolder_path for substring in recheme_skip_substrings
        ):
            logging.debug(
                f"[录播姬] 主文件夹包含跳过子字符串，跳过：{main_subfolder_path}"
            )
            continue

        logging.info(f"[录播姬] 合并文件夹：{main_subfolder_path}")
        merge_folders(
            main_subfolder_path,
            [
                os.path.join(user_folder_path, subfolder)
                for subfolder in valid_subfolders
                if subfolder != max_date_folder
            ],
            recheme_skip_substrings,
        )

        if not os.listdir(main_subfolder_path):
            os.rmdir(main_subfolder_path)
            logging.debug(f"[录播姬] 删除空文件夹：{main_subfolder_path}")
        return True

    logging.debug(f"[录播姬] 合并逻辑处理完成，用户文件夹：{user_folder}")
    return False


def recheme_main(
    folder_path_id, enable_move, social_folders, skip_folders, recheme_skip_substrings
):
    # 遍历用户文件夹
    for id, paths in folder_path_id.items():
        source_path = paths["source"]
        target_path = paths.get("target")

        # 检查源路径是否存在
        if not os.path.exists(source_path):
            logging.warning(f"[录播姬] 源路径不存在：{source_path}")
            continue

        logging.info(f"[录播姬] 开始处理源路径: {source_path}")

        # 跳过文件夹
        for user_folder in os.listdir(source_path):
            if user_folder in skip_folders:
                continue

            user_folder_path = os.path.join(source_path, user_folder)
            if not os.path.isdir(user_folder_path):
                continue

            # 检查是否是社团文件夹，如果是则进入下一层文件夹
            is_social_folder = user_folder in social_folders
            if is_social_folder:
                for sub_user_folder in os.listdir(user_folder_path):
                    sub_user_folder_path = os.path.join(user_folder_path, sub_user_folder)
                    if not os.path.isdir(sub_user_folder_path):
                        continue
                    logging.info(f"[录播姬] 开始处理子文件夹: {sub_user_folder_path}")
                    process_user_folder(
                        id,
                        os.path.join(user_folder, sub_user_folder),
                        enable_move,
                        folder_path_id,
                        recheme_skip_substrings,
                    )
            else:
                logging.info(f"[录播姬] 开始处理文件夹: {user_folder_path}")
                process_user_folder(
                    id,
                    user_folder,
                    enable_move,
                    folder_path_id,
                    recheme_skip_substrings,
                )

        # 删除空文件夹
        if not os.listdir(source_path):
            os.rmdir(source_path)
