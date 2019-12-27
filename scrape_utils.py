# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
import json
from splinter import Browser
import pandas as pd
import re

def get_mars_weather():
    jsn = requests.get("https://publish.twitter.com/oembed?url=https://twitter.com/MarsWxReport/status/1163403052969336832").json()
    html = jsn['html']
    soup = BeautifulSoup(html,"lxml")
    mars_weather = soup.find("p").get_text()
    mars_weather = re.sub("pic.twitter.+","",mars_weather)
    return mars_weather


def get_mars_featured_image():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    temp_url = soup.find('footer').a.attrs.get('data-fancybox-href')
    return "https://www.jpl.nasa.gov" + temp_url


def get_mars_news():
    url = "https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(url)
    news_items = json.loads(response.text)
    news_title = news_items.get('items')[0].get('title')
    news_paragraph_text = news_items.get('items')[0].get('description')
    return {'news_title': news_title, 'news_paragraph_text':news_paragraph_text}


def get_mars_facts():
    marsfacts_url = "https://space-facts.com/mars/"
    mars_table_list = pd.read_html(marsfacts_url)
    marsfacts_df = mars_table_list[0]
    marsfacts_df.columns = ['fact', 'value']
    return marsfacts_df.to_html(index=False, header=False).replace("\n", "")


def get_mars_images():
    hemisphere_image_urls = []
    hemi_list = ['cerberus_enhanced', 'schiaparelli_enhanced', 'syrtis_major_enhanced', 'valles_marineris_enhanced']

    for hemi in hemi_list:    
        hemi_url = []
        title = hemi.replace("_", " ")
        mars_hemi_url = f"https://astrogeology.usgs.gov/search/map/Mars/Viking/{hemi}"
        request = requests.get(mars_hemi_url)
        soup = BeautifulSoup(request.text, 'lxml')
        hemi_image_list = []
        soupy_list = soup.find_all('a', href=True)   
       
        for a in soupy_list:
            if f'{hemi}.tif/full' in str(a):         
                if str(a) not in hemi_image_list:
                    hemi_image_list.append(str(a))
                    hemi_url = hemi_image_list[0].split("\"")
                    hemisphere_image_urls.append({'title': f'{title}', 'url': hemi_url[1]})                

    return hemisphere_image_urls

# print(get_mars_news())
# print(get_mars_facts())
# print(get_mars_weather())
# print(get_mars_featured_image())
# print(get_mars_images())

# data = db.mycollection.find()
# return render_template('index.html', 
#     weather = data.weather, 
#     images = data.image_list,
# )