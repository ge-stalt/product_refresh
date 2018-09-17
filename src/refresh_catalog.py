import os
import requests
import argparse
import codecs
from contextlib import closing
import csv
from dbutil import update_catalog, add_product, get_db, get_catalog_by_id
import datetime

def refresh_catalog(catalogId, token):
    print("Refreshing CatalogId: {}".format(catalogId))

    #update status
    update_catalog(catalogId, "Inprogress")

    #download file
    get_products(catalogId, token)

    #update status
    update_catalog(catalogId, "Completed")

def get_products(catalogId, token):
    
    CURRENT_VERSION = int(datetime.datetime.now().timestamp() * 1000)

    session = requests.Session()

    db = get_db()

    catalog = get_catalog_by_id(db, catalogId)

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
    args = parser.parse_args()
    refresh_catalog(args.catalogId, args.token)