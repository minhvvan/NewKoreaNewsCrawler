from selenium import webdriver 

browser = webdriver.Chrome('.\chromedriver.exe') 
browser.get('http://www.google.com/') 
browser.save_screenshot('screenie.png')
