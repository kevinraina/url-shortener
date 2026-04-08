from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.services.url_services import create_short_url, get_original_url
from app.core.config import BASE_URL

app = FastAPI()

class URLRequest(BaseModel):
    original_url: str

@app.post("/shorten")
def shorten_url(request: URLRequest):
    short_code = create_short_url(request.original_url)
    return {"short_url": f"{BASE_URL}/{short_code}"}

@app.get("/{short_code}")
def redirect_url(short_code: str):
    original_url = get_original_url(short_code)

    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url=original_url)