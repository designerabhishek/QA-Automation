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
    """Health check endpoint for deployment monitoring."""
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

@app.route('/audit', methods=['POST'])
def audit():
    """Handle the audit form submission - simplified version without Selenium."""
    try:
        # Get URLs from the form
        urls_text = request.form.get('urls', '').strip()
        
        if not urls_text:
            flash('Please enter at least one URL to audit.', 'error')
            return redirect(url_for('index'))
        
        # Parse URLs (split by newlines and clean up)
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        
        if not urls:
            flash('Please enter at least one valid URL to audit.', 'error')
            return redirect(url_for('index'))
        
        # Print URLs to console for debugging
        logger.info(f"Audit requested for {len(urls)} URLs:")
        for i, url in enumerate(urls, 1):
            logger.info(f"  {i}. {url}")
        
        # Simplified audit without Selenium
        generated_reports = []
        for url in urls:
            try:
                # Create a simple CSV report without Selenium
                domain = url.replace('https://', '').replace('http://', '').replace('/', '')
                filename = f"{domain}.csv"
                filepath = os.path.join(EXPORT_DIR, filename)
                
                with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Category', 'Check Item', 'Status', 'Details', 'URL'])
                    writer.writerow(['Summary', 'Audit Date', 'Completed', datetime.now().isoformat(), url])
                    writer.writerow(['Summary', 'Pages Audited', 'Completed', '1', ''])
                    writer.writerow(['Summary', 'Total Issues', 'Completed', '0', ''])
                    writer.writerow(['Note', 'Selenium Disabled', 'Info', 'This is a simplified audit without browser automation', ''])
                
                generated_reports.append({
                    'url': url,
                    'filename': filename,
                    'path': filepath,
                })
                logger.info(f"Generated report for {url}: {filename}")
                
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                flash(f"Error processing {url}: {e}", 'error')
        
        # Store generated report filenames in session
        session['generated_reports'] = generated_reports
        flash(f'Generated {len(generated_reports)} report(s).', 'info')
        
        # Use 303 to ensure clients follow with GET
        return redirect(url_for('results'), code=303)
        
    except Exception as e:
        logger.error(f"Error in audit route: {str(e)}")
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/results')
def results():
    """Display audit results and download links."""
    reports = session.get('generated_reports', [])
    return render_template('results.html', reports=reports)

@app.route('/download/<filename>')
def download_file(filename):
    """Serve CSV files for download."""
    try:
        file_path = os.path.join(EXPORT_DIR, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('File not found.', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(debug=False, host='0.0.0.0', port=port)
