# core/move.py

import os
import shutil
import logging
import hashlib

# MD5计算
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def move_folder(source, target, enable_move=True):
    if enable_move:
        if not os.path.exists(target):
            logging.info(f"[move] 移动文件：{source} -> {target}")
            shutil.move(source, target)
        else:
            logging.info(f"[move] 目标文件夹已存在，合并内容：{source} -> {target}")
            for item in os.listdir(source):
                source_item_path = os.path.join(source, item)
                target_item_path = os.path.join(target, item)
                if os.path.exists(target_item_path):
                    if os.path.isfile(source_item_path) and os.path.isfile(target_item_path):
                        source_md5 = calculate_md5(source_item_path)
                        target_md5 = calculate_md5(target_item_path)
                        if source_md5 == target_md5:
                            logging.debug(f"[move] 文件内容相同，删除源文件：{source_item_path}")
                            os.remove(source_item_path)
                        else:
                            logging.debug(f"[move] 目标位置已存在同名项且文件内容不同，跳过：{target_item_path}")
                    else:
                        logging.debug(f"[move] 目标位置已存在同名项，跳过：{target_item_path}")
                    continue
                logging.debug(f"[move] 移动项：{source_item_path} -> {target_item_path}")
                shutil.move(source_item_path, target_item_path)
            try:
                os.rmdir(source)
                logging.debug(f"[move] 源文件夹已清空，已删除：{source}")
            except OSError:
                logging.debug(f"[move] 源文件夹未完全清空，未删除：{source}")
    else:
        logging.info(f"[move] 移动文件夹功能已禁用：{source} -> {target}")
