# 【Webhook】接收SmsForwarder的port请求并写入数据库

## 功能
* 启动Webhook服务接收SmsForwarder的port请求并写入数据库

## 使用
1. 打开 `sms.py` 修改数据库配置
2. 启动脚本 `py sms.py`
3. 打开 `SmsForwarder` APP，建立一个port请求的webhook服务，数据模板使用下面的
4. 建立转发规则

## SmsForwarder模板
```
{"from_":"[from]","title":"[title]", "org_content":"[org_content]","receive_time":"[receive_time]"}
```