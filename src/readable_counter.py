import re

import data

def word_is_num(word): return re.match(r'\A[0-9]+\Z', word)

def translate(node):
    word = node.surface
    feature = node.feature.split(',')
    if feature[2] == '助数詞' and word_is_num(node.prev.surface) and data.counter_suffix_dicts.uncertainty_counter_suffix_dict.get(word):
        if node.prev.prev and node.prev.prev.surface == '.' and node.prev.prev.prev and word_is_num(node.prev.prev.prev.surface):
            return ','.join(feature), ','.join(feature) != node.feature
        num = int(node.prev.surface)
        counter_suffix_pronounce_dict = data.counter_suffix_dicts.uncertainty_counter_suffix_dict[word]
        if not (counter_suffix_pronounce_dict.get(num) or counter_suffix_pronounce_dict['only_under10']):
            num %= 10
        if counter_suffix_pronounce_dict.get(num) and feature[7] != counter_suffix_pronounce_dict[num]:
            word = counter_suffix_pronounce_dict[num]
            feature[7] = word
            feature[8] = word
    return ','.join(feature), ','.join(feature) != node.feature
