import openpyxl
import pprint

wb = openpyxl.load_workbook("./xong xoa.xlsx")

sheet = wb['Sheet2']

cellA2 = sheet['H20']

print(cellA2.value)