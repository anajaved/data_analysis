'''
Finding the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.
'''


import xlrd
import os
import csv


datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    
    data=[]
    for each in range(1,9):
        station = sheet.cell_value(0, each) 
        land_section = list([sheet.cell_value(row, each) for row in range(1, sheet.nrows)])
        
        maxvalue=max(land_section)
        maxpos=land_section.index(maxvalue)+1

        max_time_pos= sheet.cell_value(maxpos, 0)
        max_realtime= xlrd.xldate_as_tuple(max_time_pos, 0)
        data.append([station,max_realtime[0], max_realtime[1], max_realtime[2], max_realtime[3],  maxvalue])
    return data    

    
data= parse_file(datafile)

def save_file(data, filename):
    heading=['Station','Year','Month','Day','Hour','Max Load']
    with open(filename, "wb") as f:
        write = csv.writer(f, delimiter='|')
        write.writerow(heading)
        for each in data:
            write.writerow(each)
