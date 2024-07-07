import random
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

dictionaries = {
    'example_dict': {
        'word1': {'meaning': 'は', 'examples': [], 'wordgem': '', 'pronji': '', 'alphapron': ''},
        'word2': {'meaning': 'を', 'examples': [], 'wordgem': '', 'pronji': '', 'alphapron': ''},
        'word1': {'meaning': 'に', 'examples': [], 'wordgem': '', 'pronji': '', 'alphapron': ''},
        'word2': {'meaning': 'が', 'examples': [], 'wordgem': '', 'pronji': '', 'alphapron': ''},
        'word1': {'meaning': 'の', 'examples': [], 'wordgem': '', 'pronji': '', 'alphapron': ''},
        'word2': {'meaning': 'で', 'examples': [], 'wordgem': '', 'pronji': '', 'alphapron': ''},
        'word1': {'meaning': 'です', 'examples': [], 'wordgem': '', 'pronji': '', 'alphapron': ''},
        'word2': {'meaning': 'でしょ', 'examples': [], 'wordgem': '', 'pronji': '', 'alphapron': ''},
        'word1': {'meaning': 'それ', 'examples': [], 'wordgem': '', 'pronji': '', 'alphapron': ''},
        'word2': {'meaning': '人口', 'examples': [], 'wordgem': '', 'pronji': '', 'alphapron': ''},
      　'word1': {'meaning': '食べる', 'examples': [], 'wordgem': '', 'pronji': '', 'alphapron': ''},
        'word2': {'meaning': 'もっとも', 'examples': [], 'wordgem': '', 'pronji': '', 'alphapron': ''},

    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/today_example')
def today_example():
    example_words = list(dictionaries['example_dict'].keys())
    random.shuffle(example_words)
    selected_words = example_words[:50]
    example_sentence = " ".join(selected_words) + "。"
    return render_template('today_example.html', example_sentence=example_sentence)

@app.route('/create_dictionary', methods=['GET', 'POST'])
def create_dictionary():
    if request.method == 'POST':
        dictionary_name = request.form.get('dictionary_name')
        if dictionary_name and dictionary_name not in dictionaries:
            dictionaries[dictionary_name] = {}
            flash(f'{dictionary_name}が作成されました')
            return redirect(url_for('hontai', dictionary_name=dictionary_name))
        else:
            flash('辞書名が無効、または既に存在します')
    return render_template('create_dictionary.html')

@app.route('/hontai')
def hontai():
    # 単語ページ
    return "単語ページ"

@app.route('/example')
def example():
    # 例文ページ
    return "例文ページ"

@app.route('/todayex')
def todayex():
    # 今日の例文ページ
    return today_example()

@app.route('/setting')
def setting():
    # 設定ページ
    return "設定ページ"

@app.route('/wordrec')
def wordrec():
    # 造語依頼ページ
    return "造語依頼ページ"

# 他のエンドポイントもここに追加

if __name__ == '__main__':
    app.run(debug=True)
