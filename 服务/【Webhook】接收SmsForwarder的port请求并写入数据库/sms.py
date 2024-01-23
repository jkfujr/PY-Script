import os
import logging
from logging.handlers import TimedRotatingFileHandler
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
import aiomysql
import uvicorn
from pydantic import BaseModel
from datetime import datetime


# 日志配置
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(
    log_dir, "log_{0}.log".format(datetime.now().strftime("%Y-%m-%d"))
)

# 配置日志记录器
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

# 文件处理器 - 每天分割日志，保留 30 天
file_handler = TimedRotatingFileHandler(
    log_file_path, when="midnight", interval=1, backupCount=30, encoding="utf-8"
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(file_formatter)
logger.addHandler(console_handler)


# 消息模型
class Message(BaseModel):
    from_: str
    title: str
    org_content: str
    receive_time: str


db_pool = None

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool
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
    yield
    db_pool.close()
    await db_pool.wait_closed()


app = FastAPI(lifespan=lifespan)


async def get_connection():
    async with db_pool.acquire() as conn:
        yield conn


@app.put("/webhook")
async def handle_webhook(
    message: Message, conn: aiomysql.Connection = Depends(get_connection)
):
    logger.debug("处理新消息")
    message.receive_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"消息接收时间: {message.receive_time}")

    try:
        logger.debug("连接数据库")
        async with conn.cursor() as cursor:
            sql = "INSERT INTO messages (`from`, `title`, `org_content`, `receive_time`) VALUES (%s, %s, %s, %s)"
            await cursor.execute(
                sql,
                (
                    message.from_,
                    message.title,
                    message.org_content,
                    message.receive_time,
                ),
            )
            await conn.commit()
            logger.info(
                f"写入数据库成功：{message.dict() if hasattr(message, 'dict') else message.model_dump()}"
            )
    except Exception as e:
        logger.error(f"数据库操作异常: {e}")


# 应用启动入口
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
