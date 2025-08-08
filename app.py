from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
import os
import csv
from datetime import datetime
import tempfile
import shutil

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Ensure export directory exists
EXPORT_DIR = 'export'
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

@app.route('/')
def index():
    """Render the main page with the URL input form."""
    return render_template('index.html')

@app.route('/audit', methods=['POST'])
def audit():
    """Handle the audit form submission."""
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
        print(f"Audit requested for {len(urls)} URLs:")
        for i, url in enumerate(urls, 1):
            print(f"  {i}. {url}")
        
        # Import and use audit_logic module
        from audit_logic import perform_audit, generate_csv_report
        
        generated_reports = []
        for url in urls:
            try:
                audit_data = perform_audit(url)
                csv_path = generate_csv_report(audit_data, export_dir=EXPORT_DIR)
                filename = os.path.basename(csv_path)
                generated_reports.append({
                    'url': url,
                    'filename': filename,
                    'path': csv_path,
                })
            except Exception as e:
                print(f"Error processing {url}: {e}")
                flash(f"Error processing {url}: {e}", 'error')
        
        # Store generated report filenames in session
        session['generated_reports'] = generated_reports
        flash(f'Generated {len(generated_reports)} report(s).', 'info')
        
        # Use 303 to ensure clients follow with GET
        return redirect(url_for('results'), code=303)
        
    except Exception as e:
        print(f"Error in audit route: {str(e)}")
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
    app.run(debug=True, host='0.0.0.0', port=5000)
