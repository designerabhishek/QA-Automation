# Website Audit Tool

A comprehensive web-based website auditing tool built with Python, Flask, and Selenium. This tool allows users to input multiple website URLs and generates detailed CSV reports for each audited site.

## Features

- **Multi-URL Processing**: Input multiple website URLs for batch auditing
- **Comprehensive Analysis**: Performs detailed audits including link integrity, image validation, SEO checks, and more
- **CSV Report Generation**: Creates detailed, downloadable CSV reports for each audited website
- **Modern Web Interface**: Clean, responsive UI with real-time progress indicators
- **Headless Browser Automation**: Uses Selenium with Chrome WebDriver for reliable website crawling

## Technology Stack

- **Backend**: Python with Flask
- **Browser Automation**: Selenium WebDriver
- **HTML Parsing**: BeautifulSoup4
- **Web Server**: Gunicorn (for production deployment)
- **Dependencies**: Uses Selenium Manager by default; Docker image includes Chromium + Chromedriver

## Project Structure

```
/
|-- app.py               # Main Flask application
|-- audit_logic.py       # Selenium and BeautifulSoup audit functions
|-- requirements.txt     # Python dependencies
|-- .gitignore           # Git ignore patterns
|-- Dockerfile           # Container image (Chromium + Chromedriver)
|-- Procfile             # App start command (for PaaS)
|-- render.yaml          # Render deployment config
|-- README.md            # Project documentation
|-- /templates/
|   |-- index.html       # Main user interface
|   |-- results.html     # Results display page
|-- /export/             # Generated CSV reports
```

## Local Installation

1. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the application:
```bash
python3 app.py
```

3. Access the application at `http://localhost:5000`

## Deployment (Render)

- This repo includes a Dockerfile and `render.yaml`.
- Render will build from Dockerfile and run `gunicorn app:app`.
- The Docker image installs Chromium and Chromedriver and sets env vars:
  - `CHROME_BINARY=/usr/bin/chromium`
  - `CHROMEDRIVER_PATH=/usr/bin/chromedriver`
- Flask `SECRET_KEY` is read from env (set in `render.yaml`).

### Steps
1. Push this repo to GitHub
2. Create a new Web Service on Render (use this repo)
3. Confirm Environment: Docker
4. Health check path: `/`
5. Deploy

## Usage

1. Paste one or more website URLs (one per line)
2. Click "Start Audit"
3. Wait for processing and download per-site CSVs

## Notes
- For full audits locally, Chrome must be installed. In Docker deployment, Chromium is preinstalled.
- If you run without Docker in production, ensure Chrome and Chromedriver are available and set `CHROME_BINARY`/`CHROMEDRIVER_PATH`.
