from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# setup flask app
app = Fask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# create route for homepage
@app.route("/") 
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# create a route for scraping, to be a clickable button in the homepage
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code=302)

# Tell Flask to run
if __name__ == "__main__"
    app.run()