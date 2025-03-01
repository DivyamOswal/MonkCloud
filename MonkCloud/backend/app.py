from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet, InvalidToken
import os
import tempfile

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Dummy user data
users = {
    "admin": {"password": generate_password_hash("password123")}
}

# File upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load or create encryption key
KEY_FILE = "secret.key"
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
else:
    with open(KEY_FILE, 'rb') as key_file:
        key = key_file.read()

cipher_suite = Fernet(key)

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# Utility functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encrypt_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
        if file_data.startswith(b'--BEGIN--'):
            flash("File is already encrypted.", "info")
            return
        encrypted_data = cipher_suite.encrypt(file_data)
        with tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(file_path)) as temp_file:
            temp_file.write(b'--BEGIN--' + encrypted_data)
        os.replace(temp_file.name, file_path)
    except Exception as e:
        flash(f"Error encrypting file: {e}", "danger")

def decrypt_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        if not encrypted_data.startswith(b'--BEGIN--'):
            flash("File is not encrypted. No decryption needed.", "info")
            return
        encrypted_data = encrypted_data[len(b'--BEGIN--'):]

        decrypted_data = cipher_suite.decrypt(encrypted_data)
        with tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(file_path)) as temp_file:
            temp_file.write(decrypted_data)
        os.replace(temp_file.name, file_path)
    except InvalidToken:
        flash("Invalid token: Unable to decrypt the file. It may have been tampered with.", "danger")
        raise
    except Exception as e:
        flash(f"Error decrypting file: {e}", "danger")
        raise

def get_file_size(file_path):
    try:
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
        return round(file_size, 2)
    except Exception as e:
        flash(f"Error getting file size: {e}", "danger")
        return None

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and check_password_hash(users[username]['password'], password):
            user = User(username)
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "danger")

    uploaded_files = []
    if current_user.is_authenticated:
        uploaded_files = [
            (filename, get_file_size(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            for filename in os.listdir(app.config['UPLOAD_FOLDER'])
        ]
    
    return render_template('index.html', uploaded_files=uploaded_files)

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('index'))

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        encrypt_file(file_path)
        flash('File uploaded and encrypted successfully!', 'success')
    else:
        flash('Invalid file format. Please upload a valid file.', 'danger')
    
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
@login_required
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        decrypt_file(file_path)
        response = send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
        encrypt_file(file_path)
        return response
    except InvalidToken:
        flash("The file cannot be decrypted. It may be corrupted or tampered with.", "danger")
        return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
@login_required
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f"File {filename} deleted successfully.", "success")
    else:
        flash("File not found.", "danger")
    
    return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
