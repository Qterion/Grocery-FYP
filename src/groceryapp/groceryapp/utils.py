from faker import Faker
import random
import csv
from django.conf import settings
from pprint import pprint
from django.core.files import File
import os
from pathlib import Path
DATA_DIR = os.path.join(settings.BASE_DIR, "data")
GROCERIES_META_CSV=os.path.join(DATA_DIR,"grocery_data.csv")
UPLOAD_DIR=Path(settings.BASE_DIR/"media/images/")

def load_grocery_data(limit=10):
    with open(GROCERIES_META_CSV, newline='', encoding="utf-8") as csvfile:
        read=csv.DictReader(csvfile)
        grocery_data=[]
        counter=0
        for i, row in enumerate(read):
            # pprint(row)
            data={
                "id":int(row.get('id')),
                "title":row.get("name"),
                "price":float(row.get("price")),
                "ingredients":row.get("ingredients"),
                "category":row.get("category"),
                "picture_filename":row.get("image"),
                "link":row.get("link"),
                "retailer":row.get("retailer"),
                "gluten_free":row.get("gluten"),
                "lactose_free":row.get("lactose"),
                "nut_free":row.get("nut"),
                "similar":row.get("similar")
            }
            grocery_data.append(data)
            if i+1>limit:
                break
        return grocery_data
def get_fake_users(count=10):
    fake=Faker()
    user_data=[]
    for _ in range(count):
        profile=fake.profile()
        gluten=bool(random.getrandbits(1))
        lactose=bool(random.getrandbits(1))
        nut=bool(random.getrandbits(1))
        
        data={
            "username":profile.get('username'),
            "email":profile.get("mail"),
            "is_active":True,
            "gluten_trigger":gluten,
            "lactose_trigger":lactose,
            "nut_trigger":nut,

        }
        user_data.append(data)
    return user_data
        