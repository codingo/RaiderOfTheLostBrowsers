import os
import sqlite3
import operator
import sys
from collections import OrderedDict
from argparse import ArgumentParser


VERSION = '0.1 UNSTABLE'

def parse(url):
    try:
        parsed_url_components = url.split('//')
        sublevel_split = parsed_url_components[1].split('/', 1)
        domain = sublevel_split[0].replace("www.", "")
        return domain
    except:
        False
    
def query_database(search_term):
    # path to user's history database (Chrome)
    data_path = os.path.expanduser('~') + str("\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    files = os.listdir(data_path)
    history_db = os.path.join(data_path, 'history')

    # querying the db
    c = sqlite3.connect(history_db)
    cursor = c.cursor()
    statement = """     SELECT DISTINCT urls.url, count(urls.visit_count) 
                        FROM            urls, visits 
                        WHERE           urls.id = visits.url 
                        GROUP BY        urls.url;"""
    cursor.execute(statement)

    results = cursor.fetchall()

    sites_count = {}
    fl=[]
    for url, count in results:
        url = parse(url)
        if search_term in str(url):
            # print url
            if url not in fl:
                fl.append(url)
    print("Results:")
    print(fl)

def main():
    parser = ArgumentParser()
    parser.add_argument("-t", dest="term", help="Provide a term to search for in URL's. Ex: https://test.sharepoint.com")
    arguments = parser.parse_args()

    if len(sys.argv) == 1:
        parser.error("No arguments given. Displaying all websites available.")

    query_database(arguments.term)

if __name__ == "__main__":
    main()