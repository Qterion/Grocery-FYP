import csv

with open("./sainsburys.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    print(row[3])