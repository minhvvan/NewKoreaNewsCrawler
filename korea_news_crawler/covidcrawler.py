#사용 모듈
from time import sleep
from bs4 import BeautifulSoup
import calendar
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class covidCrawler(object):
    #생성자 역할 함수
    def __init__(self):
        self.url = "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun="


    def getConfirmed(self):
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get(self.url)
        #element not found error 처리
        try:
            element = browser.find_element_by_id('patient_trend')
            location = element.location
            y = location.get('y')
            #사진 padding 처리 (y-60)
            browser.execute_script("window.scrollTo(%d,%d);"%(0,y-60))
            sleep(2)
            size = element.size 
            title = '일일 및 누적 확진환자 추세.png'
            element.screenshot(title)
            browser.quit()
        except Exception as ex:
            print('Not find element')


if __name__ == "__main__":
    Crawler = covidcrawler()
    Crawler.getConfirmed()