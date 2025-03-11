import os
import subprocess
from tqdm import tqdm

def fix_file(input_path, output_base, recheme_dir):
    cmd = [os.path.join(recheme_dir, "BililiveRecorder.Cli.exe"), "tool", "fix", input_path, output_base]
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error fixing {input_path}: {e}")

def main():
    input_dir = r"E:\录播\美波七海-official\整理"
    output_dir = r"E:\录播\美波七海-official\整理\修复"
    recheme_dir = r"C:\jkfujr\Server\LiveRec\BililiveRecorder\9001_综合-01"

    file_list = [filename for filename in os.listdir(input_dir) if filename.endswith(".flv")]
    total_files = len(file_list)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with tqdm(total=total_files, desc="Fixing files") as pbar:
        for filename in file_list:
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            output_base = os.path.splitext(output_path)[0]
            
            print(f"开始修复: {filename}")
            fix_file(input_path, output_base, recheme_dir)
            pbar.update(1)

    print("全部执行完成，按回车退出.")
    input()

if __name__ == "__main__":
    main()
