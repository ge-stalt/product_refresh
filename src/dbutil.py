import os
import sys
from pymongo import MongoClient
import datetime
from enum import Enum

class EntityCache(Enum):
    GRSProductCatalog = "GRSProductCatalog"
    GRSProducts = "GRSProducts"

def get_db_url(env):
    mongodb_url = "MONGODB_{env}".format(env=env.upper())
    if (os.environ[mongodb_url]):
        return os.environ[mongodb_url]
    else:
        sys.exit("Invalid environment")

def get_db_name(env):
    if (env == "local" or env == "prod"):
        db_name = os.environ["DATABASE"]
    else:
        db_name = "{env}-{database}".format(env=env.upper(), database=os.environ["DATABASE"])
    
    return db_name

def get_db(env):
    """
    Connects to mongo db

    Returns a mongodb connection
    """
    
    mongo_url = get_db_url(env)
    db_name = get_db_name(env)
    client = MongoClient(mongo_url)
    return client[db_name]

def get_catalog_count(db):
    return db[EntityCache.GRSProductCatalog.value].count({})

def get_catalogs(db):
    return db[EntityCache.GRSProductCatalog.value].find({}).limit(1)

def get_catalog_by_id(db, catalogId):
    return db[EntityCache.GRSProductCatalog.value].find_one({"hgId": catalogId})

def update_catalog(db, catalog, status):
    db[EntityCache.GRSProductCatalog.value].update({
        "hgId": catalog["hgId"]
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
    #remove old product items
    db[EntityCache.GRSProducts.value].remove({
        "CURRENT_VERSION": { "$ne": CURRENT_VERSION},
        "Updated": True,
        "ProductCatalogId": catalog["hgId"],
        "StoreFrontId": catalog["StoreFrontId"]
    })

    #set new download to true
    db[EntityCache.GRSProducts.value].update_many({
        "CURRENT_VERSION": CURRENT_VERSION,
        "Updated": False,
        "ProductCatalogId": catalog["hgId"],
        "StoreFrontId": catalog["StoreFrontId"],
    }, {
        "$set": {
            "Updated": True
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
    if (isinstance(product[0], int)):
        productMap = {
            "ProductCatalogId": store["hgId"],
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
            db[EntityCache.GRSProducts.value].insert_one(productMap)

    