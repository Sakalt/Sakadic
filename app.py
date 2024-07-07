from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

# データベースモデルの定義
class DictionaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"DictionaryEntry('{self.word}', '{self.definition}', '{self.author}')"

# すべての辞書エントリを表示するルート（ページングと検索）
@app.route('/all_entries', methods=['GET', 'POST'])
def all_entries():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str)

    if search_query:
        entries = DictionaryEntry.query.filter(
            (DictionaryEntry.word.contains(search_query)) |
            (DictionaryEntry.definition.contains(search_query))
        ).paginate(page=page, per_page=5)
    else:
        entries = DictionaryEntry.query.paginate(page=page, per_page=5)

    return render_template('all_entries.html', entries=entries, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)
