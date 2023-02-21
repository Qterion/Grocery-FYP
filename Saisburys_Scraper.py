from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import requests
import csv
import os
import urllib.request
from urllib.parse import urlparse


def simplify(item):
    if item!=None:
        return item.get_text().strip()
    return None

def scrape_page(url):
    result=requests.get(url)
    doc=BeautifulSoup(result.content,"html.parser")
    return doc

def create_file():
    with open("sainsburys.csv","w", newline='') as csvfile:
        writer=csv.writer(csvfile)
    return writer
        
def write_line(item_to_add):
    try:
        with open("sainsburys.csv","a", newline='') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow([item_to_add['title'],item_to_add['price'],item_to_add['tags'],item_to_add['ingerdients'],item_to_add['image'],item_to_add['link']])
    except:
        print(Exception)
def get_product_selenium(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(15)
    page = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(''.join(page), 'html.parser') 
    return soup
def get_Sainsburys_Items():
    urls=[["https://www.sainsburys.co.uk/shop/gb/groceries/bakery/seeall?","bakery"],["https://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/seeall","fresh"],
    ["https://www.sainsburys.co.uk/shop/gb/groceries/frozen-/seeall","frozen"]]
    create_file()
    for links in urls:
        url=links[0]
        while True:
            doc=scrape_page(url)
            results= doc.find_all(class_="productInfo")
            for i in range(len(results)-1):
                item={}
                temp=results[i].find("a")
                item['title']=simplify(temp)
                print(item['title'])
                item['link']=temp['href']
                time.sleep(5)
                item_doc=get_product_selenium(temp['href'])
                item_image=item_doc.find(class_="pd__image pd__image__nocursor")
                opener = urllib.request.URLopener()
                opener.addheader('User-Agent', 'whatever')
                price=item_doc.find(class_="pd__cost__retail-price")
                try:
                    nutrition=item_doc.find(class_="productIngredients")
                    ingredients=nutrition.get_text().strip()
                    item['ingerdients']=ingredients
                    price=simplify(price)
                    item['price']=price[1:]
                    a=urlparse(item_image['src'])
                    item_code=item_doc.find(id="productSKU").get_text().strip()
                    item['image']=item_code+os.path.splitext(os.path.basename(a.path))[1]
                    opener.retrieve(item_image['src'],"Images/Sainsburys/"+item['image'])
                    
                except:
                    item['ingerdients']=""
                    item['image']=""
                item['tags']=links[1]
                if price!=None:
                    write_line(item)
            next_page=doc.find(class_="next").find('a')
            try:
                if next_page['href']!=None:
                    url=next_page['href']
            except:
                break
            time.sleep(10)
    print("Sainsbury's Scraped!")

get_Sainsburys_Items()

# driver = webdriver.Chrome()

# driver.get("https://www.tesco.com/groceries/en-GB/products/274811214")
# time.sleep(4)
# page = driver.execute_script('return document.body.innerHTML')

# soup = BeautifulSoup(''.join(page), 'html.parser')
# link=soup.find(class_=("product-image"))['src']
# price=soup.find(class_="value").get_text().strip()
# print(link)
# print(price)
# dvls=soup.find('div',class_="product-info-block product-info-block--ingredients")
# print(dvls.get_text().strip())


# print(59123462363246324643263246342624)

# try:
#     next_page=soup.find(class_="next").find('a')
#     print(next_page.find('a'))
#     if next_page['href']!=None:
#         url=next_page['href']
#         print(url)
#         print(4421421)
# except:
#     print("lox")    
# print(100)
# print(link)
# print(100)
