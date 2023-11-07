import os
import re
import sys


file_path = sys.argv[1]

# 从文本文件中读取时间和标题信息
def read_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    time_str = re.findall(r"\d+年\d+月\d+日\d+時\d+分\d+秒", lines[1])[0]
    title_line = lines[4]
    if title_line.strip() == "【タイトル】":
        title = "NULL"
    else:
        title = re.findall(r"【タイトル】(.+)", title_line)[0].strip()
    return time_str, title

# 重命名文件
def rename_file(old_path, new_filename):
    new_path = os.path.join(os.path.dirname(old_path), new_filename)
    os.rename(old_path, new_path)
    print(f"[Info] 重命名文件：{old_path} -> {new_path}")

# 遍历文件夹，处理符合条件的文件
def traverse_folder(file_path):
    result = []

    for foldername, subfolders, filenames in os.walk(file_path):
        for filename in filenames:
            if filename.endswith(".txt"):
                txt_path = os.path.join(foldername, filename)
                ts_path = txt_path[:-3] + "ts"

                try:
                    time_str, title = read_txt(txt_path)
                    new_filename = (
                        time_str.replace("年", "")
                        .replace("月", "")
                        .replace("日", "-")
                        .replace("時", "")
                        .replace("分", "")
                        .replace("秒", "")
                        + "_"
                        + title
                        + ".txt"
                    )
                    rename_file(txt_path, new_filename)

                    if os.path.exists(ts_path):
                        new_ts_filename = new_filename[:-4] + ".ts"
                        rename_file(ts_path, new_ts_filename)
                except Exception as e:
                    print("[Error]", str(e), "跳过:", txt_path)
                    continue

                result.append({
                    "txt_path": os.path.join(foldername, new_filename),
                    "ts_path": os.path.join(foldername, new_ts_filename) if os.path.exists(ts_path) else "",
                    "start_time": time_str,
                    "title": title,
                })

    print("")
    print("[Info] 已完成 所有弹幕与录播文件 重命名操作")
    return result

if __name__ == "__main__":
    result = traverse_folder(file_path)
