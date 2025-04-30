from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/downloads'
PASSWORD = 'your_secure_password'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    files = os.listdir(UPLOAD_FOLDER)
    if not files:
        return "No file available.", 404
    latest = sorted(files)[-1]
    return send_from_directory(UPLOAD_FOLDER, latest, as_attachment=True)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        pwd = request.form.get('password')
        file = request.files.get('file')
        if pwd == PASSWORD and file:
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('index'))
        return "Unauthorized or no file selected.", 403
    return render_template('admin.html')
