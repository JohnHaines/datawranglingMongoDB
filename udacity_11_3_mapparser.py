
# -*- coding: utf-8 -*-
"""
From : Udacity Data Wrangling with MongoDB

Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many.
count_tags function should return a dictionary with the tag name as the key and number of times this tag can be encountered in 
the map as value.

"""
import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict

def count_tags(filename):
        #  Approach passing the whole file
        
        # Use defaultdict to providing a counting mechanism
        tags = defaultdict(int)
        
        tree = ET.parse(filename)
        for elem in tree.iter():
            tags[elem.tag] += 1
        return tags


def count_tags_2(filename):
        # Alternative approach using iterparse.  This returns Event and Element data.        
        tags = defaultdict(int)
        for event, element in ET.iterparse(filename):
            tags[element.tag] += 1
        return tags
    

def test():

    tags = count_tags_2('data\example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

    

if __name__ == "__main__":
    test()