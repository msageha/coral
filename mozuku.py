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

if __name__ == '__main__':
    text = input()
    text, _ = src.normalize.replace(text)
    node = mecab.parseToNode(text).next
    # node_ipa = mecab_ipa.parseToNode(text).next
    # neologd_total_word_length = 0
    # ipadic_total_word_length = 0
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
            feature, changed = src.kana.translate(node)
            is_changed |= changed
        print(f'{surface}\t{feature}')
        node = node.next
        # neologd_total_word_length += len(node.surface)
        # while ipadic_total_word_length >= neologd_total_word_length:
        #     ipadic_total_word_length += len(node_ipa.surface)
        #     node_ipa = node_ipa.next
