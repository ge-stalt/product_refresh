import os
import requests
import argparse
from dbutil import update_catalog

def refresh_catalog(catalogId, catalogUrl, token):
    print("CatalogId: {} <---> catalogUrl: {}".format(catalogId, catalogUrl))
    #update status
    update_catalog(catalogId, "Inprogress")
    #download file
    #save document
    #update status

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('--catalogId', help='A required string catalogId argument')
    parser.add_argument('--catalogUrl', help='A required string catalogUrl argument')
    parser.add_argument('--token', help='A required string token argument')
    args = parser.parse_args()
    refresh_catalog(args.catalogId, args.catalogUrl, args.token)