import glob, os
import zipfile
files = []

os.chdir("./")
for file in glob.glob("*.txt"):
    files.append(file)

with zipfile.ZipFile('DDCM_output.zip', 'w') as myzip:
    for filer in files:
        myzip.write(filer)
