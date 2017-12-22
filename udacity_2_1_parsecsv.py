"""
From Udacity Data Wrangling With MongoDB

Processes a csv file
.
Each file contains information from one meteorological station about the amount of
solar and wind energy for each hour of day.

The first line of the datafile describes the data source. The name of the weather station is extracted from it.

Data is returned as a list of lists . 
Uses  "reader" method to get data .
next() method - to get the next line from the iterator.

"""
import csv
import os

DATADIR = "data"
DATAFILE = "745090.csv"


def parse_file(datafile):
    name = ""
    data = []
    with open(datafile,'r') as f:
        #csv.reader creates a list object 
        reader = csv.reader(f, delimiter=",")
        for i, row in enumerate(reader):
            #print ("i ", i,  "row ", row)
            if i== 0:     # pick up weather station name
                name = row[1]
            else: 
                if i == 1:
                    next
                else:
                    data.append(row)   
    
    return (name, data)


def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    name, data = parse_file(datafile)
    assert name == "MOUNTAIN VIEW MOFFETT FLD NAS"
    assert data[0][1] == "01:00"
    assert data[2][0] == "01/01/2005"
    assert data[2][5] == "2"
    

if __name__ == "__main__":
    test()


