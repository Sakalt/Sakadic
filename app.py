from flask import Flask, render_template, request, redirect, url_for, session
import os
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# モックデータベース
dictionary = {
    "apple": "A fruit that is sweet and crisp.",
    "banana": "A yellow fruit that is soft and sweet."
}

# アカウントとグループのモックデータ
users = {"admin": {"password": "adminpass", "role": "admin"},
         "user1": {"password": "password1", "role": "user"}}
groups = {"group1": ["user1"]}

# 例文（リンゴ文）
example_sentence = "リンゴを食べる"
example_sentence = "リンゴを食べた"

# ファイルアップロード設定
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_sentence(sentence):
    return re.findall(r'\w+', sentence)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dic', methods=['GET', 'POST'])
def dic():
    if request.method == 'POST':
        word = request.form.get('word')
        meaning = dictionary.get(word, "Word not found.")
        return render_template('dic.html', word=word, meaning=meaning)
    return render_template('dic.html')

@app.route('/example', methods=['GET'])
def example():
    words = analyze_sentence(example_sentence)
    return render_template('example.html', sentence=example_sentence, words=words)

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if users.get(username) and users[username]["password"] == password:
            session['username'] = username
            session['role'] = users[username]["role"]
            return redirect(url_for('user_profile', username=username))
        else:
            return "ログイン失敗"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username not in users:
            users[username] = {"password": password, "role": "user"}
            return redirect(url_for('user'))
        else:
            return "ユーザー名は既に存在します"
    return render_template('register.html')

@app.route('/user/<username>')
def user_profile(username):
    if 'username' in session and session['username'] == username:
        return render_template('profile.html', username=username)
    else:
        return redirect(url_for('user'))

@app.route('/groups')
def groups_view():
    return render_template('groups.html', groups=groups)

@app.route('/public_dic')
def public_dic():
    return render_template('public_dic.html', dictionary=dictionary)

@app.route('/add_word', methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        word = request.form.get('word')
        meaning = request.form.get('meaning')
        if word and meaning:
            dictionary[word] = meaning
            return redirect(url_for('public_dic'))
        else:
            return "単語と意味を入力してください"
    return render_template('add_word.html')

@app.route('/word_request', methods=['GET', 'POST'])
def word_request():
    if request.method == 'POST':
        word = request.form.get('word')
        meaning = request.form.get('meaning')
        if word and meaning:
            # ここで造語依頼を処理する（例：DBに保存、管理者に通知など）
            return "造語依頼が送信されました"
        else:
            return "単語と意味を入力してください"
    return render_template('word_request.html')

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "ファイルがありません"
        file = request.files['file']
        if file.filename == '':
            return "ファイルが選択されていません"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload_image.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('uploaded_file.html', filename=filename)

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if 'username' in session and session['role'] == 'admin':
        return render_template('manage.html', dictionary=dictionary, users=users)
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
