from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

@app.get("/redirect")
async def get_html():
    redirect_url = "/target_url"
    return RedirectResponse(url=redirect_url)

@app.get("/target_url")
def target_url():
    return {"message": "Redirected to target URL"}