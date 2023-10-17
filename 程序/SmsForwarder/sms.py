from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from datetime import datetime

app = FastAPI()


class Message(BaseModel):
    # 来源手机号 / App包名
    from_: str
    # APP通知的标题
    title: str
    # 短信 / 通知 原始内容
    org_content: str
    # 短信/来电/APP通知的接收时间
    receive_time: str


@app.put("/webhook")
async def handle_webhook(message: Message):
    message.receive_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with mysql.connector.connect(
        host="10.0.0.111",
        port='3306',
        user="sms",
        password="gy6S*NPYNpki9TP5",
        database="sms",
        charset="utf8mb4"
    ) as connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO messages ( `from`, `title`, `org_content`, `receive_time`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (message.from_,
                                message.title,
                                message.org_content,
                                message.receive_time)
                        )
            connection.commit()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)