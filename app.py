from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Maxfiy kalit sessiyalar uchun
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Admin login ma’lumotlari
ADMIN_CREDENTIALS = {
    'Surojbek5680': '1195680Surojbek'
}

# Oddiy foydalanuvchilar ro‘yxati (demo)
users = {}

# Login sahifasi
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Login yoki parol noto‘g‘ri!')
    return render_template('login.html')

# Admin panel
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('admin.html', files=files)

# Fayl yuklash
@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('admin'):
        return redirect(url_for('login'))
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('admin'))

# Foydalanuvchi qo‘shish (simulyatsiya)
@app.route('/add_user', methods=['POST'])
def add_user():
    if not session.get('admin'):
        return redirect(url_for('login'))
    username = request.form['newUser']
    password = request.form['newPass']
    users[username] = password
    return redirect(url_for('admin'))

# Faylni yuklab olish
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
