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
        '111\t���~,��,*,*,*,*,*\n
        ��\t���~,��β,�����~,*,*,*,��,�ۥ�,�ۥ�\n
        ��\t���~,�B�廯,*,*,*,*,��,��,��\n
        �U�P\t���~,һ��,*,*,*,*,�U�P,����ԥ�,����ԥ�'
    '''
    text = input()
    node = mecab.parseToNode(text)
    while node:
        #�����ǄI����
        node = node.next
    for line in sys.stdin:
        yomi = unit.modify_mecab_node(node)
        print(node.surface)
        print(node.feature)
        print(yomi)
        print('--------')
        node = node.next

