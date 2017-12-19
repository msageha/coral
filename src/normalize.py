import re

def num_zen2han(num):
    '''全角数字を半角数字にする'''
    zenkaku = str.maketrans('０１２３４５６７８９', '0123456789')
    return num.translate(zenkaku)

def dot_zen2han(text):
    translated_text = re.sub(r'([0-9]+)．([0-9]+)', r'\1.\2', text)
    return translated_text

def replace(text):
    translated_text = num_zen2han(text)
    translated_text = dot_zen2han(translated_text)
    return translated_text, translated_text != text