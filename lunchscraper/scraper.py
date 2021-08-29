# scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup as bs

def get_html_javascript(url):
    """
        Retrieve the soup from 
    """
    
    options = Options()
    options.headless = True
    
    driver = webdriver.Chrome(options=options, executable_path=r'/usr/bin/chromedriver')
    driver.get(url)
    
    sleep(1)
    html = driver.page_source
    
    return html

def get_fb_posts(html):
    """
        Takes raw html and finds all facebook posts - usually two or so latest posts.
    """
    
    soup = bs(html, 'html.parser')
    result = soup.findAll("div", {'data-testid': 'post_message'} )
    posts = []
    
    for post in result:
        # remove unwanted span element with 'read more' text
        for x in post('span'):
            x.decompose()
        posts.append( post.get_text(separator="\n") )

    return posts

def get_menu_from_posts(posts):
    
    return None