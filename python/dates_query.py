import pymongo

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print ("Connected successfully to database!!!")
except:
    print("Could not connect to DB")

db = conn.condition
collection = db.values

unique_dates = []
query_unique_dates = collection.distinct("date")

for k in query_unique_dates:
    unique_dates.append(str(k))

tmp = ','.join(unique_dates)

print(tmp)
