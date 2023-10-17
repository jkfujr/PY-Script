import os
import re
from datetime import datetime
import html
import sys


file_path = sys.argv[1]


# 定义弹幕时间的正则
time_pattern = re.compile(
    r"\[(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})\]\s(.+?)\（(.+?)\）"
)


def process_folder(file_path):
    for entry in os.listdir(file_path):
        entry_path = os.path.join(file_path, entry)

        if os.path.isdir(entry_path):
            process_folder(entry_path)
        elif entry_path.endswith(".txt"):
            generate_xml_from_txt(entry_path)


def generate_xml_from_txt(txt_file_path):
    # 检查同名的.xml文件是否已存在，如果存在则跳过
    xml_file_path = os.path.splitext(txt_file_path)[0] + ".xml"
    if os.path.exists(xml_file_path):
        print(f"[Info] 跳过 {txt_file_path}，因为已存在同名的xml文件")
        return

    with open(txt_file_path, "r", encoding="utf-8") as txt_file:
        lines = txt_file.readlines()

    # 提取前 5 行数据
    live_url = lines[0].strip().split("】")[1]
    start_time_str = lines[1].strip().split("】")[1]
    user_name = lines[2].strip().split("】")[1]
    user_id = lines[3].strip().split("】")[1]
    title = lines[4].strip().split("】")[1]

    # 转换开始时间为datetime
    start_time = datetime.strptime(start_time_str, "%Y年%m月%d日%H時%M分%S秒")

    # xml样式 (可以删点)
    xml_style = """<BililiveRecorderXmlStyle><z:stylesheet version="1.0" id="s" xml:id="s" xmlns:z="http://www.w3.org/1999/XSL/Transform"><z:output method="html"/><z:template match="/"><html><meta name="viewport" content="width=device-width"/><title>仿mikufans录播姬弹幕文件 - <z:value-of select="/i/BililiveRecorderRecordInfo/@name"/></title><style>body{margin:0}h1,h2,p,table{margin-left:.3125rem}table{border-spacing:0}td,th{border:.0625rem solid grey;padding:.0625rem}th{position:sticky;top:0;background:#4098de}tr:hover{background:#d9f4ff}div{overflow:auto;max-height:80vh;max-width:100vw;width:fit-content}</style><h1>仿<a href="https://rec.danmuji.org">mikufans录播姬</a>弹幕XML文件</h1><p>本文件不支持在 IE 浏览器里预览，请使用 Chrome Firefox Edge 等浏览器。</p><p>文件用法参考文档 <a href="https://rec.danmuji.org/user/danmaku/">https://rec.danmuji.org/user/danmaku/</a></p><table><tr><td>录播姬版本</td><td><z:value-of select="/i/BililiveRecorder/@version"/></td></tr><tr><td>房间号</td><td><z:value-of select="/i/BililiveRecorderRecordInfo/@roomid"/></td></tr><tr><td>主播名</td><td><z:value-of select="/i/BililiveRecorderRecordInfo/@name"/></td></tr><tr><td>录制开始时间</td><td><z:value-of select="/i/BililiveRecorderRecordInfo/@start_time"/></td></tr><tr><td><a href="#d">弹幕</a></td><td>共 <z:value-of select="count(/i/d)"/> 条记录</td></tr></table><h2 id="d">弹幕</h2><div id="dm"><table><tr><th>用户名</th><th>出现时间</th><th>用户ID</th><th>弹幕</th><th>参数</th></tr><z:for-each select="/i/d"><tr><td><z:value-of select="@user"/></td><td></td><td></td><td><z:value-of select="."/></td><td><z:value-of select="@p"/></td></tr></z:for-each></table></div><script>Array.from(document.querySelectorAll('#dm tr')).slice(1).map(t=>t.querySelectorAll('td')).forEach(t=>{let p=t[4].textContent.split(','),a=p[0];t[1].textContent=`${(Math.floor(a/60/60)+'').padStart(2,0)}:${(Math.floor(a/60%60)+'').padStart(2,0)}:${(a%60).toFixed(3).padStart(6,0)}`;t[2].innerHTML=`&lt;a target=_blank rel="nofollow noreferrer" href="https://twitcasting.tv/${p[6]}"&gt;${p[6]}&lt;/a&gt;`})</script></html></z:template></z:stylesheet></BililiveRecorderXmlStyle>"""

    # xml文件头 (可以删点)
    xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet type="text/xsl" href="#s"?>
<i>
<chatid>0</chatid>
<mission>0</mission>
<maxlimit>1000</maxlimit>
<state>0</state>
<real_name>0</real_name>
<source>0</source>
<BililiveRecorder version="2.8.1" />
<BililiveRecorderRecordInfo roomid="{user_id}" shortid="0" name="{user_name}" title="{title}" start_time="{start_time_str}" />
{xml_style}

"""

    # 遍历弹幕内容并转换为xml格式
    for line in lines[5:]:
        match = time_pattern.search(line)
        if match:
            danmaku_time_str = match.group(1)
            danmaku_time = datetime.strptime(danmaku_time_str, "%Y/%m/%d %H:%M:%S")
            time_difference = (danmaku_time - start_time).seconds

            # 提取用户ID和内容
            danmaku_user_id = match.group(3)
            danmaku_content = match.group(2)

            # 对弹幕内容进行HTML转义 (防止日本人奇怪的颜表情)
            danmaku_content_escaped = html.escape(danmaku_content)

            # 弹幕xml格式
            xml_danmaku = f'<d p="{time_difference},1,25,16777215,{danmaku_time.timestamp()},0,{danmaku_user_id},0" user="{danmaku_user_id}">{danmaku_content_escaped}</d>\n'
            xml_content += xml_danmaku

    xml_content += "</i>"

    # 写入xml
    with open(xml_file_path, "w", encoding="utf-8") as xml_file:
        xml_file.write(xml_content)

    print(f"[Info] 已生成 {xml_file_path}")
    



process_folder(file_path)

print("")
print("[Info] 已完成 所有弹幕文件 XML转换操作")