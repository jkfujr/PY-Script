import os
import re
import sys


file_path = sys.argv[1]


def fix_danmaku_format(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.readlines()

    # 跳过前五行
    header = content[:5]
    danmaku_content = "".join(content[5:])

    # 使用正则分割弹幕
    danmaku_pattern = re.compile(
        r"\[\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}\] .*?（.*?）"
    )
    danmaku_list = danmaku_pattern.findall(danmaku_content)

    # 判断是否需要修正
    if danmaku_list:
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(header)
            file.write("\n".join(danmaku_list))

        print(f"[Info] 修正文件：{file_path}")
    else:
        print(f"[Info] 无需修正：{file_path}")


# 遍历所有txt文件并修正
for root, dirs, files in os.walk(file_path):
    for file in files:
        if file.endswith(".txt"):
            file_path = os.path.join(root, file)
            fix_danmaku_format(file_path)

print("")
print("[Info] 已完成 所有弹幕文件 修正操作")
