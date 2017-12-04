import math
import re

import counter_suffix_dicts
import MultiDictMeCab

def word_is_num(word): return re.match(r'\A[0-9０-９]+\Z', word)

def num_to_kana(num_str, num_type):
    if int(num_str) == 0: return 'ゼロ'
    word = ''
    DEFAULT_NUMBER_PRONOUNCE_DICT = {0: '', 1: '', 2: 'ニ', 3: 'サン', 4: 'ヨン', 5: 'ゴ',
        6: 'ロク', 7: 'ナナ', 8: 'ハチ', 9: 'キュウ'}
    NUM_SPAN_PRONOUNCE = {0:'', 1:'マン', 2:'オク', 3:'チョウ', 4:'ケイ'}
    THOUSAND_PRONOUNCE = {0: '', 1:'セン', 2:'セン', 3:'ゼン', 4:'セン', 5:'セン',
        6:'セン', 7:'セン', 8:'セン', 9:'セン'}
    HUNDRED_PRONOUNCE = {0:'', 1:'ヒャク', 2:'ヒャク', 3:'ビャク', 4:'ヒャク', 5:'ヒャク',
        6:'ピャク', 7:'ヒャク', 8:'ピャク', 9:'ヒャク'}
    TEN_PRONOUNCE = {0:'', 1:'ジュウ', 2:'ジュウ', 3:'ジュウ', 4:'ジュウ', 5:'ジュウ',
        6:'ジュウ', 7:'ジュウ', 8:'ジュウ', 9:'ジュウ'}
    # 4の倍数になるように上位の桁をゼロ埋めする
    num_str = '0000' + num_str
    num_str = num_str[-int(len(num_str)/4)*4:]

    for i in range(int((len(num_str)/4))-1, -1, -1):
        sub_num_str = num_str[-4*(i+1):][:4]
        if sub_num_str == '0000':
            continue

        elif i==0:
            #下４桁の処理
            word += DEFAULT_NUMBER_PRONOUNCE_DICT[int(sub_num_str[0])]
            word += THOUSAND_PRONOUNCE[int(sub_num_str[0])]
            if int(sub_num_str) == 100:
                word += counter_suffix_dicts.type_number_pronounce_dict[num_type][100]
                break
            else:
                word += DEFAULT_NUMBER_PRONOUNCE_DICT[int(sub_num_str[1])]
                word += HUNDRED_PRONOUNCE[int(sub_num_str[1])]
            if int(sub_num_str) == 10:
                word += counter_suffix_dicts.type_number_pronounce_dict[num_type][10]
                break
            else:
                word += DEFAULT_NUMBER_PRONOUNCE_DICT[int(sub_num_str[2])]
                word += TEN_PRONOUNCE[int(sub_num_str[2])]
            word += counter_suffix_dicts.type_number_pronounce_dict[num_type][int(sub_num_str[3])]

        else:
            word += DEFAULT_NUMBER_PRONOUNCE_DICT[int(sub_num_str[0])]
            word += THOUSAND_PRONOUNCE[int(sub_num_str[0])]
            word += DEFAULT_NUMBER_PRONOUNCE_DICT[int(sub_num_str[1])]
            word += HUNDRED_PRONOUNCE[int(sub_num_str[1])]
            word += DEFAULT_NUMBER_PRONOUNCE_DICT[int(sub_num_str[2])]
            word += TEN_PRONOUNCE[int(sub_num_str[2])]
            word += DEFAULT_NUMBER_PRONOUNCE_DICT[int(sub_num_str[3])]
            if sub_num_str == '0001':
                word += 'イチ'
            word += NUM_SPAN_PRONOUNCE.get(i)
    return word

def replace(node):
    node_ipa = node['ipadic'].next
    text = ''
    while node_ipa:
        word = node_ipa.surface
        feature = node_ipa.feature.split(',')
        next_feature = node_ipa._mecab_node.next.feature.split(',')
        #次の文字が助数詞であったとき，数字の読みで適切なものを付与する．
        if word_is_num(word) and len(next_feature) > 7 and next_feature[2] == '助数詞':
            if counter_suffix_dicts.counter_suffix_number_type_dict.get((node_ipa._mecab_node.next.surface, next_feature[7])):
                num_type = counter_suffix_dicts.counter_suffix_number_type_dict[(node_ipa._mecab_node.next.surface, next_feature[7])]
            else:
                num_type = 'A1'
            if num_to_kana(word, num_type) != num_to_kana(word, 'A1'):
                word = num_to_kana(word, num_type)

        #前の文字が数字であったとき．助数詞の読みで適切なものを付与する．
        elif feature[2] == '助数詞' and word_is_num(node_ipa._mecab_node.prev.surface) and counter_suffix_dicts.uncertainty_counter_suffix_dict.get(word):
            num = int(node_ipa._mecab_node.prev.surface)
            counter_suffix_pronounce_dict = counter_suffix_dicts.uncertainty_counter_suffix_dict[word]
            if not counter_suffix_pronounce_dict['only_under10'] or counter_suffix_pronounce_dict.get(num):
                num %= 10
            if counter_suffix_pronounce_dict.get(num) and feature[7] != counter_suffix_pronounce_dict[num]:
                word = counter_suffix_pronounce_dict[num]

        text += word
        node_ipa = node_ipa.next

    return text, text != MultiDictMeCab.get_word(node, dic='ipadic')
