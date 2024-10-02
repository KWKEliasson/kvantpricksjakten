# Kvantpricksjakten
Data treatment for kvantpriksjakten (Forskarhjälpen 2024)

## QCD module
Reads sample data from 'RawData' directory containing files:
- CQD_measurements1.xls
- CQD_measurements2.xlsx
- Well plate map.xlsx
- Plate to Excel sheet.xlsx

Create structured and formated .xlsx files from data.

Uses [openpyxl](https://openpyxl.readthedocs.io) and [xlrd](https://xlrd.readthedocs.io) libraries

## Todo
- Read additional sample meta data
- Implement spectrum analysis features:
  - Plotting 
  - Peak fitting
  - Background subtraction
