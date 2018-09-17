import os
import sys
from flask import Flask
from src.dbutil import get_catalogs

app = Flask(__name__)
app.config.from_pyfile('config.py')
print("started application with app name: ", __name__)

@app.route('/')
def homepage():
    return """
    <!DOCTYPE html>
    <head>
        <title>Product Refresh</title>
        <link rel="stylesheet" href="http://stash.compjour.org/assets/css/foundation.css">
    </head>
    <body style="width: 880px; margin: auto;">  
        <h1>Visible stuff goes here</h1>
        <p>here's a paragraph, fwiw</p>
        <p>And here's an image:</p>
        <a href="https://www.flickr.com/photos/zokuga/14615349406/">
            <img src="http://stash.compjour.org/assets/images/sunset.jpg" alt="it's a nice sunset">
        </a>

        <p>Locations:</p>
        <a href="/places/newyork">new york</a><br/>
        <a href="/places/stanford">stanford</a><br/>
        <a href="/places/tokyo">tokyo</a><br/>

        <p>
            <iframe src="https://player.vimeo.com/video/105955605" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
            <p>
                <a href="https://vimeo.com/105955605">Mary live-codes a JavaScript game from scratch &ndash; Mary Rose Cook at Front-Trends 2014
                </a> from 
                <a href="https://vimeo.com/fronttrends">Front-Trends</a> on <a href="https://vimeo.com">Vimeo</a>.
            </p>

        </p>
        ENVIRONMENT:{env}
    </body>
    """.format(env=os.environ['BUILD_ENV'])

def start_refresh(catalog):
    if (os.environ['BUILD_ENV'] == "development"):
        # refresh run script locally
        os.system("python3 refresh_catalog.py --catalogId {catalogId} --catalogUrl {catalogUrl}".format(catalogId=catalog["hgId"], catalogUrl=catalog["CatalogCSVUrl"]))
        print("process_catalog: {}", catalog["hgId"])
    else:
        # refresh catalog <create a new dyno here>
        print("create new dyno")
    

@app.route('/refresh/<token>')
def refresh_product(token="123"):
    catalogs = dbutil.get_catalogs()
    for catalog in catalogs:
        start_refresh(catalog)
    
    return "Product refresh started"

if (__name__ == '__main__'):
    app.run()