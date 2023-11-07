import os
import shutil


# 读取环境变量中的路径
script_path = os.environ.get("SCRIPT_PATH")


# 定义要重命名的文件夹和对应的新名称
folders = {
    "nakonekonako_21": "ナコ",
    "maru0maru02": "まる",
    "kurusu72me": "来栖夏芽",
    "merrysan_cas_": "merry_official",
    "mi_tagun": "みぃ太軍_Office",
    "mmos3535": "さぶすも",
    "mojibake55": "mojibake55",
    "mrin_portract": "みのりん",
    "cxxronixx": "心羽萝妮Official",
    "sara_hoshikawa": "星川莎拉_Official",
    "morinaga_miu": "森永みうofficial",
    "373staff": "美波",
    "ao_za4": "青刺める",
    "miso_ssw": "miso",
    "russyotter": "ろし",
    "tama10xx": "たま",
    "ychun_pg": "ゆゆ",
    "msbsqn": "结-Official"
}

# 获取当前目录
current_dir = os.getcwd()


def process_files():
    for old_name, new_name in folders.items():
        old_folder_path = os.path.join(script_path, old_name)
        new_folder_path = os.path.join(script_path, new_name)

        # 检查文件夹是否存在
        if os.path.exists(old_folder_path):
            os.rename(old_folder_path, new_folder_path)

            # 创建子文件夹
            subfolder_path = os.path.join(new_folder_path, "twitcasting")
            os.makedirs(subfolder_path)

            # 移动文件到子文件夹
            folder_contents = os.listdir(new_folder_path)
            for item in folder_contents:
                item_path = os.path.join(new_folder_path, item)
                if os.path.isfile(item_path):
                    shutil.move(item_path, subfolder_path)

            print(f"[Info] 重命名和移动完成: {old_name} -> {new_name}")
        # else:
        #     print(f"[Info] 文件夹不存在: {old_name} 跳过")

    print("[Info] 所有文件夹处理完成!")


process_files()