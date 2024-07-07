import os
from flask import Flask, request, redirect, url_for, render_template, flash, send_file
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'woff', 'ttf', 'otf', 'sfnt', 'json'}
app.secret_key = 'supersecretkey'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# モックデータベース
dictionaries = {
    "default": {
        "apple": {
            "meaning": "A fruit that is sweet and crisp.",
            "forms": ["apples"],
            "tags": ["fruit"],
            "related": ["banana"],
            "examples": ["I ate an apple for breakfast."]
        },
        "banana": {
            "meaning": "A yellow fruit that is soft and sweet.",
            "forms": ["bananas"],
            "tags": ["fruit"],
            "related": ["apple"],
            "examples": ["Bananas are rich in potassium."]
        }
    }
}

# 造語依頼リスト
word_requests = []

@app.route('/upload_otm', methods=['POST'])
def upload_otm():
    if 'file' not in request.files:
        flash('ファイルが選択されていません')
        return redirect(request.url)
    
    file = request.files['file']
    dictionary_name = request.form.get('dictionary')

    if file.filename == '':
        flash('ファイルが選択されていません')
        return redirect(request.url)

    if dictionary_name not in dictionaries:
        flash('辞書が存在しません')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('ファイルがアップロードされました')

        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entry in data['dictionary']:
                dictionaries[dictionary_name][entry['word']] = entry

        return redirect(url_for('public_dic'))

    flash('ファイルのアップロードに失敗しました')
    return redirect(request.url)

@app.route('/export_otm/<dictionary_name>', methods=['GET'])
def export_otm(dictionary_name):
    if dictionary_name in dictionaries:
        data = {
            "dictionary": list(dictionaries[dictionary_name].values())
        }
        filename = f"{dictionary_name}_export.json"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return send_file(filepath, as_attachment=True)
    else:
        flash('辞書が見つかりません')
        return redirect(url_for('public_dic'))

# 辞書一覧の表示
@app.route('/')
def index():
    return render_template('index.html', dictionaries=dictionaries.keys())

@app.route('/public_dic/<dictionary_name>')
def public_dic(dictionary_name):
    return render_template('public_dic.html', dictionary=dictionaries.get(dictionary_name, {}))

if __name__ == '__main__':
    app.run(debug=True)
