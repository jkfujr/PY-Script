from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import re
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
        # 计算时间差并取绝对值
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
    user_folders = os.listdir(path)

    for user_folder in user_folders:
        if user_folder not in excluded_folders:
            user_folder_path = os.path.join(path, user_folder)
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
    # 获取路径，默认为 "F:\Video\录播\综合"
    path = request.query_params.get("path", "F:\Video\录播\综合")

    # 生成表格数据
    table_data = generate_table_data(path)

    # 返回带有表格数据的 HTML 模板响应
    return templates.TemplateResponse("index.html", {"request": request, "table_data": table_data})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5888)
