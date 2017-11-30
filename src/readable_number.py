"""this script is function number to kana for clova"""
import re

import counter_suffix_dicts
import MultiDictMeCab

def word_is_num(word): return re.match(r'\A[0-9０-９]+\Z', word)

def zen_to_han(num):
    '''全角数字を半角数字にする'''
    zenkaku = str.maketrans('０１２３４５６７８９', '0123456789')
    return num.translate(zenkaku)

DEFAULT_NUMBER_PRONOUNCE_DICT = {
    0: 'ゼロ', 1: 'イチ', 2: 'ニ', 3: 'サン', 4: 'ヨン', 5: 'ゴ',
    6: 'ロク', 7: 'ナナ', 8: 'ハチ', 9: 'キュウ', 10: 'ジュウ', 100: 'ヒャク'
}

def replace(node):
    node_ipa = node['ipadic'].next
    word = MultiDictMecab.get(node, dic='ipadic')
    text = ''
    while node_ipa:
        word = node_ipa.surface
        feature = node_ipa.feature.split(',')
        next_word = node.next.surface
        next_feature = node.next.feature.split(',')
        word_copy = word
        #前の文字が，数字であったとき．助数詞の読みで適切なものを付与する．
        if word_is_num(word) and next_feature[2] == '助数詞':
            num = int(zen_to_han(word))
            