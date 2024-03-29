import subprocess
import urllib.request

from bs4 import BeautifulSoup
from storage import Storage


ARUODAS_URL = 'http://www.aruodas.lt/butu-nuoma/vilniuje?FAreaOverAllMin=40&FDistrict=1&FOrdDir=did&FPriceMax=1000&FPriceMin=500&FQuartal%5B0%5D=1&FQuartal%5B1%5D=16&FQuartal%5B2%5D=132&FQuartal%5B3%5D=18&FQuartal%5B4%5D=23&FRegion=461&FRoomNumMax=2&act=MakeSearch&detailed_search=1&mod=Siulo&obj=4'
ARUODAS_KEY = 'aruodas'

SKELBIU_URL = 'http://www.skelbiu.lt/skelbimai/?cities=465&distance=0&mainCity=0&search=1&category_id=322&keywords=&type=0&orderBy=-1&detailsSearch=1&building=0&year_min=&year_max=&floor_min=&floor_max=&floor_type=0&cost_min=500&cost_max=1000&status=0&space_min=40&space_max=iki&rooms_min=&rooms_max=2&search=Veskite+pavadinim%C4%85&selectedCity=1&selectedCity=1&district=1&quarter=1%2C16%2C132%2C18%2C23&streets=0&ignorestreets=0'
SKELBIU_KEY = 'skelbiu'

DATABASE = 'data.db'

CHROME_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    
# Parsing the pages

def parse_page(url):
    response = urllib.request.urlopen(url).read()
    return BeautifulSoup(response)

def retrieve_aruodas_adverts(page):
    adverts = {}        
    for row_tag in page.table.tbody('tr'):
        for cell_tag in row_tag('td'):
            cell_class = cell_tag.get('class')
            if (cell_class == ['list-adress']):
                href = cell_tag.a.get('href')
                link = href.split('?')[0]
                last_index_of_minus = link.rfind("-")
                objectId = link[last_index_of_minus - 1:len(link)]
            elif(cell_class == ['list-price']):
                price_split = cell_tag.b.string.split(' ')
                if len(price_split) == 3:
                    price = price_split[0] + price_split[1]
                else:
                    price = price_split[0]
        adverts[objectId] = int(price)
    return adverts

def retrieve_skelbiu_adverts(page):
    adverts = {}
    for advert_row in page.td(skelbiu_advert_div):
        tag_id = advert_row.get('id')
        objectId = tag_id[3:len(tag_id)]
        price = advert_row.find(skelbiu_price_div).contents[0].replace('\t', '').replace('Lt', '').replace(' ', '').replace('\r', '').replace('\n', '')
        adverts[objectId] = int(price)
    return adverts
        
def skelbiu_advert_div(tag):
    if tag.has_key("class"):
        tagclass = tag.get('class')
        return tagclass == ['simpleAds'] or tagclass == ['popularAds'] or tagclass == ['boldAds']
    else:
        return False

def skelbiu_price_div(tag): 
    if tag.has_key('class'):
        tagclass = tag.get('class')
        return tagclass == ['adsPrice']
    else:
        return False   

def retrieve_adverts(page_key, pageURL):
    page = parse_page(pageURL)
    if page_key == ARUODAS_KEY:
        return retrieve_aruodas_adverts(page)
    if page_key == SKELBIU_KEY:
        return retrieve_skelbiu_adverts(page)
    else:
        return None
    
# Open in browser part
    
def open_advert(page_key, objectId):
    if page_key == ARUODAS_KEY:
        objectURL = 'http://www.aruodas.lt/skelbimai/' + objectId
    if page_key == SKELBIU_KEY:
        objectURL = 'http://www.skelbiu.lt/' + objectId + '.html'
    subprocess.Popen([CHROME_PATH, objectURL])
        
def open_all(page_key, adverts):
    for key in adverts.keys():
        open_advert(page_key, key)

# result comparison

def process_page(pageURL, page_key, storage):
    print('Processing page ' + page_key)
    
    stored = storage.get_items(page_key)
    print('Stored adverts')
    print(stored)
    
    retrieved = retrieve_adverts(page_key, pageURL)
    print('Received adverts:')
    print(retrieved)
    
    additions = {}
    updates = {}
    removals = {}
    for objectId, price in retrieved.items():
        if objectId in stored:
            if price != stored[objectId]:
                updates[objectId] = price
        else:
            additions[objectId] = price
    
    for objectId, price in stored.items():
        if not objectId in retrieved:
            removals[objectId] = price
    
    print('Inserting items: ')
    print(additions)
    storage.insert_items(page_key, additions)
    print('Updating items: ')
    print(updates)
    storage.change_items(page_key, updates)
    if len(removals) != len(stored):  # we don't want to remove all stored adverts if there was a page reading error
        print('Removing items: ')
        print(removals)
        storage.remove_items(page_key, removals)
  
    open_all(page_key, additions)
    open_all(page_key, updates)
    open_all(page_key, removals)
    
storage = Storage(DATABASE)

process_page(ARUODAS_URL, ARUODAS_KEY, storage)
process_page(SKELBIU_URL, SKELBIU_KEY, storage)
