import os
import logging
import aiomysql
import uvicorn
import asyncio
from logging.handlers import TimedRotatingFileHandler
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from datetime import datetime

# 日志配置
# 确保日志目录存在
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志文件路径
log_file_path = os.path.join(log_dir, "log_{0}.log".format(datetime.now().strftime("%Y-%m-%d")))

# 创建日志记录器
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# 创建一个每天轮转的文件处理器，保留30天
handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=30, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# 合并日志与打印信息
def log_and_print(message, prefix="", level="INFO"):
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    # 日志
    logger = logging.getLogger()
    logger.log(level, message)
    # 打印
    print(prefix + message)


# 消息模型
class Message(BaseModel):
    from_: str
    title: str
    org_content: str
    receive_time: str

# 全局变量
message_buffer = []
db_connected = False
db_pool = None

async def connect_to_db():
    global db_connected
    while True:
        try:
            db_pool = await aiomysql.create_pool(
                host="10.0.0.111",
                port=3306,
                user="sms",
                password="gy6S*NPYNpki9TP5",
                db="sms",
                charset="utf8mb4",
                minsize=5,
                maxsize=10,
            )
            log_and_print("成功连接到数据库.", "INFO:     ", "INFO")
            db_connected = True
            return db_pool
        except Exception as e:
            log_and_print(f"连接数据库失败: {e}, 将在10秒后重试...", "ERROR:     ", "ERROR")
            db_connected = False
            await asyncio.sleep(10)

async def initialize():
    global db_pool
    db_pool = await connect_to_db()

async def shutdown():
    global db_pool
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()

async def get_connection():
    async with db_pool.acquire() as conn:
        yield conn

async def write_to_db():
    global message_buffer, db_connected
    while True:
        if message_buffer and db_connected:
            try:
                async with db_pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        for message in message_buffer:
                            sql = "INSERT INTO messages (`from`, `title`, `org_content`, `receive_time`) VALUES (%s, %s, %s, %s)"
                            await cursor.execute(sql, (message.from_, message.title, message.org_content, message.receive_time))
                            await conn.commit()
                        log_and_print("信息写入成功.", "INFO:     ", "INFO")
                message_buffer = []
            except Exception as e:
                log_and_print(f"数据库操作异常: {e}", "ERROR:     ", "ERROR")
        elif not db_connected:
            log_and_print(f"数据库未连接，暂存消息，等待数据库连接恢复...", "WARNING:     ", "WARNING")
        await asyncio.sleep(3)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await initialize()
    asyncio.create_task(write_to_db())

@app.on_event("shutdown")
async def shutdown_event():
    await shutdown()

@app.put("/webhook")
async def handle_webhook(message: Message):
    global message_buffer, db_connected
    message.receive_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_buffer.append(message)
    log_and_print(f"接收到新消息：{message.dict()}", "INFO:     ", "INFO")

# 应用启动入口
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, lifespan="on")
