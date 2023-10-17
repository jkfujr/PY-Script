import os
import re
import shutil

# 指定视频文件所在的路径
video_directory = r"F:\Video\Twitch"

def rename_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".ts") or filename.endswith(".mp4"):
            old_filepath = os.path.join(directory, filename)
            match = re.search(r"\[(\d{4})\.(\d{2})\.(\d{2}) (\d{2})\.(\d{2})\.(\d{2})\]\[(.*?)\]\[(.*?)\](.*?)\.(ts|mp4)", filename)
            if match:
                year = match.group(1)
                month = match.group(2)
                day = match.group(3)
                hour = match.group(4)
                minute = match.group(5)
                second = match.group(6)
                platform = match.group(7)
                streamer_id = match.group(8)
                title = match.group(9)
                extension = match.group(10)

                new_filename = f"{year}{month}{day}-{hour}{minute}{second}_{title}.{extension}"
                new_subdirectory = os.path.join(directory, streamer_id, platform)
                new_filepath = os.path.join(new_subdirectory, new_filename)

                os.makedirs(new_subdirectory, exist_ok=True)
                shutil.move(old_filepath, new_filepath)
                print(f"重命名 '{filename}' -> '{new_filename}' 并移动到 '{new_subdirectory}'.")

# 执行文件重命名和移动操作
rename_files(video_directory)