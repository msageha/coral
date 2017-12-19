import re

import data

def word_is_num(word):
    if not word: return False
    return re.match(r'\A[0-9]+\Z', word)

def num_to_kana(num_str, num_type, is_decimal):
    if int(num_str) == 0: return 'レイ'
    word = ''
    if is_decimal:
        DEFAULT_NUMBER_PRONOUNCE_DICT = {0: 'ゼロ', 1: 'イチ', 2: 'ニ', 3: 'サン', 4: 'ヨン', 5: 'ゴオ',
            6: 'ロク', 7: 'ナナ', 8: 'ハチ', 9: 'キュウ'}
        for i in num_str:
            word += DEFAULT_NUMBER_PRONOUNCE_DICT[int(i)]
    else:
        DEFAULT_NUMBER_PRONOUNCE_DICT_WITHOUT_1 = {0: '', 1: '', 2: 'ニ', 3: 'サン', 4: 'ヨン', 5: 'ゴ',
            6: 'ロク', 7: 'ナナ', 8: 'ハチ', 9: 'キュウ'}
        DEFAULT_NUMBER_PRONOUNCE_DICT_WITH_1 = {0: '', 1: 'イチ', 2: 'ニ', 3: 'サン', 4: 'ヨン', 5: 'ゴ',
            6: 'ロク', 7: 'ナナ', 8: 'ハチ', 9: 'キュウ'}
        THOUSAND_NUMBER_PRONOUNCE_DICT = {0: '', 1: '', 2: 'ニ', 3: 'サン', 4: 'ヨン', 5: 'ゴ',
            6: 'ロク', 7: 'ナナ', 8: 'ハッ', 9: 'キュウ'}
        HUNDRED_NUMBER_PRONOUNCE_DICT = {0: '', 1: '', 2: 'ニ', 3: 'サン', 4: 'ヨン', 5: 'ゴ',
            6: 'ロッ', 7: 'ナナ', 8: 'ハッ', 9: 'キュウ'}
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
                word += THOUSAND_NUMBER_PRONOUNCE_DICT[int(sub_num_str[0])]
                word += THOUSAND_PRONOUNCE[int(sub_num_str[0])]
                if int(sub_num_str) == 100:
                    word += data.counter_suffix_dicts.type_number_pronounce_dict[num_type][100]
                    break
                else:
                    word += HUNDRED_NUMBER_PRONOUNCE_DICT[int(sub_num_str[1])]
                    word += HUNDRED_PRONOUNCE[int(sub_num_str[1])]
                if int(sub_num_str) == 10:
                    word += data.counter_suffix_dicts.type_number_pronounce_dict[num_type][10]
                    break
                else:
                    word += DEFAULT_NUMBER_PRONOUNCE_DICT_WITHOUT_1[int(sub_num_str[2])]
                    word += TEN_PRONOUNCE[int(sub_num_str[2])]
                if int(num_str) > 10 and (num_type[0] == 'D' or (num_type[0] == 'C' and int(sub_num_str[3]) < 6)):
                    word += DEFAULT_NUMBER_PRONOUNCE_DICT_WITH_1[int(sub_num_str[3])]
                else:
                    if int(sub_num_str[3]) == 0:
                        pass
                    else:
                        word += data.counter_suffix_dicts.type_number_pronounce_dict[num_type][int(sub_num_str[3])]
            else:
                word += THOUSAND_NUMBER_PRONOUNCE_DICT[int(sub_num_str[0])]
                word += THOUSAND_PRONOUNCE[int(sub_num_str[0])]
                word += HUNDRED_NUMBER_PRONOUNCE_DICT[int(sub_num_str[1])]
                word += HUNDRED_PRONOUNCE[int(sub_num_str[1])]
                word += DEFAULT_NUMBER_PRONOUNCE_DICT_WITHOUT_1[int(sub_num_str[2])]
                word += TEN_PRONOUNCE[int(sub_num_str[2])]
                word += DEFAULT_NUMBER_PRONOUNCE_DICT_WITH_1[int(sub_num_str[3])]
                word += NUM_SPAN_PRONOUNCE.get(i)
    return word

def translate(node):
    word = node.surface
    feature = node.feature.split(',')
    next_feature = node.next.feature.split(',')
    #次の文字が助数詞であったとき，数字の読みで適切なものを付与する．
    if word_is_num(word):
        if len(next_feature) > 7 and data.counter_suffix_dicts.counter_suffix_number_type_dict.get((node.next.surface, next_feature[7])):
            num_type = data.counter_suffix_dicts.counter_suffix_number_type_dict[(node.next.surface, next_feature[7])]
        elif node.next.surface == '.': #小数点のときの処理，（小数点のときは，読みがついていないため）
            num_type = 'A8'
        else:
            num_type = 'A1'
        if node.prev.surface == '.' and word_is_num(node.prev.prev.surface):
            is_decimal = True
        else:
            is_decimal = False
        word = num_to_kana(word, num_type, is_decimal)
        while len(feature) < 9:
            feature.append('*')

        feature[7] = word
        feature[8] = word
    return ','.join(feature), ','.join(feature) != node.feature
