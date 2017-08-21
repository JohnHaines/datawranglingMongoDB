# -*- coding: utf-8 -*-
"""
From Udacity: Data Wrangling With MongoDB

Check the "k" value for each "<tag>" and see if there are any potential problems.
We have provided you with 3 regular expressions to check for certain patterns
in the tags. 
The function 'key_type', is to provide a count of each of
four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
"""

import xml.etree.cElementTree as ET
import pprint
import re


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        if lower_colon.search(element.attrib['k']):        # element.attrib['k'] gives the value of the tag
            keys['lower_colon'] += 1
        else:
            if problemchars.search(element.attrib['k']):
                keys['problemchars'] += 1
            else:
                if lower.search(element.attrib['k']):
                    keys['lower'] += 1
                else:
                    keys['other'] += 1
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for event, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    keys = process_map('data\example.osm')
    pprint.pprint(keys)
    


if __name__ == "__main__":
    test()