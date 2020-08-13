import requests
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd


def scraper():
    NASA_URL = "https://mars.nasa.gov/news/"
    page = requests.get(NASA_URL, allow_redirects=True)
    soup = BeautifulSoup(page.content, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[0].find('a').text
    news_p = soup.find_all('div', class_='rollover_description_inner')[0].text

    featured_image_url = ""
    with Browser('chrome', headless=True) as browser:
        # Visit URL
        url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(url)
        # Find and click the 'search' button
        button = browser.find_by_id('full_image')
        button.click()
        for img in (browser.find_by_css('.fancybox-image')):
            featured_image_url = img['src']

    MARS_URL = "https://space-facts.com/mars/"
    table = pd.read_html(MARS_URL)
    html_table_string = pd.DataFrame(table[0].set_index(0)).to_html(header=False)

    hemisphere_image_urls = {}
    with Browser('chrome') as browser:
        base_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(base_url)
        for hem in (browser.find_by_css('.description')):
            hemisphere_name = hem.find_by_tag('h3').value
            link = hem.find_by_tag('a')['href']
            hemisphere_image_urls[hemisphere_name] = link

        for hem in hemisphere_image_urls:
            to_visit = hemisphere_image_urls[hem]
            browser.visit(to_visit)
            new_link = browser.find_link_by_text('Sample')['href']
            hemisphere_image_urls[hem] = new_link

    resp = [
        {"_id": 1, "name": "news", "value": [news_title, news_p]},
        {"_id": 2, "name": "featured_image_url", "value": featured_image_url},
        {"_id": 3, "name": "html_table_string", "value": html_table_string},
        {"_id": 4, "name": "hemisphere_image_urls", "value": hemisphere_image_urls}
    ]

    return resp
