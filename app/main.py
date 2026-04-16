from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
from app.services.url_services import create_short_url, get_original_url
from app.core.config import BASE_URL

app = FastAPI(
    title="URL Shortener",
    description="Cloud-native URL shortening service — powered by FastAPI, Redis, Kubernetes & AWS",
    version="1.0.0",
)

# ── Prometheus metrics ──────────────────────────────────────────────────────
Instrumentator().instrument(app).expose(app)

urls_created = Counter(
    "url_shortener_urls_created_total",
    "Total number of short URLs created",
)

# ── Health check ────────────────────────────────────────────────────────────
@app.get("/health", tags=["ops"])
def health_check():
    return {"status": "healthy", "service": "url-shortener"}

# ── Core endpoints ──────────────────────────────────────────────────────────
class URLRequest(BaseModel):
    original_url: str

@app.post("/shorten", tags=["urls"])
def shorten_url(request: URLRequest):
    short_code = create_short_url(request.original_url)
    urls_created.inc()
    return {"short_url": f"{BASE_URL}/{short_code}", "short_code": short_code}

@app.get("/{short_code}", tags=["urls"])
def redirect_url(short_code: str):
    original_url = get_original_url(short_code)
    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=original_url)
