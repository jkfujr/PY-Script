import uvicorn
import subprocess
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>BBD</title>
</head>
<body>
    <form action="/runcmd" method="post">
        <label for="cmd_input">输入连接: </label>
        <input type="text" id="cmd_input" name="cmd_input" value=""><br><br>
        <input type="submit" value="确认">
    </form>
    <p>{}</p>
    <textarea rows="10" cols="50" readonly>{}</textarea>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_content.format("", "")

@app.post("/runcmd")
async def run_cmd(request: Request):
    form_data = await request.form()
    cmd_input = form_data["cmd_input"]
    try:
        result = subprocess.run([r"C:\jkfujr\Tools\BBDown\BBD.exe", cmd_input], capture_output=True, text=True)
        output = result.stdout
    except Exception as e:
        return HTMLResponse(
            content=html_content.format(f"错误: {e}", ""), status_code=500
        )

    return HTMLResponse(
        content=html_content.format(f"已执行下载: {cmd_input}", output), status_code=200
    )

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=45678,
        log_level="info",
        reload=True,
        use_colors=True,
    )
