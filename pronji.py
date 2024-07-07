def pronji(kanji):
    # 漢字の発音を当てるロジック
    kanji_dict = {'漢': 'kan', '串': 'kan'}
    return kanji_dict.get(kanji, '')
