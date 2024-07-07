# ヘッダーと見出しの色設定
HEADER_COLOR = "#CC7700"
WORD_COLOR = "#EEA100"
HEADING_COLOR = "#767676"

@app.route('/public_dic')
def public_dic():
    return render_template('public_dic.html', dictionaries=dictionaries)

@app.route('/create_dictionary', methods=['GET', 'POST'])
def create_dictionary():
    if request.method == 'POST':
        dictionary_name = request.form.get('dictionary_name')
        if dictionary_name and dictionary_name not in dictionaries:
            dictionaries[dictionary_name] = {}
            return redirect(url_for('public_dic'))
        else:
            flash('辞書名を入力してくださいまたは既に存在しています')
    return render_template('create_dictionary.html')

@app.route('/add_word/<dictionary_name>', methods=['GET', 'POST'])
def add_word(dictionary_name):
    if request.method == 'POST':
        word = request.form.get('word')
        meaning = request.form.get('meaning')
        examples = request.form.get('examples')
        if word and meaning:
            dictionaries[dictionary_name][word] = {
                "meaning": meaning,
                "examples": examples.split('\n')
            }
            return redirect(url_for('view_dictionary', dictionary_name=dictionary_name))
        else:
            flash('単語と意味を入力してください')
    return render_template('add_word.html', dictionary_name=dictionary_name)

@app.route('/view_dictionary/<dictionary_name>')
def view_dictionary(dictionary_name):
    if dictionary_name in dictionaries:
        dictionary = dictionaries[dictionary_name]
        return render_template('view_dictionary.html', dictionary_name=dictionary_name, dictionary=dictionary)
    else:
        flash('辞書が見つかりません')
        return redirect(url_for('public_dic'))

@app.route('/settings/<dictionary_name>', methods=['GET', 'POST'])
def settings(dictionary_name):
    if dictionary_name not in dictionaries:
        flash('辞書が見つかりません')
        return redirect(url_for('public_dic'))

    if request.method == 'POST':
        description = request.form.get('description')
        font = request.form.get('font')
        wordgem_config = request.form.get('wordgem')
        pronji_config = request.form.get('pronji')
        alphapron_config = request.form.get('alphapron')

        # 設定を保存する処理
        flash('設定が保存されました')
        return redirect(url_for('view_dictionary', dictionary_name=dictionary_name))

    return render_template('settings.html', dictionary_name=dictionary_name)

# 造語依頼機能
@app.route('/request_word/<dictionary_name>', methods=['POST'])
def request_word(dictionary_name):
    requested_word = request.form.get('requested_word')
    word_requests.append({"dictionary": dictionary_name, "word": requested_word})
    flash('造語依頼が送信されました')
    return redirect(url_for('view_dictionary', dictionary_name=dictionary_name))

# スワデシュリストの単語から例文を生成
@app.route('/example_sentence/<dictionary_name>')
def example_sentence(dictionary_name):
    swadesh_list = [...]  # スワデシュリストの単語リストをここに追加
    selected_words = random.sample(swadesh_list, 150) + random.sample(list(dictionaries[dictionary_name].keys()), 50)
    sentence = generate_sentence(selected_words)
    return render_template('example_sentence.html', dictionary_name=dictionary_name, sentence=sentence)

def generate_sentence(words):
    return " ".join(words)  # 単語をいい感じに組み合わせるロジックを追加

# 統計機能
@app.route('/statistics/<dictionary_name>')
def statistics(dictionary_name):
    word_count = len(dictionaries[dictionary_name])
    example_count = sum(len(entry["examples"]) for entry in dictionaries[dictionary_name].values())
    return render_template('statistics.html', dictionary_name=dictionary_name, word_count=word_count, example_count=example_count)
@app.route('/add_word/<dictionary_name>', methods=['GET', 'POST'])
@app.route('/add_word/<dictionary_name>', methods=['GET', 'POST'])
def add_word(dictionary_name):
    if request.method == 'POST':
        word = request.form.get('word')
        meaning = request.form.get('meaning')
        examples = request.form.get('examples')
        wordgem = request.form.get('wordgem')
        pronji = request.form.get('pronji')
        alphapron = request.form.get('alphapron')
        
        if word and meaning:
            dictionaries[dictionary_name][word] = {
                "meaning": meaning,
                "examples": examples.split('\n'),
                "wordgem": wordgem,
                "pronji": pronji,
                "alphapron": alphapron
            }
            return redirect(url_for('view_dictionary', dictionary_name=dictionary_name))
        else:
            flash('単語と意味を入力してください')
    return render_template('add_word.html', dictionary_name=dictionary_name)
