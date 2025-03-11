import os
import re
import shutil
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta

app = FastAPI()

templates = Jinja2Templates(directory=".")

def extract_datetime_from_folder_name(folder_name):
    pattern = r"(\d{8}-\d{6})"
    match = re.search(pattern, folder_name)
    
    if match:
        datetime_str = match.group(1)
        return datetime.strptime(datetime_str, "%Y%m%d-%H%M%S")
    else:
        return None

def calculate_time_difference(folder_name, earliest_flv_datetime):
    folder_datetime = extract_datetime_from_folder_name(folder_name)
    if folder_datetime:
        time_difference = abs(folder_datetime - earliest_flv_datetime)
        return time_difference
    else:
        return None

def process_sub_folder(sub_folder_path, earliest_flv_datetime):
    flv_files = [file for file in os.listdir(sub_folder_path) if file.lower().endswith(".flv")]
    if not flv_files:
        return None

    earliest_flv_file = min(flv_files)
    earliest_flv_datetime = extract_datetime_from_folder_name(earliest_flv_file)
    if not earliest_flv_datetime:
        return None

    sub_folder_name = os.path.basename(sub_folder_path)
    time_difference = calculate_time_difference(sub_folder_name, earliest_flv_datetime)
    return time_difference

def generate_table_data(path):
    table_data = []
    excluded_folders = ["000", "CCC"]
    
    path = path.replace('\x00', '')
    if not os.path.exists(path):
        return table_data

    user_folders = os.listdir(path)
    for user_folder in user_folders:
        if user_folder not in excluded_folders:
            user_folder_path = os.path.join(path, user_folder)
            if not os.path.isdir(user_folder_path):
                continue
            
            sub_folders = os.listdir(user_folder_path)
            for sub_folder in sub_folders:
                sub_folder_path = os.path.join(user_folder_path, sub_folder)
                if os.path.isdir(sub_folder_path):
                    time_difference = process_sub_folder(sub_folder_path, datetime.max)
                    if time_difference is not None:
                        table_data.append((user_folder, sub_folder, str(time_difference)))

    return table_data

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    path = request.query_params.get("path", r"F:\Video\AAAAAAAAAA\000")
    table_data = generate_table_data(path)
    return templates.TemplateResponse("index.html", {"request": request, "table_data": table_data, "path": path})

@app.post("/move_folders")
def move_folders(path: str = Form(...), time_diff: str = Form(...), user_id: str = Form(None), folder_name: str = Form(None)):
    """
    根据请求参数处理文件夹移动。
    如果提供了user_id和folder_name，则只移动指定的文件夹；
    否则按照原来的逻辑移动所有超过时间差的文件夹。
    """
    time_diff_parts = time_diff.split(":")
    time_diff_td = timedelta(minutes=int(time_diff_parts[0]), seconds=int(time_diff_parts[1]))

    path = path.replace('\x00', '')
    if not os.path.exists(path):
        return JSONResponse(content={"message": "路径不存在"}, status_code=400)

    moved_folders = []
    skipped_folders = []  # 存储被跳过的文件夹

    if user_id and folder_name:
        # 处理指定的文件夹
        sub_folder_path = os.path.join(path, user_id, folder_name)
        if os.path.exists(sub_folder_path):
            target_folder = os.path.join(path, user_id, "000_部分丢失")
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            destination_path = os.path.join(target_folder, folder_name)
            try:
                shutil.move(sub_folder_path, destination_path)
                moved_folders.append(folder_name)
            except shutil.Error as e:
                # 处理目标路径已存在的异常
                skipped_folders.append(destination_path)
                print(f"目标路径已存在，跳过移动: {destination_path}")
    else:
        # 处理所有符合条件的文件夹
        user_folders = os.listdir(path)
        for user_folder in user_folders:
            user_folder_path = os.path.join(path, user_folder)
            if not os.path.isdir(user_folder_path) or user_folder in ["000", "CCC"]:
                continue

            sub_folders = os.listdir(user_folder_path)
            for sub_folder in sub_folders:
                sub_folder_path = os.path.join(user_folder_path, sub_folder)
                if os.path.isdir(sub_folder_path):
                    time_difference = process_sub_folder(sub_folder_path, datetime.max)
                    if time_difference is not None and time_difference > time_diff_td:
                        target_folder = os.path.join(user_folder_path, "000_部分丢失")
                        if not os.path.exists(target_folder):
                            os.makedirs(target_folder)
                        destination_path = os.path.join(target_folder, sub_folder)
                        try:
                            shutil.move(sub_folder_path, destination_path)
                            moved_folders.append(sub_folder)
                        except shutil.Error as e:
                            # 处理目标路径已存在的异常
                            skipped_folders.append(destination_path)
                            print(f"目标路径已存在，跳过移动: {destination_path}")

    # 返回移动和跳过的文件夹信息
    return JSONResponse(content={"message": f"移动了 {len(moved_folders)} 个文件夹，跳过了 {len(skipped_folders)} 个文件夹", "skipped_folders": skipped_folders}, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=19002)
