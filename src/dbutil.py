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
    return productCatalogsCollection.find({}).limit(1)

def get_catalog_by_id(db, catalogId):
    productCatalogsCollection = db['productCatalogs']
    return productCatalogsCollection.find_one({"hgId": catalogId})

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

def get_cost(value):
    numberDecimals = len(str(value).split(".")[1])
    remain = int(str(value)[-1:])
    if (numberDecimals > 1 and remain > 0):
        cost = round(value + ((10 - remain) / 100), 2)
    else:
        cost = value
    return cost


def enable_new_products(db, catalog, CURRENT_VERSION):
    productCollection = db['Products']
    
    #remove old product items
    productCollection.remove({
        "CURRENT_VERSION": { "$ne": CURRENT_VERSION},
        "Updated": True,
        "StoreFrontId": catalog["StoreFrontId"],
        "CatalogLanguage": catalog["CatalogLanguage"],
        "CatalogCountry": catalog["CatalogCountry"],
        "CatalogName": catalog["CatalogName"],
    })

    #set new download to true
    productCollection.update_many({
        "CURRENT_VERSION": CURRENT_VERSION,
        "Updated": False,
        "StoreFrontId": catalog["StoreFrontId"],
    }, {
        "$set": {
            "Updated": True,
        }
    })


def isValidProduct(data):
    return (data["ProductName"] and
        data["ProductId"] and
        data["ProductCost"] and
        data["ProductImage"] and
        data["ProductImage"].startswith("https://") and
        data["Popularity"] >= 0 and
        data["ProductId"] > 0)

def add_product(db, store, product, CURRENT_VERSION):
    productCollection = db['Products']
    productMap = {
        "CURRENT_VERSION": CURRENT_VERSION,
        "ModifiedDate": int(datetime.datetime.now().timestamp() * 1000),
        "Updated": False,
        "StoreFrontId": store["StoreFrontId"],
        "StoreFrontName": store["StoreFrontName"],
        "CatalogLanguage": store["CatalogLanguage"],
        "CatalogCountry": store["CatalogCountry"],
        "CatalogId": int(store["CatalogId"]),
        "CatalogueId": int(store["CatalogueId"]),
        "CatalogName": store["CatalogName"],
        "ProductId": int(product[0]),
        "ProductName": product[1],
        "ProductDescription": product[2],
        "ProductCategories": str(product[3]).split("|"),
        "ProductBrand": product[4],
        "ProductImage": product[5],
        "Popularity": int(product[6]),
        "ProductCost": int(get_cost(round(float(product[9]) + float(product[10]) + float(product[11]) + float(product[12]), 2)) * store["PointRatio"]),
    }
    # print(productMap)
    if (isValidProduct(productMap)):
        productCollection.insert_one(productMap)

    