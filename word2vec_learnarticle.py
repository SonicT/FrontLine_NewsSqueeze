# coding=utf-8
from gensim.models import Word2Vec
import os
import pymysql.cursors
import datetime
from textrkr_test import TextRank


def start_learn(sid=100, date=str(datetime.date.today())):

    # word2vec 저장할 경로 확인
    try:
        if not os.path.exists('../../news'):
            os.makedirs('../../news')
    except os.error:
        print('you already have dir, going next')

    # sql에서 데이터(기사) 가져오기
    sql = 'SELECT content FROM article WHERE sid = %s and date = %s'
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='TIGER',
                           db='NewsSummary',
                           charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql, (sid, date))
    query_res = cursor.fetchall()

    filename_tsv = '../../news/w2_{}.tsv'.format(sid)
    filename_txt = '../../news/w2vec_{}.txt'.format(sid)

    # Word2Vec 로드.
    word2vec = Word2Vec(size=100, window=5, min_count=2, workers=4)
    cont = True
    if os.path.exists(filename_tsv):
        word2vec = Word2Vec.load(filename_tsv)
    else:
        cont = False

    # 기사마다 에러 덩어리 기사가 나거나 냉무 기사도 등장하므로, 기사별로 학습을 진행한다.
    index = 0
    for article in query_res:
        print(article)
        tes = TextRank(list(article)[0])
        # 1개 기사 단위로 읽을 컨텍스트 버퍼. word2vec은 단어 사이의 위치 상관성을 보므로, 단어가 1개보단 많아야.
        contextbuf = []
        for sentence in tes.sentences:
            if len(sentence.all_nouns) > 1:
                contextbuf.append(sentence.all_nouns)
        if not cont:
            word2vec = Word2Vec(contextbuf, size=100, window=5, min_count=2, workers=4)
            cont = True
        else:
            word2vec.build_vocab(contextbuf, update=True)
            word2vec.train(contextbuf, total_examples=len(contextbuf), epochs=word2vec.iter)
    word2vec.save(filename_tsv)
    word2vec.wv.save_word2vec_format(filename_txt, binary=False)
    print('process done')


start_learn(105, '2018-01-02')
