import re

def last_is_num(word):
    if not word:
        return False
    return re.match(r'[0-9]+\Z', word)

def first_is_num(word):
    if not word:
        return False
    return re.match(r'\A[0-9]+', word)

def translate(node):
    word = node.surface
    feature = node.feature.split(',')
    if word == '.' and last_is_num(node.prev.surface) and first_is_num(node.next.surface):
        while len(feature) < 9:
            feature.append('*')
        feature[2] = '小数点'
        feature[7] = 'テン'
        feature[8] = 'テン'
    return ','.join(feature), ','.join(feature) != node.feature
