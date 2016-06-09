from openpyxl import load_workbook
from dateutil.parser import parse
import datetime

wb2 = load_workbook('../upload/excel_export.xlsx')
ws1 = wb2.active

allowed_columns = 36

errors = 0

if ws1.max_column > allowed_columns:
    errors = 1
    print("Too many columns in use, is this only one month?")

try_date = ws1['D2'].value

if isinstance(try_date,datetime.datetime) == False:
    errors = 1
    print("Date not valid")


if errors ==1:
    print("Input file not valid")
else:
    print("File OK")
