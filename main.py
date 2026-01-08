
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/fetch-stamps")
async def fetch_stamps(req: Request):
    data = await req.json()
    url = data.get("url")

    if not url:
        return JSONResponse({"error": "url required"}, status_code=400)

    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        spans = soup.select("span.mdCMN09Image")
        images = set()

        for span in spans:
            style = span.get("style", "")
            m = re.search(r'url\(["\']?(.*?)["\']?\)', style)
            if m:
                images.add(m.group(1))

        return list(images)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

import uvicorn

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



