import os
import sys
from flask import Flask
from src.dbutil import get_catalogs
import heroku3

app = Flask(__name__)
app.config.from_pyfile('config.py')
print("started application with app name: ", __name__)

@app.route('/')
def homepage():
    return """
    <!DOCTYPE html>
    <head>
        <title>Product Refresh API Server</title>
    </head>
    <body style="width: 880px; margin: auto;">  
        <h1>Product Refresh API Server</h1>
        ENV:{env}
    </body>
    """.format(env=os.environ['BUILD_ENV'])

def start_refresh(catalog, token):
    if (os.environ['BUILD_ENV'] == "development"):
        # refresh run script locally
        os.system("python3 src/refresh_catalog.py --token {token} --catalogId {catalogId} --catalogUrl {catalogUrl}".format(token=token, catalogId=catalog["hgId"], catalogUrl=catalog["CatalogCSVUrl"]))
        print("process_catalog: {}", catalog["hgId"])
    else:
        heroku_conn = heroku3.from_key(os.environ['HEROKU_API_KEY'])
        # refresh catalog <create a new dyno here>
        print("create new dyno")
    

@app.route('/refresh/<token>')
def refresh_product(token="123"):
    catalogs = get_catalogs()
    for catalog in catalogs:
        start_refresh(catalog, token)
    
    return "Product refresh started"

if (__name__ == '__main__'):
    app.run()