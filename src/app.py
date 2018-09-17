import os
import sys
import requests
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

def create_dyno(dynoCommand):
    print("creating new dyno")
    url = "https://api.heroku.com/apps/grs-product-refresh/dynos"
    data = {
        "body": {
            
            "command": dynoCommand,
            "attach": False,
            "size": "Performance-M",
            "type": "run",
            "force_no_tty": None
        }
    }
    params = {
        "auth": ":{token}".format(token=os.environ['HEROKU_API_KEY'])
    }
    headers = {
        'Accept': 'application/vnd.heroku+json; version=3',
        'Content-type': 'application/json',
        'auth': ":" + os.environ['HEROKU_API_KEY'],
        "Range": 'id ..; max=1000'
    }
    response = requests.post(url, params=params, json=data, headers=headers)
    print(response.status_code)
    print(response.json())

def start_refresh(catalog, token):
    APP_NAME = os.environ['APP_NAME']
    dyno_command = "python3 src/refresh_catalog.py --token {token} --catalogId {catalogId} --catalogUrl {catalogUrl}".format(token=token, catalogId=catalog["hgId"], catalogUrl=catalog["CatalogCSVUrl"])

    if (os.environ['BUILD_ENV'] == "development"):
        # refresh run script locally
        os.system(dyno_command)
        print("process_catalog: {}", catalog["hgId"])
    else:
        # refresh catalog <create a new dyno here>
        # heroku_conn = heroku3.from_key(os.environ['HEROKU_API_KEY'])
        # heroku_app = heroku_conn.apps()[APP_NAME]
        # heroku_app.run_process_detached(APP_NAME, dyno_command, size=1, attach=False, printout=True)
        create_dyno(dyno_command)
        
    

@app.route('/refresh/<token>')
def refresh_product(token="123"):
    catalogs = get_catalogs()
    for catalog in catalogs:
        start_refresh(catalog, token)
    
    return "Product refresh started"

if (__name__ == '__main__'):
    app.run()