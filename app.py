import os
import pymongo
from scrape import scraper
from flask import Flask, render_template
import wget

app = Flask(__name__)

client = pymongo.MongoClient("localhost", 27017)
db = client["mars_data"]
myColl = db["mars"]


@app.route('/')
def get_data():
    news = []
    featured_image_url = ""
    html_table_string = ""
    hemisphere_image_urls = {}
    for x in myColl.find():
        if(x["name"] == "news"):
            news = x["value"]
        elif(x["name"] == "featured_image_url"):
            featured_image_url = x["value"]
        elif(x["name"] == "html_table_string"):
            html_table_string = x["value"]
        elif(x["name"] == "hemisphere_image_urls"):
            hemisphere_image_urls = x["value"]

    if('feat.jpg' not in os.listdir('static')):
        wget.download(featured_image_url, out="static/feat.jpg")

    hemi_list = []
    for key in hemisphere_image_urls:
        hemi_list.append(key)
        if (key + ".jpg" not in os.listdir('static')):
            wget.download(hemisphere_image_urls[key], out=f"static/{key}.jpg")
    return render_template('index.html', news_title=news[0],
                           news_p=news[1], table=html_table_string, hemi_list=hemi_list)


@app.route('/scrape')
def scrape_data():
    print('scraping...')
    x = myColl.delete_many({})
    resp = scraper()
    x = myColl.insert_many(resp)
    return 'Scraped'


if(__name__ == '__main__'):
    app.run(debug=True)
