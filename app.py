from flask import Flask, render_template, redirect
import scrape_mars
import pymongo
# from auth import username, password

import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')


app = Flask(__name__)
conn = f'mongodb+srv://{username}:{password}@cluster0.nmehijr.mongodb.net/test'
client = pymongo.MongoClient(conn)

db = client.mars_db
db.collection.drop()

@app.route("/")
def home():
    collection_list = db.collection.find_one()
    return render_template('index.html', collections=collection_list)


@app.route("/scrape")
def scrape():
    listings_data = scrape_mars.scrape()

    db.collection.update_one({}, {"$set":listings_data}, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

