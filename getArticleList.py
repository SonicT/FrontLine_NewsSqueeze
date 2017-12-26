import bs4
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pymysql.cursors
import datetime
import time
from urllib.parse import urlparse, parse_qs
from pymysql.err import MySQLError

# os : 시스템이 돌아가는 절대경로를 얻기 위한 과정. 크롬 드라이버가 탑재되어 있으므로 이를 통해 경로를 얻었다.
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

res = {}


def get_art_list(sid, date=datetime.date.today()):
    url = 'http://news.naver.com/main/main.nhn?sid1=' + str(sid)

    # 프로젝트 경로에서 크롬 드라이버 찾기
    driver = webdriver.Chrome(dir_path  + '/chromedriver/chromedriver.exe')

    # 시동을 위해 기다려줘야 한다는 설명이 있다.... 근데 이만큼 기다리는거 맞아?
    driver.implicitly_wait(3)

    driver.get(url)
    driver.implicitly_wait(2)

    # selenium 라이브러리의 웹드라이버는 beautifulSoup와 호환되지 않는 별개의 클래스다. 소스를 긁어서 변환하자.
    sp = bs4.BeautifulSoup(driver.page_source, 'lxml')

    soup = sp.find('div', {'id': 'main_content'})

    # 카테고리가 정해진 메인 기사들 None이 됨. 날짜가 당일일 경우에만 유효하다.
    if date == datetime.date.today():
        print("\n\n -------------기사 최고 메인 -------------- \n\n")
        for item in soup.find_all('div', {'class': "section_headline headline_subordi"}):
            keyword = item.find('h5', {'class': 'compo_headtxt'})

            # 참고 : 키워드가 구성되지 않은 섹션도 있다. 이럴 경우 예외처리를 통해 '키워드 없음'으로 저장해야겠음.
            if keyword is not None:
                subjtitle = keyword.find('a', {'class' : 'compo_linkhead'})
                if subjtitle is not None:
                    print(subjtitle.text)
                else:
                    subjtitle = keyword.text
                    print(subjtitle)
            else:
                print('No Subject')
            print('\n[')
            for list in item.find_all('li'):
                link = list.find('a', href=True)
                if link is not None:
                    title = link.text.replace('\n', '')
                    print(title + ' : ' + link['href'])
                    res.update({str(link['href']) : title})
            print(']\n')

        # 일반 메인 기사들
        print("\n\n -------------주요기사 일반 -------------- \n\n")
        for item_indepTitle in soup.find_all('div', {'class': 'section_headline headline_pht_small'}):
            for component in item_indepTitle.find_all('dl'):
                keyword = component.find_all('dt')
                if (len(keyword) > 1) and keyword is not None:
                    art_title = keyword[1].text.replace('\n','')
                    art_link = keyword[1].find('a', href=True)
                    if art_link is not None:
                        print(art_title + ' : ' + art_link['href'])
                        res.update({str(art_link['href']): art_title})
                elif keyword is not None:
                    art_title = keyword[0].text
                    art_link = keyword[0].find('a', href=True)
                    if art_link is not None:
                        print(art_title + ' : ' + art_link['href'])
                        res.update({str(art_link['href']): art_title})

        # 왜 따로 분류되었는지 모른 2의 일족
        print("\n\n -------------주요기사 일반 2-------------- \n\n")
        for item_indepTitle2 in soup.find_all('div', {'class': 'section_headline headline_pht_small2'}):
            for component in item_indepTitle2.find_all('dl'):
                keyword = component.find_all('dt')
                if (len(keyword) > 1) and keyword is not None:
                    art_title = keyword[1].text.replace('\n','')
                    art_link = keyword[1].find('a', href=True)
                    if art_link is not None:
                        print(art_title + ' : ' + art_link['href'])
                        res.update({str(art_link['href']): art_title})

                elif keyword is not None:
                    art_title = keyword[0].text.replace('\n','')
                    art_link = keyword[0].find('a', href=True)
                    if art_link is not None:
                        print(art_title + ' : ' + art_link['href'])
                        res.update({str(art_link['href']): art_title})

        # 왜 따로 분류되었는지 모른 3의 일족
        print("\n\n -------------주요기사 일반 3-------------- \n\n")
        for item_indepTitle3 in soup.find_all('div', {'class': 'section_headline headline_pht_small3'}):
            for component in item_indepTitle3.find_all('dl'):
                keyword = component.find_all('dt')
                if (len(keyword) > 1) and keyword is not None:
                    art_title = keyword[1].text.replace('\n','')
                    art_link = keyword[1].find('a', href=True)
                    if art_link is not None:
                        print(art_title + ' : ' + art_link['href'])
                        res.update({str(art_link['href']): art_title})

                elif keyword is not None:
                    art_title = keyword[0].text.replace('\n','')
                    art_link = keyword[0].find('a', href=True)
                    if art_link is not None:
                        print(art_title + ' : ' + art_link['href'])
                        res.update({str(art_link['href']): art_title})

        # 굳이 왜 분류했는지 모르는 small 컨텐트
        print("\n\n -------------주요기사 작음 2_1-------------- \n\n")
        for item_small in soup.find_all('div', {'class': 'section_headline headline_pht_small2_1'}):
            for component in item_small.find_all('dl'):
                keyword = component.find_all('dt')
                if (len(keyword) > 1) and keyword is not None:
                    art_title = keyword[1].text.replace('\n', '')
                    art_link = keyword[1].find('a', href=True)
                    if art_link is not None:
                        print(str(art_title) + ' : ' + art_link['href'])
                        res.update({str(art_link['href']): str(art_title)})

                elif keyword is not None:
                    art_title = keyword[0].text.replace('\n','')
                    art_link = keyword[0].find('a', href=True)
                    if (art_link is not None):
                        print(str(art_title) + ' : ' + art_link['href'])
                        res.update({art_link['href']: str(art_title)})

    # '페이징 처리'로 볼 수 있는 기사들. 여기서부턴 이전 날짜의 링크들도 저장된다.
    # 자바스크립트로 생성하는 것인지, jsp에서 서버응답을 기다리는 것인지 여튼 여기는 그냥 긁어오는 html태그로는 보이지 않는다.
    # 처음에는 많이들 사용하는 phantomJS headless client를 사용하려 했으나, 루비랑 사파이어? 등등 다 설치해야 한다고 그래서 그냥 버렸다(윈도만 싫어하는 거지같은 세상)
    # 대안으로 크롬의 크롬드라이버를 사용하여 실제로는 사용자를 위해 실행되지 않는 프로그램(headless client)을 대체.

    print("\n\n --------------일반 기사(페이징 처리된 '더 보기' 기사들)-------------- \n\n")
    page = 1  # 일단 1page부터 시작임. 암튼 그럼.
    not_end = True  # while 루프의 해제
    # !!특정 페이지 안에도 해당 페이지 내에서 많이 본 기사인'헤드라인'으로 구성된 주요 뉴스가 따로 있긴 하다. 관련없이 그냥 모으기로 함.

    while not_end:
        # '다음 페이지' 버튼을 찾는다
        _nbtn = soup.find('a', {'class': '_paging next'})

        # 페이지 넘어가는 href. 해당 페이지 번호는 href처리가 안되어있다.
        # 1-10까지 있을 경우, 해당 페이지 숫자 1개를 제외하고 있어야 하는 _paging 클래스 버튼 수는 9개!
        _pages = soup.find('div', {'id': 'paging'}).find_all('a', {'class': '_paging'})

        if ((page - 1) % 10 != 0) and (len(_pages) < (page% 10)):
            print('\n\n---------------STOP!!!!-------------\n\n')
            break

        if page != 1 and ((page -1) % 10 == 0) and _nbtn is None:
            print('\n\n---------------STOP!!!!-------------\n\n')
            break

        nurl= url + '#&date=' + str(date) + ' 00:00:00&page=' + str(page)
        print('\n\n---------------page' + str(page)+'------------\n\n')
        driver.get(nurl)
        WebDriverWait(driver, 2)
        time.sleep(1)

        soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

        _ul = soup.find('div', {'id': 'section_body'})

        for _articles in _ul.find_all('li'):
            _sub = _articles.find('a', href=True)
            _link = _sub['href']
            if _link.startswith('/'):
                _link = 'http://news.naver.com' + _link
            print(_sub.text + ' : ' + _link)
            res.update({_link: _sub.text})

        page = page + 1

    driver.implicitly_wait(3)

    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='TIGER',
                           db='NewsSummary',
                           charset='utf8mb4')
    for url, title in res.items():
        cursor = conn.cursor()
        query = parse_qs(urlparse(url).query)
        try:
            oid = query['oid']
            aid = query['aid']
        except:
            print(url)
        sql = 'INSERT INTO Link (sid, oid, aid, url, title, date) VALUES (%s,%s,%s,%s,%s,%s)'

        try:
            cursor.execute(sql, (sid, oid, aid, url, title, str(date)))
            conn.commit()
        except MySQLError:
            print('중복있나봄 넘어갈게여')
            continue
    print(cursor.lastrowid)
    conn.close()


# 테스트 : sid=100 은 정치
# 왠만해선 네이버에서 제공하는 뉴스 카테고리를 십분 활용해보고자, html소스코드를 좀 더 파보고 있다.
get_art_list(101)
