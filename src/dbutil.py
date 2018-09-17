import os
from pymongo import MongoClient
import datetime

def get_db():
    """
    Connects to mongo db

    Returns a mongodb connection
    """
    mongo_url = os.environ['MONGODB_URL']
    client = MongoClient(mongo_url)
    return client['nulabs']

def get_catalog_count():
    db = get_db()
    productCatalogsCollection = db['productCatalogs']
    return productCatalogsCollection.count({})

def get_catalogs():
    db = get_db()
    productCatalogsCollection = db['productCatalogs']
    return productCatalogsCollection.find({}).limit(3)

def update_catalog(catalogId, status):
    db = get_db()
    productCatalogsCollection = db['productCatalogs']
    productCatalogsCollection.update({
        "hgId": catalogId
    }, {
        "$set": {
            "Status": status,
            "ModifiedDate": int(datetime.datetime.now().timestamp() * 1000)
        }
    })
    return
