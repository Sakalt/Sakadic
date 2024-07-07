# モックデータベース
dictionary = {
    "apple": {"meaning": "A fruit that is sweet and crisp.", "forms": ["apples"], "tags": ["fruit"], "related": ["banana"]},
    "banana": {"meaning": "A yellow fruit that is soft and sweet.", "forms": ["bananas"], "tags": ["fruit"], "related": ["apple"]}
}

@app.route('/add_word', methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        word = request.form.get('word')
        meaning = request.form.get('meaning')
        forms = request.form.get('forms').split(',')
        tags = request.form.get('tags').split(',')
        related = request.form.get('related').split(',')
        if word and meaning:
            dictionary[word] = {"meaning": meaning, "forms": forms, "tags": tags, "related": related}
            return redirect(url_for('public_dic'))
        else:
            return "単語と意味を入力してください"
    return render_template('add_word.html')

@app.route('/public_dic')
def public_dic():
    return render_template('public_dic.html', dictionary=dictionary)

@app.route('/dic', methods=['GET', 'POST'])
def dic():
    if request.method == 'POST':
        word = request.form.get('word')
        entry = dictionary.get(word)
        if entry:
            meaning = entry["meaning"]
            forms = entry["forms"]
            tags = entry["tags"]
            related = entry["related"]
        else:
            meaning = "Word not found."
            forms = tags = related = []
        return render_template('dic.html', word=word, meaning=meaning, forms=forms, tags=tags, related=related)
    return render_template('dic.html')
