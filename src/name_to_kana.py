import re
import subprocess

#正規表現
def check_all_kana(word):
    return re.match(r'\A[ぁ-んァ-ン・ー]+\Z', word)
def check_all_katakana(word):
    return re.match(r'\A[ァ-ン]+\Z', word)

def replace(node):
    """固有名詞の人名で、ipa辞書とneologdで読みが異なる場合"""
    node_neologd = node['mecab-ipadic-neologd'].next
    node_ipa = node['ipadic'].next
    word = node_neologd.surface
    feature_neologd = node_neologd.feature.split(',')
    word_copy = word
    #例：word='橋本環奈', feature = ['名詞', '固有名詞', '人名', '一般', '*', '*', '橋本環奈', 'ハシモトカンナ', 'ハシモトカンナ']
    if feature_neologd[1] == '固有名詞' and feature_neologd[2]=='人名' and (not check_all_kana(word)):
        word_copy = ''
        while node_ipa:
            word_ipa = node_ipa.surface
            feature_ipa = node_ipa.feature.split(',')
            node_ipa = node_ipa.next
            if word_ipa != '' and check_all_katakana(word_ipa):
                word_copy += word_ipa
                continue
            elif word_ipa == '' or len(feature_ipa) <= 7 or feature_ipa[7] =='*':
                continue
            word_copy += feature_ipa[7]
        if word_copy != feature_neologd[7]:
            word_copy = feature_neologd[7]
        else:
            word_copy = word
    return word_copy, word_copy!=word