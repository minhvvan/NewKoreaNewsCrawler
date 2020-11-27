from korea_news_crawler.articlecrawler import ArticleCrawler
from korea_news_crawler.covidcrawler import covidCrawler
from korea_news_crawler.stock import stockCrawler
import os

if __name__ == "__main__":
    # stockcrawler = stockCrawler()
    # stockcrawler.setComp(["삼성전자","카카오","LG화학"])
    # stockcrawler.getStockChart()


    Crawler = ArticleCrawler()
    Crawler.set_category("IT과학")  # 정치, 경제, 생활문화, IT과학, 사회, 세계 카테고리 사용 가능
    Crawler.set_date_range(2020, 11, 1, 2020, 11, 30)
    # Crawler.set_keyword("네이버")
    # Crawler.set_captureFlag(True)
    Crawler.start()
    
    # covidcrawler = covidCrawler()
    # covidcrawler.getConfirmed()
