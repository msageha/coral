import re

import data

def word_is_kana(word): return re.match(r'\A[ぁ-んァ-ン]+\Z', word)

def hira_to_kata(word):
    '''ひらがなをカタカナに'''
    hira = 'ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをん'
    kata = 'ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲン'
    zenkaku = str.maketrans(hira, kata)
    return word.translate(zenkaku)

def translate(node):
    word = node.surface
    feature = node.feature.split(',')
    if word_is_kana(word):
        while len(feature) < 9:
            feature.append('*')
        if feature[7] == '*':
            feature[7] = hira_to_kata(word)
            feature[8] = hira_to_kata(word)
    return ','.join(feature), ','.join(feature) != node.feature
