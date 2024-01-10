# core/move.py

import os
import shutil
import logging

def move_folder(source, target, enable_move=True):
    if enable_move:
        if not os.path.exists(target):
            logging.info(f"移动文件夹：{source} -> {target}")
            shutil.move(source, target)
        else:
            logging.info(f"目标文件夹已存在，合并内容：{source} -> {target}")
            for item in os.listdir(source):
                source_item_path = os.path.join(source, item)
                target_item_path = os.path.join(target, item)
                if os.path.exists(target_item_path):
                    logging.info(f"目标位置已存在同名项，跳过：{target_item_path}")
                    continue
                logging.info(f"移动项：{source_item_path} -> {target_item_path}")
                shutil.move(source_item_path, target_item_path)
            try:
                os.rmdir(source)
                logging.info(f"源文件夹已清空，已删除：{source}")
            except OSError:
                logging.info(f"源文件夹未完全清空，未删除：{source}")
    else:
        logging.info(f"移动文件夹功能已禁用：{source} -> {target}")
