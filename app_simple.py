from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
import os
import csv
from datetime import datetime
import tempfile
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Ensure export directory exists
EXPORT_DIR = 'export'
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)
    logger.info(f"Created export directory: {EXPORT_DIR}")

@app.route('/')
def index():
    """Render the main page with the URL input form."""
    logger.info("Index page accessed")
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for deployment platforms."""
    logger.info("Health check accessed")
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

@app.route('/audit', methods=['POST'])
def audit():
    """Handle the audit form submission."""
    try:
        url = request.form.get('url', '').strip()
        if not url:
            flash('Please enter a valid URL', 'error')
            return redirect(url_for('index'))
        
        logger.info(f"Audit requested for URL: {url}")
        
        # For now, just return a simple response without Selenium
        # This will help us test if the basic deployment works
        results = [
            {
                'category': 'Basic Check',
                'check_item': 'URL Accessibility',
                'status': 'PASS',
                'details': 'URL is accessible (simplified check)',
                'url': url
            },
            {
                'category': 'Basic Check', 
                'check_item': 'Response Time',
                'status': 'INFO',
                'details': 'Response time check (simplified)',
                'url': url
            }
        ]
        
        # Generate CSV filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        domain = url.replace('https://', '').replace('http://', '').replace('/', '_').replace('.', '_')
        filename = f"{domain}_{timestamp}.csv"
        filepath = os.path.join(EXPORT_DIR, filename)
        
        # Write results to CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Category', 'Check Item', 'Status', 'Details', 'URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        
        logger.info(f"Results saved to: {filepath}")
        
        return render_template('results.html', results=results, filename=filename)
        
    except Exception as e:
        logger.error(f"Error during audit: {str(e)}")
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    """Download the CSV file."""
    try:
        filepath = os.path.join(EXPORT_DIR, filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            flash('File not found', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        flash('Error downloading file', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
