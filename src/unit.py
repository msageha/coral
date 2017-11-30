import argparse
import csv
import math
import re
import sys

# Input files to be processed
data_dir = 'data'
unit_dict_path = data_dir + '/unit_dict.csv'
unit_pronounce_dict_path = data_dir + '/unit_pronounce.csv'

# 正規表現
def word_is_num(word): return re.match(r'\A[0-9]+\Z', word)
def word_is_all_type_num(word): return re.match(r'\A[0-9一二三四五六七八九〇壱弐参０-９]+\Z', word)

# 正規化処理
def convert_kanji_num(num):
    '''漢数字を'''
    ksuji = str.maketrans('一二三四五六七八九〇壱弐参', '1234567890123')
    return num.translate(ksuji)

def em_to_en(num):
    '''全角数字を半角数字にする'''
    zenkaku = str.maketrans('０１２３４５６７８９', '0123456789')
    return num.translate(zenkaku)

def num_normalize(num):
    num = convert_kanji_num(num)
    num = em_to_en(num)
    return num

def number_pronounce_type_dict_generate():
    '''
        単位毎に、数字の読みのタイプを定義
    '''
    number_pronounce_type = '''A1 イチ ニ サン ヨン ゴ ロク ナナ ハチ キュウ ジュウ ヒャク
        A2 イチ ニ サン ヨン ゴ ロク ナナ ハチ キュウ ジュッ ヒャク
        A3 イッ ニ サン ヨン ゴ ロク ナナ ハチ キュウ ジュッ ヒャク
        A4 イチ ニ サン ヨン ゴ ロッ ナナ ハチ キュウ ジュッ ヒャッ
        A5 イッ ニ サン ヨン ゴ ロク ナナ ハッ キュウ ジュッ ヒャク
        A6 イッ ニ サン ヨン ゴ ロッ ナナ ハチ キュウ ジュッ ヒャッ
        A7 イッ ニ サン ヨン ゴ ロッ ナナ ハッ キュウ ジュッ ヒャッ
        A8 イチ ニー サン ヨン ゴー ロク ナナ ハチ キュウ ジュッ ヒャク
        B1 イチ ニ サン シ ゴ ロク シチ ハチ ク ジュウ ヒャク
        B2 イチ ニ サン ヨン ゴ ロク シチ ハチ ク ジュウ ヒャク
        B3 イチ ニ サン ヨン ゴ ロク シチ ハチ キュウ ジュウ ヒャク
        B4 イチ ニ サン ヨ ゴ ロク シチ ハチ ク ジュウ ヒャク
        B5 イチ ニ サン ヨン ゴ ロク ナナ ハチ ク ジュウ ヒャク
        B6 イチ ニ サン ヨン ゴ ロク ナナ ハチ キュウ ジュウ ヒャク
        B7 イチ ニ サン ヨ ゴ ロク ナナ ハチ キュウ ジュウ ヒャク
        B8 イチ 二 サン ヨ ゴ ロク ナナ ハチ ク ジュウ ヒャク
        C1 ヒト フタ ミ ヨ イツ ム ナナ ヤ ココノ ト ヒャク
        C2 ヒト フタ ミ ヨ イツ ム ナナ ヤ キュウ ト ヒャク
        C3 ヒト フタ ミ ヨ イツ ム ナナ ハチ キュウ ト ヒャク
        C4 ヒト フタ ミ ヨ イツ ム ナナ ハチ キュウ ジュウ ヒャク
        C5 ヒト フタ ミ ヨ ゴ ム ナナ ハチ キュウ ジュッ ヒャク
        C6 ヒト フタ サン ヨン ゴ ム ナナ ハチ キュウ ジュウ ヒャク
        C7 ヒト フタ サン ヨン ゴ ロク ナナ ハチ キュウ ジュウ ヒャク
        C8 ヒト フタ サン ヨン ゴ ロク ナナ ハッ キュウ ジュッ ヒャク
        C9 ヒト フタ サン ヨン ゴ ロク ナナ ハチ キュウ ジュッ ヒャク
        C10 ヒト フタ サン ヨン ゴ ロク ナナ ハチ キュウ ジュッ ヒャッ
        C11 ヒト フタ サン ヨン ゴ ロッ ナナ ハチ キュウ ジュッ ヒャッ
        D1 イチ フツ ミッ ヨッ イツ ムイ ナノ　ヨウ ココノ トウ ヒャク
        D2 ヒト フタ ミ ヨン イツ ムウ ナノ ヨウ ココノ トウ
        D3 ヒト フタ ミ ヨ ゴ ロク ナナ ハチ キュウ ジュッ
        D4 ヒト フタ ミ ヨ イツ ム ナナ ヤ ココノ トウ'''.split('\n')
    number_pronounce_type_dict =  {}
    for i in number_pronounce_type:
        tmp = i.split()
        key = tmp[0]
        number_pronounce_type_dict[key] = {}
        number_pronounce_type_dict[key][0] = ''
        for j in range(1, len(tmp)):
            number_pronounce_type_dict[key][j] = tmp[j]
    return number_pronounce_type_dict

