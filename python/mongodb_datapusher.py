
# -*- coding: utf-8 -*-

# CSV heading: Timestamp, MW, tag, value

# 2 significant bits

import pymongo
import csv
import dateutil.parser

conn=pymongo.MongoClient()
db = conn.condition

list_tag = []
list_description = []
list_unit = []
list_date = []
list_value = []


with open('Parser_output.csv') as csvfile:
    linereader = csv.reader(csvfile, delimiter= ',')
    for row in linereader:
        list_tag.append(row[0])
        list_description.append(row[1])
        list_unit.append(row[2])
        list_date.append(row[3])
        list_value.append(row[4])

x = 0
while x < len(list_date):
    insert = db.test.insert_one(
    {
        "date": dateutil.parser.parse(list_date[x]),
        "description": list_description[x],
        "unit": list_unit[x],
        "tag": list_tag[x],
        "value": float(list_value[x]),
        })
    x += 1

print("Data storing complete!")
