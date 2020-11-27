from time import sleep
from bs4 import BeautifulSoup
import calendar
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from korea_news_crawler.exceptions import *

class stockCrawler:
    #생성자 역할 함수
    def __init__(self):
        self.url = "https://search.naver.com/search.naver?ie=UTF-8&sm=whl_hty&query="
        self.comp = []

    def setComp(self,li):
        for item in li:
            self.comp.append(item)


    def getStockChart(self):
        browser = webdriver.Chrome(ChromeDriverManager().install())
        for keyword in self.comp:
            print(keyword)
            
            if(keyword == ''):
                print('Please Check keyword')
                continue
            else:
                self.url = "https://search.naver.com/search.naver?ie=UTF-8&sm=whl_hty&query="+keyword

            browser.get(self.url)
            #element not found error 처리
            try:
                button = browser.find_element_by_xpath('//*[@id="_cs_root"]/div[1]/div/h3/a')
                link = button.get_attribute("href")
                browser.get(link)
                sleep(2)

                element = browser.find_element_by_id('chart_area')
                location = element.location
                y = location.get('y')
                #사진 padding 처리 (y-160)
                browser.execute_script("window.scrollTo(%d,%d);"%(0,y-60))
                sleep(2)
                size = element.size 
                title = keyword + ' 증권정보.png'
                element.screenshot(title)
                # browser.save_screenshot(title)
                # browser.quit()
            except Exception as ex:
                print('Not find element')
                print(ex)
                # browser.quit()
                raise InvalidStock(keyword)


if __name__ == "__main__":
    Crawler = stockCrawler()
    Crawler.setComp(["삼성전자","삼성전자우","카카오"])
    Crawler.getStockChart()