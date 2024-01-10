# run.py
import os
import logging
from datetime import datetime
from core.recheme import merge_folders, process_user_folder, process_merge_logic, process_all_folders


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
# (全局)是否启用移动文件夹
enable_move = True

# 执行路径
folder_path_id = {
    "AAA": {"source": r"F:\Video\AAAAAAAAAA", "target": r"F:\Video\AAAAAAAAAA\000"},
    "PPP": {"source": r"F:\Video\PPPPPPPPPP", "target": r"F:\Video\PPPPPPPPPP\000"},
    "TEST": {"source": r"F:\测试数据"},
}

# 社团文件夹名称列表
social_folders = ["NIJISANJI", "HOLOLIVE", "VSPO"]

# 需要跳过的特殊文件夹名称列表
skip_folders = ["000", "111"]

# 录播姬_需要跳过的录播子文件夹
recheme_skip_substrings = ["【blrec-flv】", "【blrec-hls】", "000_部分丢失"]

# 使用导入的函数
process_all_folders(folder_path_id, enable_move, social_folders, skip_folders, recheme_skip_substrings)