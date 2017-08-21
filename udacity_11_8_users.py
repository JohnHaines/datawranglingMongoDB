# -*- coding: utf-8 -*-
"""
From Udacity: Data Wrangling With MongoDB

Find out how many unique users have contributed to the map
The function process_map returns a set of unique user IDs ("uid")

"""
import xml.etree.cElementTree as ET
import pprint
import re


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'uid' in element.attrib:               # element.attrib is a dictionary containing each attribute (as a key) and the attribute value
            users.add(element.attrib['uid'])      # use add to add a single item to a set 
    
    return users

def test():

    users = process_map('data\example.osm')
    pprint.pprint(users)
    assert len(users) == 6

if __name__ == "__main__":
    test()