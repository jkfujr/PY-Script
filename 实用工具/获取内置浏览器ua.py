from fastapi import FastAPI, Request, Response, HTTPException, Cookie

app = FastAPI()

@app.get("/")
def read_root(request: Request):
    headers_text = "========== Headers ==========\n"
    for name, value in request.headers.items():
        headers_text += f"{name}: {value};\n"

    cookies_text = "========== Cookies ==========\n"
    for cookie_name, cookie_value in request.cookies.items():
        cookies_text += f"{cookie_name}: {cookie_value};\n"

    return Response(content=headers_text + cookies_text, media_type="text/plain")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
