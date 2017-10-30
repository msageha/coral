import MeCab
from src import unit

mecab_dic_dir = '/usr/local/mecab/lib/mecab/dic/'
neologd_path = mecab_dic_dir + 'mecab-ipadic-neologd-all'
mecab = MeCab.Tagger('-d {}'.format(neologd_path))
mecab.parse('')
ipadic_path = mecab_dic_dir + 'ipadic'
mecab_ipa = MeCab.Tagger('-d {}'.format(ipadic_path))
mecab_ipa.parse('')

if __name__ == '__main__':
    '''
      text =
        '111\t名詞,数,*,*,*,*,*\n
        本\t名詞,接尾,助数詞,*,*,*,本,ホン,ホン\n
        の\t助詞,連体化,*,*,*,*,の,ノ,ノ\n
        鉛筆\t名詞,一般,*,*,*,*,鉛筆,エンピツ,エンピツ'
    '''
    text = input()
    node = mecab.parseToNode(text)
    while node:
        #ココで処理する
        node = node.next
    for line in sys.stdin:
        yomi = unit.modify_mecab_node(node)
        print(node.surface)
        print(node.feature)
        print(yomi)
        print('--------')
        node = node.next

