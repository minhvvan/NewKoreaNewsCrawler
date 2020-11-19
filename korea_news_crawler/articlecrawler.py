#!/usr/bin/env python
# -*- coding: utf-8, euc-kr -*-


#사용 모듈
from time import sleep
from bs4 import BeautifulSoup
from multiprocessing import Process
from korea_news_crawler.exceptions import *
from korea_news_crawler.articleparser import ArticleParser
from korea_news_crawler.writer import Writer
import os
import platform
import calendar
import requests
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#크롤러 클래스
class ArticleCrawler(object):
    #생성자 역할 함수
    #Category와 date등 주요 변수들 생성
    def __init__(self):
        self.categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, 
                            '오피니언': 110,'politics': 100, 'economy': 101, 'society': 102, 'living_culture': 103, 
                           'world': 104, 'IT_science': 105,'opinion': 110}
        self.selected_categories = []
        self.date = {'start_year': 0, 'start_month': 0, 'start_date':0, 'end_year': 0, 'end_month': 0, 'end_date': 0}
        self.user_operating_system = str(platform.system())
        self.keyword = ""
        self.captureFlag = False
        # self.browser = webdriver.Chrome(ChromeDriverManager().install())


    #Category 설정 함수
    def set_category(self, *args):
        for key in args:
            if self.categories.get(key) is None:
                raise InvalidCategory(key)
        self.selected_categories = args

    #keyword 설정 함수
    def set_keyword(self, str):
        self.keyword = str

    #captureFlag 설정 함수
    def set_captureFlag(self, flag):
        self.captureFlag = flag

    #크롤링할 기사 날짜 설정
    def set_date_range(self, start_year, start_month, start_date, end_year, end_month, end_date):
        args = [start_year, start_month, start_date, end_year, end_month, end_date]
        if start_year > end_year:
            raise InvalidYear(start_year, end_year)
        if start_month < 1 or start_month > 12:
            raise InvalidMonth(start_month)
        if end_month < 1 or end_month > 12:
            raise InvalidMonth(end_month)
        if start_date < 1 or start_date > 32:
            raise InvalidDate(start_date)
        if end_date < 1 or end_date > 32:
            raise InvalidDate(end_date)
        if start_year == end_year and start_month > end_month:
            raise OverbalanceMonth(start_month, end_month)
        if start_year == end_year and start_date > end_date:
            raise OverbalanceMonth(start_date, end_date)
        for key, date in zip(self.date, args):
            self.date[key] = date
        print(self.date)

    #url 설정 함수
    @staticmethod
    def make_news_page_url(category_url, start_year, end_year, start_month, end_month, start_date, end_date):
        made_urls = []
        #전달받은 기간동안 수행
        for year in range(start_year, end_year + 1):
            if start_year == end_year:
                year_startmonth = start_month
                year_endmonth = end_month
            else:
                if year == start_year:
                    year_startmonth = start_month
                    year_endmonth = 12
                elif year == end_year:
                    year_startmonth = 1
                    year_endmonth = end_month
                else:
                    year_startmonth = 1
                    year_endmonth = 12
            
            for month in range(year_startmonth, year_endmonth + 1):
                if year_startmonth == year_endmonth:
                    for month_day in range(1,  end_date + 1):
                        if len(str(month)) == 1:
                            month = "0" + str(month)
                        if len(str(month_day)) == 1:
                            month_day = "0" + str(month_day)
                else:
                    for month_day in range(1, calendar.monthrange(year, month)[1] + 1):
                        if len(str(month)) == 1:
                            month = "0" + str(month)
                        if len(str(month_day)) == 1:
                            month_day = "0" + str(month_day)
                        
                # 날짜별로 Page Url 생성
                url = category_url + str(year) + str(month) + str(month_day)
                # 전체 페이지 설정(Redirect)
                totalpage = ArticleParser.find_news_totalpage(url + "&page=10000")
                print(totalpage)
                for page in range(1, totalpage + 1):
                    made_urls.append(url + "&page=" + str(page))
                    
        return made_urls

    #data를 받아오는 함수
    @staticmethod
    def get_url_data(url, max_tries=10):
        remaining_tries = int(max_tries)
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
        while remaining_tries > 0:
            try:
                return requests.get(url,headers=headers)
            except requests.exceptions:
                sleep(60)
            remaining_tries = remaining_tries - 1
        raise ResponseTimeout()

    #crawling 함수
    def crawling(self, category_name):
        # Multi Process PID
        print(category_name + " PID: " + str(os.getpid()))    

        writer = Writer(category_name=category_name, date=self.date)

        # 기사 URL 형식
        url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + str(self.categories.get(category_name)) + "&date="

        # 설정 기간 동안 crawling
        day_urls = self.make_news_page_url(url, self.date['start_year'], self.date['end_year'], 
                    self.date['start_month'], self.date['end_month'], self.date['start_date'], self.date['end_date'] )
        print(category_name + " Urls are generated")
        print("The crawler starts")

        for URL in day_urls:

            regex = re.compile("date=(\d+)")
            news_date = regex.findall(URL)[0]

            request = self.get_url_data(URL)

            document = BeautifulSoup(request.content, 'html.parser')

            # 각 페이지에 있는 기사들 가져오기
            post_temp = document.select('.newsflash_body .type06_headline li dl')
            post_temp.extend(document.select('.newsflash_body .type06 li dl'))
            
            # 각 페이지에 있는 기사들의 url 저장
            post = []
            for line in post_temp:
                post.append(line.a.get('href')) # 해당되는 page에서 모든 기사들의 URL을 post 리스트에 넣음
            del post_temp

            for content_url in post:  # 기사 URL
                # 크롤링 대기 시간
                sleep(0.01)
                
                # 기사 HTML 가져옴
                request_content = self.get_url_data(content_url)
                try:
                    document_content = BeautifulSoup(request_content.content, 'html.parser')
                except:
                    continue


                try:
                    # 기사 제목 가져옴
                    tag_headline = document_content.find_all('h3', {'id': 'articleTitle'}, {'class': 'tts_head'})
                    text_headline = ''  # 뉴스 기사 제목 초기화
                    text_headline = text_headline + ArticleParser.clear_headline(str(tag_headline[0].find_all(text=True)))
                    
                    #keyword 검사
                    if not self.keyword in text_headline:
                        continue

                    if not text_headline:  # 공백일 경우 기사 제외 처리
                        continue

                    # 기사 본문 가져옴
                    tag_content = document_content.find_all('div', {'id': 'articleBodyContents'})
                    text_sentence = ''  # 뉴스 기사 본문 초기화
                    text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))

                    #keyword 검사
                    if not self.keyword in text_sentence:
                        continue
                    if not text_sentence:  # 공백일 경우 기사 제외 처리
                        continue

                    # 기사 언론사 가져옴
                    tag_company = document_content.find_all('meta', {'property': 'me2:category1'})
                    text_company = ''  # 언론사 초기화
                    text_company = text_company + str(tag_company[0].get('content'))
                    if not text_company:  # 공백일 경우 기사 제외 처리
                        continue

                    # #사진 저장
                    if(self.captureFlag):
                        browser = webdriver.Chrome(ChromeDriverManager().install())
                        # browser.maximize_window()
                        browser.get(content_url)
                        #element not found error 처리
                        try:
                            element = browser.find_element_by_class_name('end_photo_org')
                            location = element.location
                            y = location.get('y')
                            #사진 padding 처리 (y-60)
                            browser.execute_script("window.scrollTo(%d,%d);"%(0,y-60))
                            size = element.size 
                            title = text_headline+'.png'
                            #기사 제목으로 사진제목 설정
                            element.screenshot(title)
                        except Exception as ex:
                            print('Not find element')
                    
                        
                    # CSV 작성
                    wcsv = writer.get_writer_csv()
                    wcsv.writerow([news_date, category_name, text_company, text_headline, text_sentence, content_url])
                    
                    print('작성완료')

                    del text_company, text_sentence, text_headline
                    del tag_company 
                    del tag_content, tag_headline
                    del request_content, document_content

                except Exception as ex:
                    del request_content, document_content
                    pass
        writer.close()

    # crawling 시작 함수
    def start(self):
        # MultiProcess crawling 시작
        for category_name in self.selected_categories:
            proc = Process(target=self.crawling, args=(category_name,))
            proc.start()

#test용
if __name__ == "__main__":
    Crawler = ArticleCrawler()
    Crawler.set_category("생활문화", "IT과학")
    Crawler.set_date_range(2017, 1, 2018, 4)
    Crawler.start()
