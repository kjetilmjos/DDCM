import os

try:
    os.remove('./upload/CONFIG_query.json') # change to . when using node.js
except:
    next
try:
    os.remove('./upload/excel_export.xlsx') # change to . when using node.js
except:
    next
try:
    os.remove('./public/DDCM_output.zip') # change to . when using node.js
except:
    next
    try:
        os.remove('./Parser_output.csv') # change to . when using node.js
    except:
        next
try:
    os.remove('./upload/CONFIG_dates.json') # change to . when using node.js
except:
    next
try:
    os.remove('./upload/CONFIG_tags.json') # change to . when using node.js
except:
    next
try:
    os.remove('./upload/CONFIG_query.json') # change to . when using node.js
except:
    next
try:
    filelist = [ f for f in os.listdir("./") if f.endswith(".txt") ]
    for f in filelist:
        os.remove(f)
except:
    next

print("Files removed!")
