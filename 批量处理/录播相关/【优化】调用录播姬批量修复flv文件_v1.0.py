import os
import subprocess
from tqdm import tqdm

# 录播路径
input_dir = r"F:\新建文件夹"
# 输出路径
output_dir = r"F:\A"
# 录播姬路径
recheme_dir = r"C:\BililiveRecorder-CLI-win-x64"

# 遍历录播路径的flv文件
file_list = [filename for filename in os.listdir(input_dir) if filename.endswith(".flv")]
total_files = len(file_list)

# 检查输出路径
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 进度条
with tqdm(total=total_files, desc="Fixing files") as pbar:
    for filename in file_list:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        output_base = os.path.splitext(output_path)[0]
        
        # 构造fix命令
        cmd = [os.path.join(recheme_dir, "BililiveRecorder.Cli.exe"), "tool", "fix", input_path, output_base]
        
        # 调用fix命令
        subprocess.run(cmd, shell=True)
        
        # 更新进度条
        pbar.update(1)

print("全部执行完成，按回车退出.")
input()
