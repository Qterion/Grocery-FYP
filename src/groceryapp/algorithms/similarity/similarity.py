import csv
import os
from pathlib import Path
def create_file(filename):
    with open(filename,"w", newline='', encoding="utf-8") as csvfile:
        writer=csv.DictWriter(csvfile, fieldnames=['name',"price","category","ingredients","image","link",'similar'])
        writer.writeheader()
    return writer
  
def write_line(item_to_add, filename):
    with open(filename,"a", newline='',  encoding="utf-8") as csvfile:
        writer=csv.DictWriter(csvfile, ['name',"price","category","ingredients","image","link",'similar'])
        writer.writerow(
            item_to_add)

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


def  pre_process(item):
  item=item.lower()
  items=["'",":","pack",'cans']
  for i in items:
    item=item.replace(i,"")
  item=item.replace(" x ","x")
  item=item.replace("-"," ")
  item=item.replace("&"," ")
  item=item.replace(';'," ")
  item=item.replace('/',' ')
  item=item.replace(' litre',"l")
  # we split the string into array
  item=item.split()
  item=set(item)

  return item

def jaccard_similarity(value1, value2):
    value1_processed = pre_process(value1)
    value2_processed = pre_process(value2)
    common_words = value1_processed.intersection(value2_processed)
    main_string=max(len(value1_processed), len(value2_processed))

    sim_score = int((len(common_words) /main_string)*100)

    return sim_score

# string1 = "Lemsip 500ml"
# string2 = "Pepsi 500ml"
# print(jaccard_similarity(string1,string2))
def get_image_filename(image):
  img=image[:len(image)-4]
  path=Path(__file__).resolve().parent.parent.parent
  path=Path(path/"media/images/")
  if img=="image_not_found":
      image=None
  else:
      for fn in path.glob(f'{img}.*'):
        image=os.path.basename(fn)
  return image

def find_similarity(file_to_create, file1,file2):
  create_file(file_to_create)
  with open(file1, 'r',encoding="utf-8") as file:
    aldireader = csv.reader(file)
    for row1 in aldireader:
      tmp=row1
      valA=tmp[0]
      highest_link=''
      score=0
      with open(file2, 'r',encoding="utf-8") as csfile:
        icelandreader = csv.reader(csfile, delimiter=',')
        for row2 in icelandreader:
          if row2[2]==tmp[2]:
            tmp2=row2[0]
            temp=jaccard_similarity(valA,tmp2)
            if temp>score:
              score=temp
              highest_link=row2[5]
      if(score>=98):
        image=tmp[4]
        image=get_image_filename(image)
        item={'name':tmp[0],"price":tmp[1],"category":tmp[2],"ingredients":tmp[3],"image":tmp[4],"link":tmp[5],"similar":highest_link}
      else:
        item={'name':tmp[0],"price":tmp[1],"category":tmp[2],"ingredients":tmp[3],"image":tmp[4],"link":tmp[5],"similar":None}
      write_line(item,file_to_create)


def find_similarity_aldi():
  file1="../new_aldi.csv"
  file2="../iceland.csv"
  file_to_create="../aldi_sim.csv"
  find_similarity(file_to_create, file1,file2)


def find_similarity_iceland():
  file1="../iceland.csv"
  file2="../new_aldi.csv"
  file_to_create="../iceland_sim.csv"
  find_similarity(file_to_create, file1,file2)



find_similarity_aldi()
find_similarity_iceland()


