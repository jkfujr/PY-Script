import os
import logging
import aiomysql
import uvicorn
import asyncio
import httpx
import yaml
from logging.handlers import TimedRotatingFileHandler
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from contextlib import asynccontextmanager

# 获取目录
script_directory = os.path.dirname(os.path.abspath(__file__))

# 读取配置
config_path = os.path.join(script_directory, "config.yaml")
with open(config_path, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

HOST = config.get('HOST', '0.0.0.0')
PORT = config.get('PORT', 8000)

DB_CONFIG = config.get('DB', {})
GOTIFY_CONFIG = config.get('Gotify', {})

### 日志模块
def log():
    global logger
    if logging.getLogger().handlers:
        return logging.getLogger()

    # 获取目录
    log_directory = os.path.join(script_directory, "logs")
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # 日志格式
    log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(processName)s - %(message)s"
    )

    # 日志名称和后缀
    default_log_file_name = "sms"
    log_file_path = os.path.join(log_directory, default_log_file_name)

    # 创建日志文件处理器,每天分割日志文件
    log_file_handler = TimedRotatingFileHandler(
        log_file_path,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    log_file_handler.suffix = "%Y-%m-%d.log"
    log_file_handler.setFormatter(log_formatter)

    # 创建并配置 logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_file_handler)

    return logger

logger = log()

# 合并日志与打印信息
def log_print(message, prefix="", level="INFO"):
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    # 日志
    logger = logging.getLogger()
    logger.log(level, message)
    # 打印
    print(prefix + message)

# 信息模型
class Message(BaseModel):
    from_: str
    title: str
    org_content: str
    receive_time: str

# 全局变量
message_buffer = []
db_pool = None

### Gotify推送
async def push_gotify(title, org_content):
    if not GOTIFY_CONFIG.get('ENABLE', False):
        log_print("[Gotify] 推送未启用", "INFO:     ", "INFO")
        return

    max_retries = GOTIFY_CONFIG.get('MAX-TRY', 3)
    retry_delay = 3
    servers = GOTIFY_CONFIG.get('SERVER', {})

    async def push_to_server(server_name, server_config):
        url = f"{server_config['url']}/message?token={server_config['token']}"
        priority = server_config.get('priority', 5)
        payload = {
            "message": org_content,
            "priority": priority,
            "title": title
        }

        async with httpx.AsyncClient(verify=False) as client:
            for attempt in range(1, max_retries + 1):
                try:
                    resp = await client.post(url, json=payload)
                    if resp.status_code == 200:
                        log_print(f"[Gotify {server_name}] 信息推送成功", "INFO:     ", "INFO")
                        break
                    else:
                        log_print(f"[Gotify {server_name}] 信息推送失败，状态码：{resp.status_code}，重试次数：{attempt}/{max_retries}", "ERROR:     ", "ERROR")
                except Exception as e:
                    log_print(f"[Gotify {server_name}] 信息推送异常：{e}，重试次数：{attempt}/{max_retries}", "ERROR:     ", "ERROR")
                await asyncio.sleep(retry_delay)
            else:
                log_print(f"[Gotify {server_name}] 信息推送失败：达到最大重试次数 {max_retries} 次", "ERROR:     ", "ERROR")

    # 创建任务列表
    tasks = [push_to_server(server_name, server_config) for server_name, server_config in servers.items()]
    # 并发执行任务
    await asyncio.gather(*tasks)

### 数据库连接
async def db_connect():
    global db_pool
    if not DB_CONFIG.get('ENABLE', False):
        log_print("[DB] 数据库未启用", "INFO:     ", "INFO")
        return

    try:
        db_pool = await aiomysql.create_pool(
            host=DB_CONFIG['HOST'],
            port=DB_CONFIG['PORT'],
            user=DB_CONFIG['DBUSER'],
            password=DB_CONFIG['DBPASS'],
            db=DB_CONFIG['DBNAME'],
            charset=DB_CONFIG.get('DBCHARSET', 'utf8mb4'),
            minsize=5,
            maxsize=10,
        )
        log_print("[DB] 成功连接到数据库.", "INFO:     ", "INFO")
    except Exception as e:
        log_print(f"[DB] 连接数据库失败: {e}, 将在10秒后重试...", "ERROR:     ", "ERROR")
        await asyncio.sleep(10)

### 初始化和关闭
async def initialize():
    await db_connect()

async def shutdown():
    global db_pool
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()

### 测试数据库连接
async def db_test():
    global db_pool
    while True:
        try:
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT 1")
                    result = await cursor.fetchone()
                    if result and result[0] == 1:
                        logger.debug(f"[DB-检查] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 数据库连接正常.")
                    else:
                        log_print("[DB-检查] 数据库连接异常.", "ERROR:     ", "ERROR")
                        raise Exception("Database connection failed")
            await asyncio.sleep(600)
        except Exception as e:
            log_print(f"[DB-检查] 数据库连接异常: {e}, 将在10秒后重试...", "ERROR:     ", "ERROR")
            await asyncio.sleep(10)

### 写入数据库
async def db_write():
    global message_buffer, db_pool
    while True:
        if message_buffer:
            if db_pool:
                try:
                    async with db_pool.acquire() as conn:
                        async with conn.cursor() as cursor:
                            for message in message_buffer:
                                sql = "INSERT INTO messages (`from`, `title`, `org_content`, `receive_time`) VALUES (%s, %s, %s, %s)"
                                await cursor.execute(sql, (message.from_, message.title, message.org_content, message.receive_time))
                            await conn.commit()
                        log_print("[DB] 信息写入成功.", "INFO:     ", "INFO")
                    message_buffer = []
                except Exception as e:
                    log_print(f"[DB] 数据库操作异常: {e}", "ERROR:     ", "ERROR")
            else:
                log_print("[DB] 数据库未连接，等待连接...", "WARNING:     ", "WARNING")
        await asyncio.sleep(3)

### FastAPI应用
@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize()
    if DB_CONFIG.get('ENABLE', False):
        asyncio.create_task(db_test())
        asyncio.create_task(db_write())
    yield
    await shutdown()

app = FastAPI(lifespan=lifespan)

### Webhook处理
@app.put("/webhook")
async def handle_webhook(message: Message):
    global message_buffer
    message.receive_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_buffer.append(message)
    log_print(f"接收到新信息：{message.dict()}", "INFO:     ", "INFO")

    asyncio.create_task(push_gotify(message.title, message.org_content))

### 应用启动入口
if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