def read_csv(file):
    return_dict = {}
    with open(file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            key = row[0]
            return_dict[key] = {}
            for i in range(1, len(row)):
                return_dict[key][header[i]] = row[i]
    return return_dict

def num_pronounce_generate(num, number_pronounce_type): #numは4桁以下
    last_num_pronounce = number_pronounce_type_dict[number_pronounce_type]
    '''数字の読みを生成する'''
    num_pronounce = {0: '', 1: '', 2: 'ニ', 3: 'サン', 4: 'ヨン', 5: 'ゴ', 6: 'ロク', 7: 'ナナ', 8: 'ハチ', 9: 'キュー'}
    num_span_pronounce = {1:'', 10**4:'マン', 10**8:'オク', 10**12:'チョウ', 10**16:'ケイ', 10**20:'ガイ'}
    thousand_pronounce = {0: '', 1:'セン', 2:'セン', 3:'ゼン', 4:'セン', 5:'セン', 6:'セン', 7:'セン', 8:'セン', 9:'セン'}
    hundred_pronounce = {0:'', 1:'ヒャク', 2:'ヒャク', 3:'ビャク', 4:'ヒャク', 5:'ヒャク', 6:'ピャク', 7:'ヒャク', 8:'ピャク', 9:'ヒャク'}
    pronounce = ''
    if num == 0:
        return 'ゼロ'
    num_size = int(math.log10(num)+1) #桁数
    #4桁づつ(兆、億、万、千以下)に分けて処理する。
    for i in range(math.ceil(num_size/4), 0, -1):
        num_span = 10**((i-1)*4)
        num_tmp = int( (num%(num_span*10**4)) / num_span )
        num_tmp_padding =  '%04d' % num_tmp
        if num_tmp_padding == '0000':
            continue
        if int(num_tmp_padding[0]) != 0:
            if int(num_tmp_padding[0]) != 1or i == 1:
                pronounce += num_pronounce[int(num_tmp_padding[0])]
            else:
                pronounce += 'イッ'
            pronounce += thousand_pronounce[int(num_tmp_padding[0])]
        if int(num_tmp_padding[1]) != 0:
            pronounce += num_pronounce[int(num_tmp_padding[1])] + hundred_pronounce[int(num_tmp_padding[1])]
        if int(num_tmp_padding[2]) != 0:
            if i == 1 and int(num_tmp_padding[3])==0:
                pronounce += num_pronounce[int(num_tmp_padding[2])] + last_num_pronounce[10]
            else:
                pronounce += num_pronounce[int(num_tmp_padding[2])] + 'ジュー'
        #最後のループ(9999以下のとき)
        if i==1:
            pronounce += last_num_pronounce[int(num_tmp_padding[3])]
        else:
            pronounce += num_pronounce[int(num_tmp_padding[3])] if int(num_tmp_padding[3]) != 1 else 'イチ'
            pronounce += num_span_pronounce[num_span]
    return pronounce

def decimal_proniunce(num_str):
    num_pronounce = {'0': 'ゼロ', '1': 'イチ', '2': 'ニー', '3': 'サン', '4': 'ヨン', '5': 'ゴー', '6': 'ロク', '7': 'ナナ', '8': 'ハチ', '9': 'キュー'}
    pronounce = ''
    for i in num_str:
        pronounce += num_pronounce[i]
    return pronounce.rstrip('ー')

def unit_pronounce_generate(num, unit, unit_dict, unit_pronounce_dict):
    '''単位の読みを生成する'''
    pronounce = None
    if unit_pronounce_dict.get(unit):
        unit_num_key = str(num)[-4:]
        if unit_num_key == '1000':
            pass
        elif unit_num_key[-3:] == '100':
            unit_num_key = '100'
        elif unit_num_key[-2:] == '10':
            unit_num_key = '10'
        else:
            unit_num_key = unit_num_key[-1]
        pronounce = unit_pronounce_dict[unit][unit_num_key]
    elif unit_dict.get(unit):
        pronounce = unit_dict[unit]['読み']
    return pronounce

def modify_mecab_node(node, num=None, insert_comma=False):
    '''mecabのnodeを受け取り、数字と単位について正しい読みに修正して返す'''
    #単語が数字だった場合
    if word_is_all_type_num(node.surface):
        num = int(num_normalize(node.surface)) if num else num
        unit = node.next.surface
        num_pronounce_type = unit_dict.get(unit, {'type': 'A1'})['type']
        if node.prev and (node.prev.surface == '.' or node.prev.surface == '．') and node.prev.prev and word_is_all_type_num(node.prev.prev.surface):
            num_pronounce = decimal_proniunce(str(num))
        else:
            num_pronounce = num_pronounce_generate(num, num_pronounce_type)
        return num_pronounce
    #前の単語が数字だった場合
    elif node.prev and word_is_all_type_num(node.prev.surface):
        num = int(num_normalize(node.prev.surface))
        unit = node.surface
        unit_pronounce = unit_pronounce_generate(num, unit, unit_dict, unit_pronounce_dict)
        return unit_pronounce
    return None

def modify_mecab_text(text):
    '''
    例:
    text = '111\t名詞,数,*,*,*,*,*\n本\t名詞,接尾,助数詞,*,*,*,本,ホン,ホン\nの\t助詞,連体化,*,*,*,*,の,ノ,ノ\n鉛筆\t名詞,一般,*,*,*,*,鉛筆,エンピツ,エンピツ'
    '''
    pass

number_pronounce_type_dict = number_pronounce_type_dict_generate()
unit_pronounce_dict = read_csv(unit_pronounce_dict_path)
unit_dict = read_csv(unit_dict_path)
