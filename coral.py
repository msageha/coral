import MeCab
import subprocess
import src

mecab_dic_dir = subprocess.check_output(['mecab-config', '--dicdir']).decode('utf-8').strip() + '/'
neologd_path = mecab_dic_dir + 'mecab-ipadic-neologd'
mecab = MeCab.Tagger('-d {}'.format(neologd_path))
mecab.parse('')
# ipadic_path = mecab_dic_dir + 'ipadic'
# mecab_ipa = MeCab.Tagger('-d {}'.format(ipadic_path))
# mecab_ipa.parse('')
# mecab = mecab_ipa

def parse(text):
    text, _ = src.normalize.replace(text)
    node = mecab.parseToNode(text).next
    while node.next:
        surface = node.surface
        feature = node.feature
        is_changed = False
        if not is_changed:
            feature, changed = src.readable_number.translate(node)
            is_changed |= changed
        if not is_changed:
            feature, changed = src.readable_counter.translate(node)
            is_changed |= changed
        if not is_changed:
            feature, changed = src.dot_kana.translate(node)
            is_changed |= changed
        node = node.next
        yield surface, feature

if __name__ == '__main__':
    text = input()
    for node in parse(text):
        surface = node[0]
        feature = node[1]
        print(f'{surface}\t{feature}')
