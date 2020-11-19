from selenium import webdriver 

browser = webdriver.Chrome('.\chromedriver.exe') 
browser.get('https://finance.naver.com/sise/')
element = browser.find_element_by_class_name('box_top_submain2')
# element = browser.find_element_by_id('main_content')
size = element.size 
print(size)
element.screenshot('clcl.png')
