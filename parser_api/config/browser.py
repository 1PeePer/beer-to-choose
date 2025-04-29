from typing import Dict, Any

# Browser settings
BROWSER_SETTINGS: Dict[str, Any] = {
    "headless": True,
    "args": [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-accelerated-2d-canvas",
        "--no-first-run",
        "--no-zygote",
        "--disable-gpu",
        "--disable-geolocation",
        "--disable-extensions",
        "--disable-notifications",
        "--disable-infobars",
        "--disable-popup-blocking",
        "--disable-web-security",
        "--disable-features=IsolateOrigins,site-per-process",
    ],
    "timeout": 30000
}

# Context settings
CONTEXT_SETTINGS: Dict[str, Any] = {
    "locale": "ru-RU",
    "viewport": {"width": 1920, "height": 1080},
    "extra_http_headers": {
        "Referer": "https://lenta.com/",
        "Sec-Fetch-Dest": "document",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    },
    "permissions": [],
    "geolocation": None
}

# Parser settings
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
BASE_URL = "https://lenta.com"
TIMEOUT = 30000
LOG_MAX_SIZE_MB = 1
RESULTS_DIR = "results"