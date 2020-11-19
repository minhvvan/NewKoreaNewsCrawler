from korea_news_crawler.articlecrawler import ArticleCrawler
import os

if __name__ == "__main__":
    # print(os.getcwd()+'\chromedriver.exe')
    Crawler = ArticleCrawler()
    Crawler.set_category("IT과학")  # 정치, 경제, 생활문화, IT과학, 사회, 세계 카테고리 사용 가능
    Crawler.set_date_range(2020, 11, 19, 2020, 11, 19)
    Crawler.set_keyword("네이버")
    Crawler.set_captureFlag(True)
    Crawler.start()
