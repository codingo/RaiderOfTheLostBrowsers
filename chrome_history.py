import os
import sqlite3
import operator
from collections import OrderedDict

# website to analyse
site="yahoo.com"


def parse(url):
    try:
        parsed_url_components = url.split('//')
        sublevel_split = parsed_url_components[1].split('/', 1)
        domain = sublevel_split[0].replace("www.", "")
        return domain
    except:
        False
    
# path to user's history database (Chrome)
data_path = os.path.expanduser('~')+"\AppData\Local\Google\Chrome\User Data\Default"
files = os.listdir(data_path)

history_db = os.path.join(data_path, 'history')

# querying the db
c = sqlite3.connect(history_db)
cursor = c.cursor()
select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
cursor.execute(select_statement)

results = cursor.fetchall()

sites_count = {}
fl=[]
for url, count in results:
    url = parse(url)
    if site in str(url):
        # print url
        if url not in fl:
            fl.append(url)
print("Results:")
print(fl)
