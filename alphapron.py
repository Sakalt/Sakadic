def alphapron(word):
    # 子音と母音に分けて発音を当てるロジック
    vowels = 'aeiou'
    consonants = ''.join(set(word) - set(vowels))
    return {'consonants': consonants, 'vowels': ''.join(v for v in word if v in vowels)}
