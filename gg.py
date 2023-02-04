import csv

with open("./iceland.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    print(row)