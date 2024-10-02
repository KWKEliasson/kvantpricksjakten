# Kvantpricksjakten
Data treatment for kvantpriksjakten (Forskarhjälpen 2024)

## QCD module
Reads sample data from 'RawData' directory containing files:
- CQD_measurements1.xls
- CQD_measurements2.xlsx
- Well plate map.xlsx
- Plate to Excel sheet.xlsx

Create structured and formated .xlsx files from data.
Uses openpyxl and xlrd libraries

## Todo
- Read additional sample meta data
- Implement peak fitting and background subtraction
- Refactor code to be more structured and readable
