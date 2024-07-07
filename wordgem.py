def wordgem(words):
    # 文字列の組み合わせと省略を行うロジック
    combined_words = ''.join(words)
    return combined_words[:len(words)//2]  # 簡単な例
