#!/bin/bash

# 设置源目录和目标目录
SOURCE_DIR="/home/录播文件/"
DESTINATION_DIR="/onedrive/录播/"

# 获取当前时间
CURRENT_TIME=$(date +%Y%m%d-%H%M%S)
LOG_FOLDER="logs"
LOG_FILE="$LOG_FOLDER/$CURRENT_TIME.log"

# 创建日志文件夹（如果不存在）
mkdir -p "$LOG_FOLDER"

# 重定向标准输出和标准错误到日志文件
exec > >(tee -a "$LOG_FILE")
exec 2>&1

echo "[Info] 脚本执行开始于：$(date)"

# 获取三天前的日期
THREE_DAYS_AGO=$(date -d "3 days ago" +%Y%m%d)

# 获取要处理的文件夹总数
total_dirs=$(find "$SOURCE_DIR" -type d | wc -l)

# 初始化计数器和速度记录
counter=0
total_size=0
start_time=$(date +%s)

# 遍历源目录下的所有子目录
find "$SOURCE_DIR" -type d | while read -r dir; do
    # 检查是否是youtube录播文件夹
    if [[ $dir =~ /youtube/.* ]]; then
        # 获取文件夹名称
        folder_name=$(basename "$dir")
        # 检查是否符合年月日_标题的命名规则
        if [[ $folder_name =~ ^[0-9]{8}_ ]]; then
            # 提取文件夹中的日期部分
            folder_date=${folder_name:0:8}
            # 检查日期是否是三天前
            if [[ $folder_date -lt $THREE_DAYS_AGO ]]; then
                # 构建目标路径，保留文件夹结构
                target_path="$DESTINATION_DIR$(dirname "${dir//$SOURCE_DIR/}")"
                # 获取文件夹大小
                folder_size=$(du -sb "$dir" | awk '{print $1}')
                total_size=$((total_size + folder_size))
                # 打印移动前的文件夹名
                echo "[Info] 准备移动文件夹：$dir 到 $target_path"
                # 移动前增加计数器
                ((counter++))
                # 打印进度条
                echo -ne "[Info] 进度：[$counter/$total_dirs] ($(bc <<< "scale=2; ($counter/$total_dirs)*100")%) \r"
                # 执行移动操作，保留文件夹结构
                if ! rclone move "$dir" "$target_path/$folder_name"; then
                    echo "[Error] 移动失败：$dir"
                    continue
                fi
                # 清除进度条
                echo -ne "\033[K"
                # 计算移动时间
                end_time=$(date +%s)
                elapsed_time=$((end_time - start_time))
                # 计算移动速度
                speed=$(bc <<< "scale=2; $total_size / $elapsed_time / 1024 / 1024")
                echo "[Info] 移动速度：$speed MB/s"
            fi
        fi
    elif [[ $dir =~ /Twitch/.* ]]; then
        # 获取文件夹名称
        folder_name=$(basename "$dir")
        # 提取文件夹中的日期部分
        folder_date=$(echo "$folder_name" | grep -oP '\[\K[0-9.]+(?=\])')
        if [[ -n $folder_date ]]; then
            # 将日期格式转换为年月日形式
            folder_date=$(date -d "$folder_date" +%Y%m%d)
            # 检查日期是否是三天前
            if [[ $folder_date -lt $THREE_DAYS_AGO ]]; then
                # 构建目标路径，保留文件夹结构
                target_path="$DESTINATION_DIR$(dirname "${dir//$SOURCE_DIR/}")"
                # 获取文件夹大小
                folder_size=$(du -sb "$dir" | awk '{print $1}')
                total_size=$((total_size + folder_size))
                # 打印移动前的文件夹名
                echo "[Info] 准备移动文件夹：$dir 到 $target_path"
                # 移动前增加计数器
                ((counter++))
                # 打印进度条
                echo -ne "[Info] 进度：[$counter/$total_dirs] ($(bc <<< "scale=2; ($counter/$total_dirs)*100")%) \r"
                # 执行移动操作，保留文件夹结构
                if ! rclone move "$dir" "$target_path/$folder_name"; then
                    echo "[Error] 移动失败：$dir"
                    continue
                fi
                # 清除进度条
                echo -ne "\033[K"
                # 计算移动时间
                end_time=$(date +%s)
                elapsed_time=$((end_time - start_time))
                # 计算移动速度
                speed=$(bc <<< "scale=2; $total_size / $elapsed_time / 1024 / 1024")
                echo "[Info] 移动速度：$speed MB/s"
            fi
        fi
    fi
done

echo "[Info] 移动完成。"

# 在所有移动完成后，检查目标目录并删除空文件夹
echo "[Info] 正在清理空文件夹..."
find "$DESTINATION_DIR" -type d -empty -path "$DESTINATION_DIR/*/youtube/*" -delete
echo "[Info] 清理完成。"


echo "[Info] 脚本执行结束于：$(date)"