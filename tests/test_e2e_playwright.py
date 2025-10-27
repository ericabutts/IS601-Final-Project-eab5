import subprocess
import time
import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.e2e
def test_calculator_frontend():
    # Start FastAPI backend with coverage
    backend = subprocess.Popen(
        ["coverage", "run", "-m", "uvicorn", "main:app", "--port", "8000"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(1)

    # Playwright test
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:5500/frontend/index.html")


        page.fill("#a","5")
        page.fill("#b","7")
        page.click("#add")

        page.wait_for_selector("#result", timeout=5000)
        result = page.inner_text("#result")
        assert result == "12"

        browser.close()

    backend.terminate()
