from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
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


def create_file(filename):
    with open(filename,"w", newline='', encoding="utf-8") as csvfile:
        writer=csv.writer(csvfile)
    return writer


def get_product_selenium(url, driver):
    driver.get(url)
    time.sleep(5)   
    driver.refresh()
    time.sleep(20)
    page = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(''.join(page), 'html.parser') 
    return soup     


def write_line(item_to_add, filename):
    with open(filename,"a", newline='',  encoding="utf-8") as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow([
            item_to_add['title'],
            item_to_add['price'],item_to_add['tags'],
            item_to_add['ingerdients'],
            item_to_add['image'],item_to_add['link']])


def get_Aldi_Items():
    
    urls=[
    ["https://groceries.aldi.co.uk/en-GB/drinks?origin=dropdown&c1=groceries&c2=drinks&c3=shopall-drinks&clickedon=shopall-drinks","drinks"],
    ["https://groceries.aldi.co.uk/en-GB/fresh-food","fresh"],
    ["https://groceries.aldi.co.uk/en-GB/bakery?origin=dropdown&c1=groceries&c2=bakery&c3=shopall-bakery&clickedon=shopall-bakery","bakery"],
    ["https://groceries.aldi.co.uk/en-GB/frozen?origin=dropdown&c1=groceries&c2=frozen-food&c3=shopall-frozen-food&clickedon=shopall-frozen-food","frozen"]
    ]
    doc=get_product_selenium("https://groceries.aldi.co.uk/en-GB/fresh-food",webdriver.Chrome())
    #create_file("aldi.csv")
    counter=0
    driver= webdriver.Chrome()
    for links in urls:
        url=links[0]
        # if counter==0:
        #     url="https://groceries.aldi.co.uk/en-GB/drinks?sortDirection=asc&page=5"
        # counter=1
        while True:
            doc=get_product_selenium(url,driver)
            print(doc)
            results= doc.find_all(class_="product-tile-text text-center px-3 mb-3")
            
            for i in range(len(results)-1):
                item={}
                try:
                    item['title']=simplify(results[i])
                    item['link']="https://groceries.aldi.co.uk"+results[i].find('a')['href']
                except:
                    break
                print(item['link'])
                
                time.sleep(20)

                item_doc=get_product_selenium(item['link'],driver)
                item_image=item_doc.find(class_="product-main-img img-fluid")
                if item_image!=None:
                    opener = urllib.request.URLopener()
                    opener.addheader('User-Agent', 'whatever')
                    a=urlparse(item_image['src'])
                    item['image']=os.path.basename(a.path)
                    time.sleep(5)
                    opener.retrieve(item_image['src'],"../../media/images"+item['image'])
                else:
                    item['image']=""
                
                try:
                    price=simplify(item_doc.find(class_="product-price h4 m-0 font-weight-bold"))
                    print(price)
                    item['price']=price[1:]
                    item['tags']=links[1]
                    if price=="{{Product.ListPrice}}":
                        price=""
                except:
                    item['price']=""
                try:
                    items=item_doc.find_all("tr")
                    for i in items:
                        if "Ingredients" in i.find("th"):
                            nutrition=i
                    nutrition=nutrition.find("td")
                    ingredients=simplify(nutrition)
                    item['ingerdients']=ingredients                    
                except:
                    item['ingerdients']=""
                    
                if item['price']!="":
                    write_line(item,"aldi.csv")
            try:
                next_page=doc.find(class_="row filters-row d-block pt-2").find(class_="page-item next ml-2").find('a')
                if next_page['href']!=None:
                    url=links[0]+next_page['href']
            except:
                break
            time.sleep(20)
    print("ALDI Scraped!")


#get_Aldi_Items()

urls=[["https://groceries.aldi.co.uk/en-GB/p-williams-bros-brewing-co-fraoch-heather-ale-500ml/5022943903311","drinks"]
    ,["https://groceries.aldi.co.uk/en-GB/fresh-food","fresh"],
    ["https://groceries.aldi.co.uk/en-GB/bakery?origin=dropdown&c1=groceries&c2=bakery&c3=shopall-bakery&clickedon=shopall-bakery","bakery"],
    ["https://groceries.aldi.co.uk/en-GB/frozen?origin=dropdown&c1=groceries&c2=frozen-food&c3=shopall-frozen-food&clickedon=shopall-frozen-food","frozen"],
    ]
driver= webdriver.Chrome()   
item_doc=get_product_selenium("https://uk.indeed.com/viewjob?jk=8cb16bf412dbf747&tk=1gud1d1n5g80k801&from=hp&advn=4121280368461714&adid=410943331&ad=-6NYlbfkN0DLxniXb9xd09bch3T7EymxCrgj1jiT2kSu__xrmi42oKXtCF0Lmj9Q-wveQwgKXr0Tj0E9KR1ZxUjxkBODTX_7fM8M-X6dyPFrr5U3kJVP9SBw4nP9nrDDOsgMQF4SLknH5zaQMQ6cxdQ-KpwzRSPHame9N_zRnQNX2Cm25bW433-_M7d7Ft0RSkNtiMv9IheI5q0y3kuZB-k4I6oMV1HD00oyP9xomkVMs8oYU00TBlb8mOcOVss8VNsVGGV24-kPShHiM-AlTr9hIvC_cftF0TZHYW2IZlb9LKsOMnAcoYR3r_G72mRdTguaekfT4QRBDMdrfBX0Ws4WQjl2BlHTFLU7WSC2W9MeQB-oqYT666Mup4VdVdxcw6eAZjqDApDGdUbgrtbgTrFmaBp8pMEE760K98Z2049EAk3IjE2zrypKxkGIPKOaVzfAKRWrgiUGWjSsczs6LXhzxAkH3wTDT7njWY9V1bxMRf-BvDxeIA%3D%3D&pub=4a1b367933fd867b19b072952f68dceb&xkcb=SoD1-_M3QNK75iwsRp0JbzkdCdPP&vjs=3",driver)
# next_page=item_doc.find(class_="row filters-row d-block pt-2").find(class_="page-item next ml-2").find('a')
# if next_page['href']!=None:
#     url=urls[0][0]+next_page['href']
#     print(url)

descripption=simplify(item_doc.find(class_="jobsearch-jobDescriptionText jobsearch-JobComponent-description"))
print(descripption)
# items=item_doc.find_all("tr")
# for i in items:
#     if "Ingredients" in i.find("th"):
#         print(simplify(i.find("td")))
    



