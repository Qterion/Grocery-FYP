import spacy
import pandas as pd
from thefuzz import fuzz
import csv
import numpy as np
def text_similarity(text1, text2):
    nlp = spacy.load("en_core_web_lg")
    doc1=nlp(text1)
    print(doc1)
    doc2=nlp(text2)
    print(doc2)
    similarity=doc1.similarity(doc2)
    return similarity

def create_file(filename):
    with open(filename,"w", newline='', encoding="utf-8") as csvfile:
        writer=csv.writer(csvfile,delimiter="^")
    return writer
  
def write_line(item_to_add, filename):
    with open(filename,"a", newline='',  encoding="utf-8") as csvfile:
        writer=csv.writer(csvfile,delimiter="^")
        writer.writerow(
            item_to_add)

# with open("../aldi.csv", 'r',encoding="utf-8") as csfile:
#   print(1)
# create_file("cosine_similarity.csv")
# with open("../new_aldi.csv", 'r',encoding="utf-8") as file:
#   icelandreader = csv.reader(file)
#   for row in icelandreader:
#     tmp=row
#     valA=tmp[0]
#     highest_item=''
#     score=0
#     with open("../iceland.csv", 'r',encoding="utf-8") as csfile:
#       aldireader = csv.reader(csfile, delimiter=',')
#       for row in aldireader:
#         if row[2]==tmp[2]:
#           temp=text_similarity(valA,row[0])
#           if temp>score:
#             score=temp
#             highest_item=row[0]
#     if(score!=0):
#       write_line([valA,highest_item,score],"cosine_similarity.csv")

text1="Hello"
text2="Hi"

print(text_similarity(text1,text2))

# create_file("fixed_cosine_similarity.csv")
# with open("./similarity.csv", 'r',encoding="utf-8") as file:
#     similarity = csv.reader(file)
#     for row in similarity:
#         row[2]=int(float(row[2])*100)
#         if(row[2]>=80):
#             print(row[2])
#             write_line(row,'fixed_cosine_similarity.csv')
    