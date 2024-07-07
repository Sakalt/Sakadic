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
