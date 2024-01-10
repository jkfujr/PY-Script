import os
import re
import logging
from collections import defaultdict
from datetime import datetime

# 移动操作
from recheme.move import move_folder


### 日志模块
# 日志文件夹路径和日志文件名
log_folder = "logs"
log_filename = datetime.now().strftime("%Y%m%d-%H%M%S.log")
log_file_path = os.path.join(os.path.dirname(__file__), log_folder, log_filename)

# 确保日志文件夹存在
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# 设置日志记录器
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


### 设定
# 是否启用移动文件夹
enable_move = True

# 执行路径
folder_path_id = {
    "AAA": {"source": r"F:\Video\AAAAAAAAAA", "target": r"F:\Video\AAAAAAAAAA\000"},
    "PPP": {"source": r"F:\Video\PPPPPPPPPP", "target": r"F:\Video\PPPPPPPPPP\000"},
    "TEST": {"source": r"F:\测试数据", "target": r"F:\测试数据\000"},
}

# 社团文件夹名称列表
social_folders = ["NIJISANJI", "HOLOLIVE", "VSPO"]

# 需要跳过的特殊文件夹名称列表
skip_folders = ["000", "111"]

# 录播姬_需要跳过的录播子文件夹
recheme_skip_substrings = ["【blrec-flv】", "【blrec-hls】", "000_部分丢失"]


# 录播姬录播处理，合并文件夹
def merge_folders(main_folder, folders_to_merge):
    logging.info(f"合并文件夹: {main_folder} <- {folders_to_merge}")
    for folder in folders_to_merge:
        if any(substring in folder for substring in recheme_skip_substrings):
            logging.info(f"跳过文件夹：{folder}")
            continue

        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            target_item_path = os.path.join(main_folder, item)
            logging.info(f"将 {item_path} 移动到 {target_item_path}")
            move_folder(item_path, target_item_path)

        os.rmdir(folder)


# 处理文件夹
def process_user_folder(id, user_folder):
    source_path = folder_path_id[id]["source"]
    target_path = folder_path_id[id]["target"]

    user_folder_path = os.path.join(source_path, user_folder)

    subfolders = os.listdir(user_folder_path)

    # 逻辑1: 只有一个子文件夹
    if len(subfolders) == 1:
        source_user_folder_path = os.path.join(source_path, user_folder)
        target_user_folder_path = os.path.join(target_path, user_folder)
        if enable_move:
            move_folder(source_user_folder_path, target_user_folder_path)

    # 逻辑2: 有多个子文件夹
    elif len(subfolders) >= 2:
        subfolder_info = defaultdict(list)

        for subfolder in subfolders:
            if any(substring in subfolder for substring in recheme_skip_substrings):
                logging.debug(f"跳过文件夹：{subfolder}")
                continue
            subfolder_path = os.path.join(user_folder_path, subfolder)

            # 匹配日期
            match = re.search(r"(\d{8}-\d{6})", subfolder)
            if match:
                time_info = match.group()
                subfolder_info[time_info].append(subfolder)
            else:
                logging.info(f"子文件夹命名不符合规则，跳过：{subfolder}")

        # 逻辑2.1: 存在同日期的子文件夹
        for time_info, subfolder_list in subfolder_info.items():
            # 如果同日期的子文件夹数量大于等于2，则需要合并
            while len(subfolder_list) >= 2:
                merge_logic_result = process_merge_logic(
                    id, user_folder, {time_info: subfolder_list}
                )

                # 如果成功合并，更新子文件夹信息
                if merge_logic_result:
                    subfolder_list = [
                        subfolder
                        for subfolder in os.listdir(user_folder_path)
                        if os.path.isdir(os.path.join(user_folder_path, subfolder))
                    ]
                else:
                    # 如果无法合并（例如因为所有子文件夹都包含需要跳过的子字符串），跳出循环
                    break

        # 逻辑2.2: 执行逻辑1
        if len(os.listdir(user_folder_path)) == 1:
            source_user_folder_path = os.path.join(source_path, user_folder)
            target_user_folder_path = os.path.join(target_path, user_folder)
            if enable_move:
                move_folder(source_user_folder_path, target_user_folder_path)


# 处理合并逻辑
def process_merge_logic(id, user_folder, subfolder_info):
    source_path = folder_path_id[id]["source"]
    user_folder_path = os.path.join(source_path, user_folder)

    for time_info, subfolder_list in subfolder_info.items():
        valid_subfolders = [
            subfolder
            for subfolder in subfolder_list
            if not any(skip_str in subfolder for skip_str in recheme_skip_substrings)
        ]

        # 如果没有有效的子文件夹，跳过当前时间信息的处理
        if not valid_subfolders:
            logging.debug(f"跳过合并：{subfolder_list}")
            continue

        if len(subfolder_list) >= 2:
            # 存储FLV文件的时间和文件名的映射关系
            flv_time_mapping = {}

            # 遍历同日期时间的子文件夹，找出FLV文件的时间并存储到映射中
            for subfolder in subfolder_list:
                subfolder_path = os.path.join(source_path, user_folder, subfolder)
                flv_files = [
                    f for f in os.listdir(subfolder_path) if f.endswith(".flv")
                ]

                if flv_files:
                    flv_files.sort(
                        key=lambda f: datetime.strptime(
                            re.search(r"(\d{8}-\d{6})", f).group(), "%Y%m%d-%H%M%S"
                        )
                    )
                    max_date_flv = flv_files[-1]
                    flv_time_mapping[subfolder] = (
                        datetime.strptime(
                            re.search(r"(\d{8}-\d{6})", max_date_flv).group(),
                            "%Y%m%d-%H%M%S",
                        )
                        if max_date_flv.endswith(".flv")
                        else None
                    )

            # 找到时间最大的FLV所在的子文件夹
            max_date_folder = max(flv_time_mapping, key=flv_time_mapping.get)

            # 获取子文件夹路径
            main_subfolder_path = os.path.join(
                source_path, user_folder, max_date_folder
            )

            if any(
                substring in main_subfolder_path
                for substring in recheme_skip_substrings
            ):
                continue

            # 合并其他日期时间一样但标题不一样的子文件夹
            merge_folders(
                main_subfolder_path,
                [
                    os.path.join(source_path, user_folder, subfolder)
                    for subfolder in subfolder_list
                    if subfolder != max_date_folder
                ],
            )

            # 删除合并后的空文件夹
            if not os.listdir(main_subfolder_path):
                os.rmdir(main_subfolder_path)
            return True

    return False


# 遍历用户文件夹
for id, paths in folder_path_id.items():
    source_path = paths["source"]
    target_path = paths["target"]

    # 检查源路径是否存在
    if not os.path.exists(source_path):
        logging.warning(f"源路径不存在：{source_path}")
        continue

    logging.info(f"开始处理源路径: {source_path}")

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
                # 更新路径，加上社团文件夹的路径
                sub_user_folder_path = os.path.join(
                    target_path, user_folder, sub_user_folder
                )
                logging.info(f"开始处理源路径: {sub_user_folder_path}")
                process_user_folder(id, sub_user_folder_path)
        else:
            logging.info(f"开始处理文件夹: {user_folder_path}")
            process_user_folder(id, user_folder)

    # 删除空文件夹
    if not os.listdir(source_path):
        os.rmdir(source_path)
