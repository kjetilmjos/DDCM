# -*- coding: utf-8 -*-

import pymongo
from datetime import datetime
from datetime import timedelta
import dateutil.parser
import json
import glob, os
import zipfile
from openpyxl import Workbook

#----Setting up openpyxl-----
wb = Workbook()
dest_filename = 'Query output.xlsx'
ws1 = wb.active
ws1.title = "Query output"
#----/Setting up openpyxl/-----

#----Setting up Database connection-----
mongodb_server_url = 'mongodb://166.166.0.133:27017'
try:
    conn=pymongo.MongoClient(mongodb_server_url)
    db = conn.condition
    database_name = db.PN1042 # change to correct PN number
    print ("Connected successfully to database")
except:
    print("Could not connect to DB")
#----/Setting up Database connection/-----

#----Initializing arrays-----
tags_array = []
query_dates_array = []
#----/Initializing arrays/-----

#----Reading configuration file-----
with open('CONFIG.json', 'r') as config_file:
    config_file = json.load(config_file)

for tags in config_file['tags']:
    tags_array.append(tags['tag'])

for dates in config_file['dates']:
    query_dates_array.append(dateutil.parser.parse(dates['date']))

MW_tag = config_file["MW_tag"]
MW_hysteres = config_file["MW_hysteres"]
#----/Reading configuration file/-----

def check_date(tag, date, MW_tag, MW_hysteres):
    # Find MW entry with date from list
    query_reference_MW = database_name.find({u'tag' : MW_tag, u'date' : date})

    if query_reference_MW.count() == 0:
        ws1['A1'] = date
        ws1['A2'] = "No valid MW entry found on this date"
    else:
        reference_MW = query_reference_MW[0][u'value']

        # Calculate timedeltas in weeks
        date_week = date - timedelta(weeks=1)
        #date_month = date_loop - timedelta(weeks=4)
        #date_six_months = date_loop - timedelta(weeks=24)
        #date_year = date_loop - timedelta(weeks=52)

        #--------------------------Last database entry query-------------------------------#
        query_reference_value = database_name.find({u'tag' : tag, u'date' : date})
        print (query_reference_value)
        reference_entry_value = query_reference_value[0][u'value']
        reference_entry_description = query_reference_value[0][u'description']
        reference_entry_unit = query_reference_value[0][u'unit']
        #--------------------------/Last database entry query-------------------------------#

        #--------------------------Week query-------------------------------#
        list_week = []
        relevant_dates_week = []
        week_average = 0
        week_value_dev = 0
        week_sample = 0

        query_dates_week = database_name.find({u'tag' : MW_tag, u'value' : {'$lt' : reference_MW + MW_hysteres , '$gt': reference_MW - MW_hysteres}, u'date' : {'$gte' : date_week, '$lt' : date}})
        for i in query_dates_week:
            relevant_dates_week.append(i[u'date'])

        query_last_week = database_name.find({u'tag' : tag, u'date' : { "$in" : relevant_dates_week}},{"_id": 0, u'value' : 1})

        if query_last_week.count() != 0:
            for k in query_last_week:
                list_week.append(k[u'value'])
                week_average = sum(list_week) / float(len(list_week))
                week_value_dev = reference_entry_value - week_average
                week_sample = len(list_week)
        else:
            week_average = 0
            week_value_dev = 0
            week_sample = 0


        #--------------------------/Week query-------------------------------#
        ws1['A5'] = "Reference sample"
        ws1['A6'] = "Tag: "+ tag
        ws1['A7'] = "Description: "+ reference_entry_description
        ws1['A8'] = "Unit: "+ reference_entry_unit
        ws1['A9'] = "Value: "+ str(reference_entry_value)[0:5]
        ws1['A10'] = "Timestamp: "+ str(date)[0:10]
        ws1['A11'] = "MW: "+ str(reference_MW) [0:5]

        ws1['A15'] = "Compared to last week average"
        ws1['A16'] = "Number of samples: "+ str(week_sample)
        ws1['A17'] = "Average: "+ str(week_average) [0:5]
        ws1['A18'] = "Value deviation: " + str(week_value_dev) [0:5]

# Running the check_date method for each tag each date
for dates in query_dates_array:
    for tags in tags_array:
        check_date(tags, dates, MW_tag, MW_hysteres)


wb.save(filename = dest_filename)
