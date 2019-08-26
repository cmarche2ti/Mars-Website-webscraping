from flask import Flask, render_template, redirect
import scrape_utils


# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

@app.route('/')
def index():
    # Query database for each item
    # return items and render homepage for mars website
    weather_cursor = db.mars.find({},{'weather':1})
    for cursor in weather_cursor:
        weather = cursor
    news_cursor = db.mars.find({},{'mars_news':1})
    for cursor in news_cursor:
        news = cursor
    facts_cursor = db.mars.find({},{'mars_facts':1})
    for cursor in facts_cursor:
        facts = cursor
    featured_cursor = db.mars.find({},{'featured_image':1})
    for cursor in featured_cursor:
        featured = cursor
    images_cursor = db.mars.find({},{'mars_images':1})
    for cursor in images_cursor:
        images = cursor
    
    return render_template('index.html', 
            weather = weather, 
            news = news, 
            facts = facts, 
            featured = featured,
            images = images)

@app.route('/scrape')
def mars_scrape():
    # start with an empty collection
    db.mars.drop
    # code to scrape each website here
    to_insert = {
        "weather": scrape_utils.get_mars_weather(),
        "featured_image": scrape_utils.get_mars_featured_image(),
        "mars_news": scrape_utils.get_mars_news(),
        "mars_facts": scrape_utils.get_mars_facts(),
        "mars_images": scrape_utils.get_mars_images()
        }
    db.mars.insert_one(to_insert)    
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)