import sys
import time
import pymongo as pm
import jieba as jb
import jieba.posseg as pseg


def cut_article(cur_article):
    for col in cur_article.find({}).batch_size(1):
        try:
            if 'text_cut' in col.keys():
                print('exist {}'.format(col['title']), file=sys.stderr)
                continue
            tmp = [(w.word, w.flag)
                   for w in pseg.cut(col['text']) if w.word.strip()]
            col['text_cut'] = [w[0] for w in tmp]
            col['text_speech'] = [w[1] for w in tmp]

            comment = []
            for com in col['comment']:
                tmp = [(w.word, w.flag)
                       for w in pseg.cut(com['text']) if w.word.strip()]
                com['text_cut'] = [w[0] for w in tmp]
                com['text_speech'] = [w[1] for w in tmp]
                comment.append(com)
            col['comment'] = comment
            print(col['_id'], col['title'], file=sys.stderr)
            cur_article.update({'url': col['url']}, col)
        except:
            pass
def cut_user(cur):
    for col in cur.find({}).batch_size(1):
        item = []
        for data in col['data']:
            item.append(data)
            tmp = [(w.word, w.flag)
                   for w in pseg.cut(data['text']) if w.word.strip()]
            item[-1]['text_cut'] = [w[0] for w in tmp]
            item[-1]['text_speech'] = [w[1] for w in tmp]
        col['data'] = item
        cur.update({'_id': col['_id']}, col)
        print(col['_id'], col['id'], file=sys.stderr)


def main():
    # connect to database

    client = pm.MongoClient(
        'mongodb://user:1234@cluster0-shard-00-00-4uiip.gcp.mongodb.net:27017,cluster0-shard-00-01-4uiip.gcp.mongodb.net:27017,cluster0-shard-00-02-4uiip.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
    tdb = client['ptt_static']
    cur_article = tdb['article']
    cur_user = tdb['user']

    # jieba config
    jb.set_dictionary('./dict/dict.txt')
    jb.load_userdict('./dict/ptt_dict.txt')
    jb.enable_parallel(4)

    # stopword = set()
    # with open('./dict/ptt_stop_word.txt', 'r') as f:
    #     for line in f.readlines():
    #         stopword.add(line.strip())

    # cut_article(cur_article)
    cut_user(cur_user)


if __name__ == "__main__":
    main()
