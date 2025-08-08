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
- **Dependencies**: webdriver-manager for automatic ChromeDriver management

## Project Structure

```
/
|-- app.py               # Main Flask application
|-- audit_logic.py       # Selenium and BeautifulSoup audit functions
|-- requirements.txt     # Python dependencies
|-- .gitignore          # Git ignore patterns
|-- README.md           # Project documentation
|-- /templates/
|   |-- index.html      # Main user interface
|   |-- results.html    # Results display page
|-- /export/            # Generated CSV reports
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Site-Audit-Automation
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Input URLs**: Enter one or more website URLs in the textarea (one per line)
2. **Start Audit**: Click the "Start Audit" button to begin the analysis
3. **Wait for Processing**: The tool will crawl each website and perform comprehensive checks
4. **Download Reports**: Access individual CSV reports for each audited website

## Development Status

### ✅ Completed
- Basic Flask application structure
- Modern, responsive web interface
- URL parsing and form handling
- File download functionality
- Project structure and documentation

### 🚧 In Progress
- Selenium audit logic implementation
- CSV report generation with detailed findings
- Multi-page website crawling
- Comprehensive audit checks

### 📋 Planned Features
- Sitemap discovery and crawling
- Link integrity validation
- Image optimization checks
- SEO analysis
- Performance metrics
- Accessibility compliance checks
- Custom audit configurations

## API Endpoints

- `GET /` - Main application page
- `POST /audit` - Submit URLs for auditing
- `GET /results` - View audit results
- `GET /download/<filename>` - Download CSV reports

## Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` or `production`
- `SECRET_KEY`: Flask secret key for session management

### Chrome WebDriver
The application automatically downloads and manages ChromeDriver using `webdriver-manager`. No manual installation required.

## Deployment

### Development
```bash
python app.py
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please create an issue in the repository or contact the development team.

---

**Note**: This is the initial implementation. The audit logic module (`audit_logic.py`) contains placeholder functionality and will be fully implemented in the next development phase.
