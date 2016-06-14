
# -*- coding: utf-8 -*-
import pymongo
from datetime import datetime
from datetime import timedelta
import dateutil.parser
import json
import glob, os
import zipfile

TAG = []
reference_date = []
Date_for_file = []
files = []

with open('./upload/CONFIG_query.json', 'r') as f: # change config path if running locally
    config = json.load(f)

for taggiser in config['tags']:
    TAG.append(taggiser['tag'])

for dattiser in config['dates']:
    reference_date.append(dateutil.parser.parse(dattiser['date']))
    Date_for_file.append(dattiser['date'][0:10]) # Only import date not time

MW_tag = config["MW_tag"]
MW_hysteres = config["MW_hysteres"]
noprint_limit = config["noprint_limit"]
# Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print ("Connected successfully to database!!!")
except:
    print("Could not connect to DB")

db = conn.condition
collection_values = db.values
date_file_loope= 0

for date_loop in reference_date:
    for tag_loop in TAG:
        no_print = 0
        query_reference_MW = collection_values.find({u'tag' : MW_tag, u'date' : date_loop})
        reference_MW = query_reference_MW[0][u'value']

        # Note all timedelta in weeks
        date_week = date_loop - timedelta(weeks=1)
        date_month = date_loop - timedelta(weeks=4)
        date_six_months = date_loop - timedelta(weeks=24)
        date_year = date_loop - timedelta(weeks=52)

        #--------------------------Last database entry query-------------------------------#
        reference_entry_tag = tag_loop
        reference_entry_MW = reference_MW
        reference_entry_timestamp = date_loop
        query_reference_value = collection_values.find({u'tag' : tag_loop, u'date' : date_loop})
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

        query_dates_week = collection_values.find({u'tag' : MW_tag, u'value' : {'$lt' : reference_entry_MW + MW_hysteres , '$gt': reference_entry_MW - MW_hysteres}, u'date' : {'$gte' : date_week, '$lt' : date_loop}})
        for i in query_dates_week:
            relevant_dates_week.append(i[u'date'])

        query_last_week = collection_values.find({u'tag' : tag_loop, u'date' : { "$in" : relevant_dates_week}})

        for k in query_last_week:
            list_week.append(k[u'value'])

        try:
            week_average = sum(list_week) / float(len(list_week))
        except:
            week_average = 0
        if week_average != 0:
            week_value_dev = reference_entry_value - week_average
            if abs(week_value_dev) < noprint_limit:
                no_print = 1
        else:
            week_value_dev = 0
        week_sample = len(list_week)

        #--------------------------/Week query-------------------------------#

        #--------------------------Month query-------------------------------#
        list_month = []
        relevant_dates_month = []
        month_average = 0
        month_value_dev = 0
        month_sample = 0

        query_dates_month = collection_values.find({u'tag' : MW_tag, u'value' : {'$lt' : reference_entry_MW + MW_hysteres , '$gt': reference_entry_MW - MW_hysteres}, u'date' : {'$gte' : date_month, '$lt' : date_loop}})
        for i in query_dates_month:
            relevant_dates_month.append(i[u'date'])

        query_last_month = collection_values.find({u'tag' : tag_loop, u'date' : { "$in" : relevant_dates_month}})

        for k in query_last_month:
            list_month.append(k[u'value'])
        try:
            month_average = sum(list_month) / float(len(list_month))
        except:
            month_average = 0
        if month_average != 0:
            month_value_dev = reference_entry_value - month_average
            if abs(month_value_dev) < noprint_limit:
                no_print = 1
        else:
            month_value_dev = 0
        month_sample = len(list_month)
        #--------------------------/Month query-------------------------------#

        #--------------------------Six month query-------------------------------#
        list_six_months = []
        relevant_dates_six_month = []
        six_months_average = 0
        six_months_value_dev = 0
        six_months_sample = 0

        query_dates_six_months = collection_values.find({u'tag' : MW_tag, u'value' : {'$lt' : reference_entry_MW + MW_hysteres , '$gt': reference_entry_MW - MW_hysteres}, u'date' : {'$gte' : date_six_months, '$lt' : date_loop}})
        for i in query_dates_six_months:
            relevant_dates_six_month.append(i[u'date'])

        query_last_six_months = collection_values.find({u'tag' : tag_loop, u'date' : { "$in" : relevant_dates_six_month}})

        for k in query_last_six_months:
            list_six_months.append(k[u'value'])

        try:
            six_months_average = sum(list_six_months) / float(len(list_six_months))
        except:
            six_months_average = 0
        if six_months_average != 0:
            six_months_value_dev = reference_entry_value - six_months_average
            if abs(six_months_value_dev) < noprint_limit:
                no_print = 1
        else:
            six_months_value_dev = 0
        six_months_sample = len(list_six_months)
        #--------------------------/Six month query-------------------------------#

        #--------------------------Year query-------------------------------#
        list_year = []
        relevant_dates_year = []
        year_average = 0
        year_value_dev = 0
        year_sample = 0

        query_dates_year = collection_values.find({u'tag' : MW_tag, u'value' : {'$lt' : reference_entry_MW + MW_hysteres , '$gt': reference_entry_MW - MW_hysteres}, u'date' : {'$gte' : date_year, '$lt' : date_loop}})
        for i in query_dates_year:
            relevant_dates_year.append(i[u'date'])

        query_last_year = collection_values.find({u'tag' : tag_loop, u'date' : { "$in" : relevant_dates_year}})

        for k in query_last_year:
            list_year.append(k[u'value'])

        try:
            year_average = sum(list_year) / float(len(list_year))
        except:
            year_average = 0
        if year_average != 0:
            year_value_dev = reference_entry_value - year_average
            if abs(year_value_dev) < noprint_limit:
                no_print = 1
        else:
            year_value_dev = 0
        year_sample = len(list_year)
        #--------------------------/Year query-------------------------------#

        #--------------------------Lifespan query-------------------------------#
        list_lifespan = []
        relevant_dates_lifespan = []
        life_average = 0
        life_value_dev = 0
        life_sample = 0

        query_dates_lifespan = collection_values.find({u'tag' : MW_tag, u'value' : {'$lt' : reference_entry_MW + MW_hysteres , '$gt': reference_entry_MW - MW_hysteres}, u'date' : {'$lt' : date_loop}})
        for i in query_dates_lifespan:
            relevant_dates_lifespan.append(i[u'date'])

        query_lifespan = collection_values.find({u'tag' : tag_loop, u'date' : { "$in" : relevant_dates_lifespan}})

        for k in query_lifespan:
            list_lifespan.append(k[u'value'])

        try:
            life_average = sum(list_lifespan) / float(len(list_lifespan))
        except:
            life_average = 0
        if life_average != 0:
            life_value_dev = reference_entry_value - life_average
            if abs(life_value_dev) < noprint_limit:
                no_print = 1
        else:
            life_value_dev = 0
        life_sample = len(list_lifespan)
        #--------------------------/Lifespan query-------------------------------#
        if no_print == 0:

            with open("DDCM -" + tag_loop + "-[" + Date_for_file[date_file_loope] + "].txt", "w") as text_file:
                text_file.write("----------------------------Data Driven Condition Monitoring [DDCM]----------------------------\n")
                text_file.write("\n")

                text_file.write("-------------------------------------\n")
                text_file.write("Reference sample\n")
                text_file.write("Tag: %s\n" % reference_entry_tag)
                text_file.write("Description: %s\n" % reference_entry_description)
                text_file.write("Unit: %s\n" % reference_entry_unit)
                text_file.write("Timestamp: %s\n" % reference_entry_timestamp)
                text_file.write("Value: %g\n" % reference_entry_value)
                text_file.write("MW: %g\n" % reference_entry_MW)
                text_file.write("MW Threshold +/-: %g\n" % MW_hysteres)
                text_file.write("-------------------------------------\n")
                text_file.write("\n\n")

                text_file.write("-------------------------------------\n")
                text_file.write("Compared to last week average\n")
                text_file.write("Number of samples: %d\n" % week_sample)
                text_file.write("Average: %g\n" % week_average)
                text_file.write("Value deviation: %g\n" % week_value_dev)
                text_file.write("-------------------------------------\n")
                text_file.write("\n\n")

                text_file.write("-------------------------------------\n")
                text_file.write("Compared to last month average\n")
                text_file.write("Number of samples: %d\n" % month_sample)
                text_file.write("Average: %g\n" % month_average)
                text_file.write("Value deviation: %g\n" % month_value_dev)
                text_file.write("-------------------------------------\n")
                text_file.write("\n\n")

                text_file.write("-------------------------------------\n")
                text_file.write("Compared to last six months average\n")
                text_file.write("Number of samples: %d\n" % six_months_sample)
                text_file.write("Average: %g\n" % six_months_average)
                text_file.write("Value deviation: %g\n" % six_months_value_dev)
                text_file.write("-------------------------------------\n")
                text_file.write("\n\n")

                text_file.write("-------------------------------------\n")
                text_file.write("Compared to year average\n")
                text_file.write("Number of samples: %d\n" % year_sample)
                text_file.write("Average: %g\n" % year_average)
                text_file.write("Value deviation: %g\n" % year_value_dev)
                text_file.write("-------------------------------------\n")
                text_file.write("\n\n")

                text_file.write("-------------------------------------\n")
                text_file.write("Compared to lifespan average\n")
                text_file.write("Number of samples: %d\n" % life_sample)
                text_file.write("Average: %g\n" % life_average)
                text_file.write("Value deviation: %g\n" % life_value_dev)
                text_file.write("-------------------------------------\n")
                text_file.write("\n\n")

                text_file.write("----------------------------/Data Driven Condition Monitoring [DDCM]----------------------------\n")

    date_file_loope += 1

with open("Query complete.txt", "w") as text_file:
    text_file.write("Finished searching through database...\n")
os.chdir("./")
for file in glob.glob("*.txt"):
    files.append(file)

with zipfile.ZipFile('./public/DDCM_output.zip', 'w') as myzip:
    for filer in files:
        myzip.write(filer)
print("Query complete!")
