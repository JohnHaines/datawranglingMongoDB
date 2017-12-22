"""
From Udacity:  Data Wrangling with MongoDB  Lesson 6 Problem Set 3

Function fix_area() receives a string as an input, and returns a float representing the value of the area or None.
"""
import codecs
import csv
import json
import pprint

CITIES = 'data/cities.csv'

def fix_area(area):     # area provided as a string
    #  empty string
    if area == ("NULL"):
        #print (area, "returning None" )
        return None
    
    #  float including integer
    try:
        area_as_float = float(area)
        #print (area, "returning ", area_as_float )
        return area_as_float
    except ValueError:
        pass

    # everything else
    try:
        if area[0] == "{":
            # code below based on having two values with a pipe character split
            pt1,pt2 = area.split("|", 2)
            pt1 = pt1[1:]
            pt2 = pt2[:len(pt2)-1]
            if len(pt1) > len(pt2):
                return float(pt1)
            else: 
                return float(pt2)           
            
    except ValueError:
        print (area, "value error returning None")
        return None
    



def process_file(filename):
    
    data = []

    with open(filename, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        #skipping the extra metadata
        for i in range(3):
            next(reader)

        # processing file
        
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    assert data[3]["areaLand"] == None        
    print(data[8]["areaLand"])
    assert data[8]["areaLand"] == 55166700.0
    print(data[20]["areaLand"])
    assert data[20]["areaLand"] == 14581600.0
    print(data[33]["areaLand"])
    assert data[33]["areaLand"] == 20564500.0    

if __name__ == "__main__":
    test()
