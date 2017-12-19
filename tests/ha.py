from konlpy.tag import Kkma
from konlpy.utils import pprint
from bs4 import BeautifulSoup
import bs4
import urllib.request

from konlpy.tag import Twitter

kkma = Kkma()

OUTPUT_FILE_NAME = 'output.txt'


URL = 'http://news.naver.com/main/read.nhn?' \
      'mode=LPOD&mid=sec&oid=001&aid=0009745229&isYeonhapFlash=Y&rc=N'

# 크롤링 +분석 함수 --> 파이썬 함수는 def 함수명 (매개변수) : 엔터 치고 탭임
def get_text(url):
    source_code_from_URL = urllib.request.urlopen(url)

    #BeautifulSoup개체 : URL을 2번째 매개변수 기준으로 파싱. 'lxml'은 xml 라이브러리. 내장 파서인 html.parser도 가능
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''

    #본문
    for item in soup.find_all('div', {'id' : 'articleBodyContents'}):
        #print(item) #이 선택자의 html 나옴
        children = item.children
        for a in children:
            if(type(a) == bs4.element.NavigableString):
                if(len(a) > 1):
                    text = text + a + '\n'
                    print(a)
                    pprint(kkma.pos(a))

        for pic in item.find_all('span', {'class' : 'end_photo_org'}):
            print(pic.img)
    text = text.replace(u'\xa0', u'')
    return text


def main():
    open_output_file = open(OUTPUT_FILE_NAME, 'w')
    result_text = get_text(URL)
    open_output_file.write(result_text)
    open_output_file.close()


main()

