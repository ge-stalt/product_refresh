import os
import requests
import argparse
from helpers.db_util import update_catalog

def refresh_catalog(catalogId, catalogUrl):
    #update status
    print("CatalogId: {} <---> catalogUrl: {}".format(catalogId, catalogUrl))
    # update_catalog(catalog["hgId"], "Inprogress")
    #download file
    #save document
    #update status

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('--catalogId', help='A required string catalogId argument')
    parser.add_argument('--catalogUrl', help='A required string catalogUrl argument')
    args = parser.parse_args()
    refresh_catalog(args.catalogId, args.catalogUrl)