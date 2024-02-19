import os
import logging
from datetime import datetime

# 录播姬处理
from core.recheme import recheme_main

# blrec处理
from core.blrec import blrec_main

### 日志模块
# 日志文件夹路径和日志文件名
log_folder = "logs"
log_filename = datetime.now().strftime("%Y%m%d-%H%M%S.log")
log_file_path = os.path.join(os.path.dirname(__file__), log_folder, log_filename)

# 确保日志文件夹存在
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# 创建日志记录器
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# 创建文件处理器并设置级别为DEBUG
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

# 创建控制台处理器并设置级别为INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

### 设定
# (全局)是否启用移动文件夹
enable_move = True

# (全局)执行路径
folder_path_id = {
    "AAA": {"source": r"F:\Video\AAAAAAAAAA", "target": r"F:\Video\AAAAAAAAAA\000"},
    "PPP": {"source": r"F:\Video\PPPPPPPPPP", "target": r"F:\Video\PPPPPPPPPP\000"},
    "TEST": {"source": r"F:\测试数据", "target": r"F:\测试数据\000"},
}

# (全局)社团文件夹名称列表
social_folders = ["NIJISANJI", "HOLOLIVE", "VSPO"]

# (全局)需要跳过的特殊文件夹名称列表
skip_folders = ["000", "111"]

# (录播姬)需要跳过的录播子文件夹
recheme_skip_substrings = ["【blrec-flv】", "【blrec-hls】", "000_部分丢失", "1970"]


# blrec
logging.info("[BLREC] 开始处理")
blrec_main(folder_path_id, enable_move, social_folders, skip_folders)
logging.info("[BLREC] 处理完成")

# 录播姬
logging.info("[录播姬] 开始处理")
recheme_main(folder_path_id, enable_move, social_folders, skip_folders, recheme_skip_substrings)
logging.info("[录播姬] 处理完成")
