"""
From Udacity Data Wrangling With MongoDB Lesson 2 Excercie 2

For a file of power station data finds the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.


"""

import xlrd
import os
import csv

DATAFILE = "2013_ERCOT_Hourly_Load_Data.xls"
DATADIR = "data"
outfile = "data/2013_Max_Loads.csv"

def parse_file_examples(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    data = [[sheet.cell_value(r, col) 
                for col in range(sheet.ncols)] 
                    for r in range(sheet.nrows)]

    print ("\nList Comprehension")
    print ("data[3][2]:",  data[3][2])

    print ("\nCells in a nested loop:")    
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            if row == 50:
                print (sheet.cell_value(row, col))


    ### other useful methods:
    print ("\nROWS, COLUMNS, and CELLS:")
    print ("Number of rows in the sheet:",  sheet.nrows)
    print ("Type of data in cell (row 3, col 2):",sheet.cell_type(3, 2))
    print ("Value in cell (row 3, col 2):",sheet.cell_value(3, 2))
    print ("Get a slice of values in column 3, from rows 1-3:", sheet.col_values(3, start_rowx=1, end_rowx=4))

    print ("\nDATES:")
    print ("Type of data in cell (row 1, col 0):",sheet.cell_type(1, 0))
    exceltime = sheet.cell_value(1, 0)
    print ("Time in Excel format:",exceltime)
    print ("Convert time to a Python datetime tuple, from the Excel float:", xlrd.xldate_as_tuple(exceltime, 0))
    
    return data

def parse_file_1(datafile):
    """   More examples this time picking up minimum and maximum values
    """
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    col = 1
    minValue = min(sheet.col_values(col, start_rowx=1, end_rowx=None))
    maxValue = max(sheet.col_values(col, start_rowx=1, end_rowx=None))
    sumValue = sum(sheet.col_values(col, start_rowx=1, end_rowx=None))
    #  knock one off for header
    avgValue = sumValue/(sheet.nrows - 1)
    
    for row in range(sheet.nrows):
        if sheet.cell_value(row,col)== minValue:
            minTime = sheet.cell_value(row,col-1)
            minTime = xlrd.xldate_as_tuple(minTime, 0)
            print (minTime)
        if sheet.cell_value(row,col)== maxValue:
            maxTime = sheet.cell_value(row,col-1)
            maxTime = xlrd.xldate_as_tuple(maxTime, 0)    

    #  alternative to looping through is to use the Index method
    #  maxpos = cv.index(maxValue) + 1

    data = {
                'maxtime':  maxTime,
                'maxvalue': maxValue,
                'mintime':  minTime,
                'minvalue': minValue,
                'avgcoast': avgValue
        }
    return data

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []
    # 
    data.append(["Station", "Year", "Month", "Day", "Hour", "Max Load"])
    for col in range(1, sheet.ncols - 1):
        # omits fist column
        colValues = sheet.col_values(col, start_rowx=1, end_rowx=None)
        station = sheet.cell_value(0,col)
        maxValue = max(colValues)
        maxpos =  colValues.index(maxValue) + 1
        maxTime = sheet.cell_value(maxpos,0)
        maxYear, maxMonth, maxDay, maxHour, maxMin, maxSec = xlrd.xldate_as_tuple(maxTime, 0)
        print("Station", station, "maxYear", maxYear, "maxValue", maxValue)
        data.append([station,maxYear,maxMonth, maxDay, maxHour,maxValue])
    return data

def save_file(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        row = csv.writer(csvfile, delimiter='|')
        for i in data:
            row.writerow(i)
    return
    
def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    test()
