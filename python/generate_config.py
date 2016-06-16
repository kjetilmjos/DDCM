import json

with open('./upload/CONFIG_dates.json') as f:
    dates = json.load(f)

with open('./upload/CONFIG_tags.json') as k:
    tags = json.load(k)

dates.update(tags)

with open('./upload/CONFIG_query.json', 'w') as f:
    json.dump(dates, f)


print("Config file generated")
