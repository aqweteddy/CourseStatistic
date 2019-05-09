import pymongo as pm
import jieba as jb
import jieba.posseg as pseg

def main():
    # connect to database

    client = pm.MongoClient(host="localhost", port=27017)
    tdb = client['ptt_static']
    cur_article = tdb['article']
    # cur_user = tdb['user']

    # jieba config
    jb.set_dictionary('./dict/dict.txt')
    jb.load_userdict('./dict/ptt_dict.txt')
    jb.enable_parallel(3)

    # stopword = set()
    # with open('./dict/ptt_stop_word.txt', 'r') as f:
    #     for line in f.readlines():
    #         stopword.add(line.strip())


# cut_text.append([w.word.strip() for w in pseg.cut(text) if w.word.strip() and w.flag in ('N', 'n') and w.word.strip() not in stop_word])\n
    for col in cur_article.find({}):
        tmp = [(w.word, w.flag) for w in pseg.cut(col['text']) if w.word.strip()]
        col['text_cut'] = [w[0] for w in tmp]
        col['text_speech'] = [w[1] for w in tmp]

        comment = []
        for com in col['comment']:
            tmp = [(w.word, w.flag) for w in pseg.cut(com['text']) if w.word.strip()]
            com['text_cut'] = [w[0] for w in tmp]
            com['text_speech'] = [w[1] for w in tmp]
            comment.append(com)
        col['comment'] = comment
        print(col['_id'])
        cur_article.update({'_id': col['_id']}, col)






if __name__ == "__main__":
    main()