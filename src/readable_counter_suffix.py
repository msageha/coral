import re

import counter_suffix_dicts
import MultiDictMeCab

def word_is_num(word): return re.match(r'\A[0-9０-９]+\Z', word)

def zen_to_han(num):
    '''全角数字を半角数字にする'''
    zenkaku = str.maketrans('０１２３４５６７８９', '0123456789')
    return num.translate(zenkaku)

def replace(node):
    node_ipa = node['ipadic'].next
    text = ''
    while node_ipa:
        word = node_ipa.surface
        feature = node_ipa.feature.split(',')
        #前の文字が，数字であったとき．助数詞の読みで適切なものを付与する．
        if feature[2] == '助数詞' and word_is_num(node_ipa._mecab_node.prev.surface) and counter_suffix_dicts.uncertainty_counter_suffix_dict.get(word):
            num = int(zen_to_han(node_ipa._mecab_node.prev.surface))
            counter_suffix_pronounce_dict = counter_suffix_dicts.uncertainty_counter_suffix_dict[word]
            if not counter_suffix_pronounce_dict['only_under10'] or counter_suffix_pronounce_dict.get(num):
                num %= 10
            if counter_suffix_pronounce_dict.get(num) and feature[7] != counter_suffix_pronounce_dict[num]:
                word = counter_suffix_pronounce_dict[num]
        text += word
        node_ipa = node_ipa.next
    return text, text != MultiDictMeCab.get_word(node, dic='ipadic')
