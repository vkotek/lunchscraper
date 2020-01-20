# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup as bs

def get_html_javascript(url):

    options = Options()

    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path=r'/usr/bin/chromedriver')
    driver.get(url)
    sleep(1)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    return soup

def get_facebook_posts(soup):

    result = soup.findAll("div", {'data-testid': 'post_message'} )
    posts = []

    for post in result:
        # remove unwanted span element with 'read more' text
        for x in post('span'):
            x.decompose()
        posts.append( post.get_text(separator="\n") )
    return posts

def find_menu_post(posts):
    # Currently returns first post and splits into list
    return posts[0].split("\n")
