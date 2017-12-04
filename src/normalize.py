

def num_zen_to_han(num):
    '''全角数字を半角数字にする'''
    zenkaku = str.maketrans('０１２３４５６７８９', '0123456789')
    return num.translate(zenkaku)

def replace(text):
    translated_text = num_zen_to_han(text)
    return translated_text, translated_text != text
