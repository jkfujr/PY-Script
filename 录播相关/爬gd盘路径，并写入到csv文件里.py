import os
import csv

# 获取执行脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, 'directory_structure.csv')

# 定义遍历函数
def traverse_directory(path, file_writer):
    for root, dirs, files in os.walk(path):
        for name in dirs:
            # 拼接完整路径
            full_path = os.path.join(root, name)
            # 分割路径并获取第6层级的文件夹名
            path_parts = full_path.split(os.path.sep)
            folder_name = path_parts[5] if len(path_parts) > 5 else 'null'
            # 写入 CSV 文件
            file_writer.writerow([full_path, folder_name])

# 打开 CSV 文件并写入数据
with open(csv_file_path, mode='w', encoding='utf-8', newline='') as file:
    file_writer = csv.writer(file)
    # 写入表头
    file_writer.writerow(['Full Path', '6th-level Folder Name'])
    # 调用遍历函数
    traverse_directory(r'G:\共享云端硬盘\vtbrecorder1-old4\recroot', file_writer)
