# coding=utf-8
import pymysql.cursors
from textrkr_test import TextRank

bot_id = 'bot1'
sql_query = 'select a.oid, a.aid, a.content from article a where a.content is not null and (select count(*) ' \
            'from summary where art_oid = a.oid and art_aid = a.aid)=0'

conn = pymysql.connect(host='localhost', user='root', password='TIGER', db='NewsSummary', charset='utf8mb4')
cursor = conn.cursor()
cursor.execute(sql_query)

# 왠진 몰라도 pymysql의 쿼리문 답은 tuple 형태의 콤마가 하나 있는 녀석으로 돌아온다. 왜냐구? 나도 모름.
articles_nosumm = cursor.fetchall()

for article in articles_nosumm:
    _art = list(article)
    _oid = _art[0]
    _aid = _art[1]
    tes = TextRank(_art[2])
    summary = tes.summarize()

    try:
        sql_query = 'insert into summary (art_oid, art_aid, userid, content, time) values (%s, %s, %s, %s, NOW())'
        cursor.execute(sql_query, (_oid, _aid, bot_id, summary))
        conn.commit()
    except pymysql.MySQLError as e:
        print('sql error.')
        continue
