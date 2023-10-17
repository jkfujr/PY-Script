import os
import sys


file_path = sys.argv[1]

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
    "msbsqn": "结-Official",
    "kaguramea_vov": "神楽Mea_Official"
}

# 遍历文件夹字典，进行重命名操作
for old_folder, new_name in folders.items():
    old_path = os.path.join(file_path, old_folder)
    new_path = os.path.join(file_path, new_name)

    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"[Info] 重命名文件夹 {old_folder} -> {new_name}")
    # else:
    #     print(f"文件夹 {old_folder} 不存在")

print("")
print("[Info] 已完成 所有文件夹 重命名操作")
