import os
import logging
from datetime import datetime

# 录播姬处理
from core.recheme import recheme_main

# blrec处理
from core.blrec import blrec_main


### 设定
# (全局)是否启用移动文件夹
enable_move = True

# (全局)执行路径
folder_path_id = {
    "AAA": {"source": r"F:\Video\AAAAAAAAAA", "target": r"F:\Video\AAAAAAAAAA\000"},
    "PPP": {"source": r"F:\Video\PPPPPPPPPP", "target": r"F:\Video\PPPPPPPPPP\000"},
    # "TEST": {"source": r"F:\测试数据", "target": r"F:\测试数据\000"},
}

# (全局)社团文件夹名称列表
social_folders = ["NIJISANJI", "HOLOLIVE", "VSPO"]

# (全局)需要跳过的特殊文件夹名称列表
skip_folders = ["000", "111", "222", "333", "444"]

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
