from korea_news_crawler.articlecrawler import ArticleCrawler
from korea_news_crawler.covidcrawler import covidCrawler
from korea_news_crawler.stock import stockCrawler
import os

if __name__ == "__main__":
    # print(os.getcwd()+'\chromedriver.exe')
    # Crawler = ArticleCrawler()
    # Crawler.set_category("IT과학")  # 정치, 경제, 생활문화, IT과학, 사회, 세계 카테고리 사용 가능
    # Crawler.set_date_range(2020, 11, 22, 2020, 11, 22)
    # Crawler.set_keyword("네이버")
    # Crawler.set_captureFlag(True)
    # Crawler.start()
    # covidcrawler = covidCrawler()
    # covidcrawler.getConfirmed()
    stockcrawler = stockCrawler()
    stockcrawler.getStockChart("LG화학")
