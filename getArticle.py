# -*- coding: utf-8 -*-
from konlpy.tag import Twitter
from konlpy.utils import pprint
from bs4 import BeautifulSoup
import bs4
import urllib.request
from textrkr_test import TextRank
import math
import numpy
import operator

twt = Twitter()

OUTPUT_FILE_NAME = 'output.txt'

URL = 'http://news.naver.com/main/read.nhn?oid=001&aid=0009767851'


# 크롤링 +분석 함수 --> 파이썬 함수는 def 함수명 (매개변수) : 엔터 치고 탭임
def get_text(url):
    source_code_from_URL = urllib.request.urlopen(url)

    # BeautifulSoup개체 : URL을 2번째 매개변수 기준으로 파싱. 'lxml'은 xml 라이브러리. 내장 파서인 html.parser도 가능
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''

    for title in soup.find_all('h3',{'id':'articleTitle'}):
        children = title.children
        for a in children:
            if (type(a) == bs4.element.NavigableString):
                if (len(a) > 1):
                    text = text + a + '\n\n\n'
                    print(a)
                    pprint(twt.pos(a))

    text = text.replace(u'\xa0', u'')

    for item in soup.find_all('div', {'id': 'articleBodyContents'}):
        # print(item) #이 선택자의 html 나옴
        children = item.children
        for a in children:
            if type(a) == bs4.element.NavigableString:
                if len(a) > 1:
                    text = text + a + '\n'
                    print(a)
                    pprint(twt.pos(a))
        for pic in item.find_all('span', {'class': 'end_photo_org'}):
            print(pic.img)
    text = text.replace(u'\xa0', u'')
    return text


def main():
    open_output_file = open(OUTPUT_FILE_NAME, 'w')
    result_text = get_text(URL)
    tes = TextRank(result_text)
    print('\n---------요약결과----------\n')
    print(tes.summarize(4))
    print('\n\n----------nouns----------\n' + str(tes.nouns) + '\n')
    _res = {}
    _tots = len(tes.sentences)
    for key, count in tes.bow.items():
        _bigD = 0
        _data = []
        for stb in tes.sentences:
            if stb.bow[key] >0:
                _bigD += 1
        for stc in tes.sentences:
            if stc.bow[key] > 0:
                _idf = math.log(_tots/_bigD, 2)
                _tf = math.log(stc.bow[key] + 1, 2)
                _data.append(_tf * _idf)

        _avg = numpy.average(_data)
        _var = numpy.var(_data)
        listk = key + '- number : ' + str(_bigD) + ', avg : ' + str(_avg) + ', variance : ' + str(_var)
        _res.update({listk: _avg})
    _res = sorted(_res.items(), key=operator.itemgetter(1))
    for a in _res:
        print(a[0])

    open_output_file.write(result_text)
    open_output_file.close()


main()
