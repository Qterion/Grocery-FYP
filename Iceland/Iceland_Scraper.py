from bs4 import BeautifulSoup
import time
import requests
import csv
import os
import urllib.request
from urllib.parse import urlparse


def simplify(item):
    return item.get_text().strip()

def scrape_page(url):
    result=requests.get(url)
    doc=BeautifulSoup(result.content,"html.parser")
    return doc

def create_file():
    with open("iceland.csv","w", newline='', encoding="utf-8") as csvfile:
        writer=csv.writer(csvfile)
    return writer
        
def write_line(item_to_add):
    with open("iceland.csv","a", newline='',  encoding="utf-8") as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow([item_to_add['title'],item_to_add['price'],item_to_add['tags'],item_to_add['ingerdients'],item_to_add['image'],item_to_add['link']])
def get_Iceland_Items():
    urls=[["https://www.iceland.co.uk/fresh","fresh"],
    ["https://www.iceland.co.uk/bakery","bakery"],
    ["https://www.iceland.co.uk/frozen","frozen"],
    ["https://www.iceland.co.uk/drinks","drinks"]]
    # Also need to add chocolate sections and other stuff
    # cuz why not?
    create_file()
    for links in urls:
        url=links[0]
        while True:
            doc=scrape_page(url)
            results= doc.find_all(class_="name-link")
            for i in range(len(results)-1):
                item={}
                item['title']=simplify(results[i])
                item['link']=results[i]['href']
                
                time.sleep(20)
                item_doc=scrape_page(results[i]['href'])
                nutrition=item_doc.find(class_="product-right-col-inner")
                item_image=item_doc.find(class_="product-image main-image image-to-zoom")
                
                
                if item_image!=None:
                    opener = urllib.request.URLopener()
                    opener.addheader('User-Agent', 'whatever')
                    a=urlparse(item_image['href'])
                    item['image']=os.path.basename(a.path)
                    time.sleep(5)
                    opener.retrieve(item_image['href'],"Images/Iceland/"+item['image'])
                else:
                    item['image']=""
                price=item_doc.find(class_="product-sales-price").get_text().strip()
                item['price']=price[1:]
                
                try:
                    nutrition=nutrition.find(class_="mt-3")
                    ingredients=nutrition.get_text().strip()
                    item['ingerdients']=ingredients
                except:
                    item['ingerdients']=""
                item['tags']=links[1]
                write_line(item)
            next_page=doc.find(class_="page-link page-next")
            try:
                if next_page['href']!=None:
                    url=next_page['href']
            except:
                break
            time.sleep(20)
    print("Iceland Scraped!")

get_Iceland_Items()

    





