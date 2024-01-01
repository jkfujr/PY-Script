import os
import subprocess
import time

# 获取脚本所在的路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 录播路径
file_path = r"F:\Video\TCCCCCCCCC"

# 重命名指定的文件夹名
run_file_rename = True
# 重命名弹幕与录播文件的文件名 格式为 "年月日-时分秒_标题"
run_file_rename_rec = True
# 在路径下的文件夹内新建 "twitcasting" 子文件夹，并移动所有文件(不包括文件夹)到 "twitcasting" 子文件夹内
run_file_move = True
# 弹幕格式修正 (建议开)
run_danmaku_corr = True
# 转换弹幕为录播姬弹幕xml样式 (依赖弹幕格式修正)
run_danmaku_txt_to_xml = True


def execute(script_path, variable, script_name):
    try:
        print("")
        print("==========")
        print(f"[Info] 开始执行脚本：{script_name}")
        print("==========")
        print("")
        subprocess.run(["python", script_path, variable])
    except Exception as e:
        print(f"[Error] 执行脚本 {script_name} 时出错: {e}")

# 根据开关决定是否执行
if run_file_rename:
    execute(os.path.join(script_dir, "core", "file_rename.py"), file_path, "重命名指定的文件夹名")
    time.sleep(1)

if run_file_rename_rec:
    execute(os.path.join(script_dir, "core", "file_rename_rec.py"), file_path, "重命名弹幕与录播文件名")
    time.sleep(1)

if run_file_move:
    execute(os.path.join(script_dir, "core", "file_move.py"), file_path, "移动弹幕与录播文件")
    time.sleep(1)

if run_danmaku_corr:
    execute(os.path.join(script_dir, "core", "danmaku_corr.py"), file_path, "弹幕修正")
    time.sleep(1)

if run_danmaku_txt_to_xml:
    execute(os.path.join(script_dir, "core", "danmaku_txt_to_xml.py"), file_path, "txt弹幕转xml弹幕")
    time.sleep(1)
