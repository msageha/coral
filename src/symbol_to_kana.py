from symbol_dicts import special_char_dict

def replace(node):
    """記号を，カナに変換する"""
    node_neologd = node['mecab-ipadic-neologd'].next
    word = node_neologd.surface
    feature = node_neologd.feature.split(',')
    if feature[0] == '記号' and special_char_dict.get(word):
        return special_char_dict.get(word), True
    return word, False