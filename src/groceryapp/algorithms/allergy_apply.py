
import csv
import re


import nltk
import re

def create_file(filename):
    with open(filename,"w", newline='', encoding="utf-8") as csvfile:
        writer=csv.DictWriter(csvfile, fieldnames=["id",'name',"retailer","price","category","ingredients","image","link","similar","gluten",'lactose','nut'])
        writer.writeheader()
    return writer
  
def write_line(item_to_add, filename):
    with open(filename,"a", newline='',  encoding="utf-8") as csvfile:
        writer=csv.DictWriter(csvfile, ["id",'name',"retailer","price","category","ingredients","image","link","similar","gluten",'lactose','nut'])
        writer.writerow(
            item_to_add)


def extract_ingredients(text):
    # Remove unwanted parts of the string
    text = re.sub(r'ALLERGY ADVICE:.*$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'May contain:.*$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Does not contain:.*$', '', text, flags=re.IGNORECASE)

    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    # Remove non-alphabetic tokens and convert to lower case
    ingredients = [token.lower() for token in tokens if token.isalpha()]

    # Filter out common non-ingredient words (customize this list as needed)
    non_ingredients = ['with', 'and', 'in', 'for', 'the', 'of', 'a', 'an']
    ingredients = [ingredient for ingredient in ingredients if ingredient not in non_ingredients]

    return ingredients

def contains_ingredient(ingredient_string, trigger_keywords):
    if len(ingredient_string)<3:
        return None

    ingredient_string = ingredient_string.lower()

    # Extract ingredients
    ingredients = extract_ingredients(ingredient_string)

    # Check if any trigger keyword is present in the extracted ingredients
    contains = any(re.search(trigger_keywords, ingredient) for ingredient in ingredients)

    return not contains

def contains_gluten_ingredient(description):
    gluten_keywords = r'\b(?:wheat|barley|rye|triticale|malt|brewer.?s yeast|wheat starch|hydrolyzed wheat protein|wheat bran|wheat germ|durum|semolina|spelt|farro|einkorn|kamut|bulgur)\b'
    return contains_ingredient(description, gluten_keywords)

def contains_lactose_ingredient(description):
    lactose_keywords = r'\b(?:milk|lactose|whey|casein|curds|galactose|lactalbumin|lactoglobulin|lactoferrin|lactulose)\b'
    return contains_ingredient(description, lactose_keywords)

def contains_nut_ingredient(description):
    nut_keywords = r'\b(?:nut.?s|almond.?s|brazil nut.?s|cashew|chestnut.?s|filbert.?s|hazelnut.?s|macadamia.?s|pecan.?s|pine nut|pistachio|walnut.?s)\b'
    return contains_ingredient(description, nut_keywords)




def remove_bold_ch(letter):
  for i in range(len(letter)-1):
        if ord(letter[i])>=119808 and ord(letter[i])<=119833:
          ltr=ord(letter[i])%26
          ltr=ltr+97
          print(letter[i])
          letter[i]=chr(ltr)
        elif ord(letter[i])>=119834 and ord(letter[i])<=119859:
          ltr=ord(letter[i])%26
          ltr=ltr+97
          print(letter[i])
          letter[i]=chr(ltr)
  return letter




def collect_data():
    stores=["aldi_sim.csv","iceland_sim.csv"]
    store_name=['aldi','iceland']
    output="final_grocery.csv"
    functions=[contains_gluten_ingredient,contains_lactose_ingredient,contains_nut_ingredient]
    create_file(output)
    counter=0
    for i in range(len(stores)):
        with open(stores[i], 'r',encoding="utf-8") as file:
            storereader=csv.DictReader(file)
            for row in storereader:
                allergy=[]
                ingredients=row.get('ingredients')
                ingredients=remove_bold_ch(ingredients)
                for f in functions:
                    result=f(ingredients)
                    allergy.append(result)
                name=row.get('name')
                price=row.get('price')
                category=row.get('category')
                image=row.get('image')
                link=row.get('link')
                try:
                    similar=row.get("similar")
                except:
                    similar=None
                
                       
                item={"id":counter,'name':name,"retailer":store_name[i],"price":price,"category":category,"ingredients":ingredients,"image":image,"link":link,"similar":similar,"gluten":allergy[0],'lactose':allergy[1],'nut':allergy[2]}
                counter+=1
                write_line(item, output)

collect_data()

