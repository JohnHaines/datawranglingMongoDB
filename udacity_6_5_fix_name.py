"""
From Udacity: Data Wrangling With MongoDB  

Function fix_name() will recieve a string as an input, and returns a list of all the names. If there is only one name, the list will
have only one item in it; if the name is "NULL", the list should be empty.
"""
import codecs
import csv
import pprint

CITIES = 'data/cities.csv'


def fix_name(name):
    return_name = []

    # Value is null
    if name != ("NULL"):
        
        # take out characters we don't like at the start of the string 
        if name[0] == "{":
            name = name.replace("{","")
            name = name.replace("}", "")
        if name[0] == "(":
            name = name.replace("(","")
            name = name.replace(")","")
           
        entries = name.count("|")
        if entries > 0:
            return_name = name.split("|", entries+1)
        else:
            return_name.append(name)    
    
    return return_name

def process_file(filename):
    data = []
    # note this might give encoding issues depending on the data set used.
    with open(filename, "r"  ) as f:
        reader = csv.DictReader(f)
        #skipping the extra metadata
        for i in range(3):
            next(reader)
        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "name" in line:
                line["name"] = fix_name(line["name"])
            data.append(line)
    return data


def test():
    data = process_file(CITIES)

    print ("Printing 20 results:")
    for n in range(20):
        pprint.pprint(data[n]["name"])

    assert data[14]["name"] == ['Negtemiut', 'Nightmute']
    assert data[9]["name"] == ['Pell City Alabama']
    assert data[3]["name"] == ['Kumhari']

if __name__ == "__main__":
    test()