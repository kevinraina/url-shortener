# URL Shortener - Traffic Generator
# Run this before/during demo to make Grafana graphs light up

$BASE = "http://a69d26da0e5974a79b07ea6ad3986915-2075969225.us-east-1.elb.amazonaws.com"

$URLS = @(
    "https://www.google.com",
    "https://www.instagram.com",
    "https://www.github.com",
    "https://www.reddit.com",
    "https://www.netflix.com",
    "https://www.amazon.com",
    "https://www.twitter.com",
    "https://www.linkedin.com",
    "https://www.stackoverflow.com",
    "https://www.wikipedia.org",
    "https://www.spotify.com",
    "https://www.microsoft.com"
)

Write-Host "Starting traffic generator... Press Ctrl+C to stop" -ForegroundColor Green
Write-Host "Open http://localhost:3000 to see live metrics" -ForegroundColor Cyan
Write-Host ""

$round = 1
while ($true) {
    Write-Host "--- Round $round ---" -ForegroundColor Yellow

    $short_codes = @()

    # Shorten all URLs
    foreach ($url in $URLS) {
        try {
            $body = "{`"original_url`": `"$url`"}"
            $response = Invoke-RestMethod -Uri "$BASE/shorten" -Method POST -Body $body -ContentType "application/json"
            $code = $response.short_code
            $short_codes += $code
            Write-Host "  Shortened: $url -> $code" -ForegroundColor White
        } catch {
            Write-Host "  Error shortening $url" -ForegroundColor Red
        }
    }

    # Hit the short URLs (generates redirect traffic)
    foreach ($code in $short_codes) {
        try {
            Invoke-WebRequest -Uri "$BASE/$code" -MaximumRedirection 0 -ErrorAction SilentlyContinue | Out-Null
            Write-Host "  Visited: /$code" -ForegroundColor Gray
        } catch {}
    }

    # Hit health endpoint
    Invoke-RestMethod -Uri "$BASE/health" -Method GET | Out-Null

    Write-Host "  Round $round done. Sleeping 3s..." -ForegroundColor Green
    $round++
    Start-Sleep -Seconds 3
}
