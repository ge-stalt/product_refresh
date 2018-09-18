import os
import requests
import argparse
import codecs
from contextlib import closing
import csv
from dbutil import update_catalog, add_product, get_db, get_catalog_by_id, enable_new_products
import datetime

def refresh_catalog(env, catalogId, token):
    print("Refreshing CatalogId: {}".format(catalogId))

    CURRENT_VERSION = int(datetime.datetime.now().timestamp() * 1000)

    db = get_db(env)

    #get catalog
    catalog = get_catalog_by_id(db, catalogId)

    #update status
    update_catalog(db, catalog, "Inprogress")

    #download file
    download_products(db, catalog, token, CURRENT_VERSION)

    #enable new projdcts
    enable_new_products(db, catalog, CURRENT_VERSION)

    #update status
    update_catalog(db, catalog, "Completed")



def download_products(db, catalog, token, CURRENT_VERSION):
    
    session = requests.Session()

    with closing(session.get(catalog["CatalogCSVUrl"], stream=True, cookies={'grs': token})) as r:
        reader = csv.reader(codecs.iterdecode(r.iter_lines(), encoding='ISO-8859-1'))
        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            elif row != [] and len(row) > 1 and line_count > 0:
                add_product(db, catalog, row, CURRENT_VERSION)
                line_count += 1
            else:
                print(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('--catalogId', help='A required string catalogId argument')
    parser.add_argument('--token', help='A required string token argument')
    parser.add_argument('--env', help='A required string env argument')
    args = parser.parse_args()
    refresh_catalog(args.env, args.catalogId, args.token)