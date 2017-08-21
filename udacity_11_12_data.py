# -*- coding: utf-8 -*-
"""
From Udacity: Data Wrangling with MongoDB

Wrangle the data and transform its shape.  The output should be a list of dictionaries like this:
{
#"id": "2406124091",
#"type: "node", #
#"visible":"true",
#"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
#"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
#"amenity": "restaurant",
#"cuisine": "mexican",
#"name": "La Cabana De Don Luis",
#"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats and not strings. 
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:
{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
POSITION = ["lat", "lon"]

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

mapping = { "St": "Street", "St.": "Street", "Ave.": "Avenue", "Ave": "Avenue", "Rd.": "Road", "N." : "North"}



def shape_element(element):
    
    node = {}
    created = {}
    address = {}
    nd_refs = []
    pos =[0.0,0.0]
    
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        for name, value in element.attrib.items():
            if name in CREATED:
                
                created[name] = value
                node['created'] = created
                continue
            
            if name in POSITION:
                if name == "lat":
                    pos[0] = (float(value))
                else:
                    pos[1] = float(value)    
                node['pos'] = pos
                continue
               
            node[name] = value      
        
        for tag in element.iter("tag"):
            name = tag.attrib['k']
            value = tag.attrib['v']
                    
            if problemchars.search(name):      # ignore if problem
                continue
                
            if name.startswith('addr'):
                if name.count(':') == 1:  
                    front,label = name.split(":",2)
                    value = update_name(value, mapping)
                    address[label] = value
                    node['address'] = address
            else:
                name = name.replace(':', '_')  
                node[name] = value    
                            
                
        for tag in element.iter("nd"):    
            value = tag.attrib['ref']
            nd_refs.append(value)
            node["node_refs"] = nd_refs    
        
        return node
    else:
        return None
'''
def process_1(file_in, pretty=False):
    for event, element in ET.iterparse(file_in):
            el = shape_element(element)
            pprint.pprint(el)
'''    
    
    
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for event, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def update_name(name, mapping):
    #  split provided name into constituent parts. 
    #  Look for each in the mapping and replace it.
    #  Build up new name in list and then convert back to string
    new_name = []
    name_list = name.split(" ")
    for word in name_list:
        if word in mapping:
            word = word.replace(word, mapping[word])
        new_name.append(word)
    name = " ".join(new_name)
    return name

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('data\example.osm', True)
    pprint.pprint(data[-1])
    
    correct_first_elem = {
        "id": "261114295", 
        "visible": "true", 
        "type": "node", 
        "pos": [41.9730791, -87.6866303], 
        "created": {
            "changeset": "11129782", 
            "user": "bbmiller", 
            "version": "7", 
            "uid": "451048", 
            "timestamp": "2012-03-28T18:31:23Z"
        }
    }
    assert data[0] == correct_first_elem
    assert data[-1]["address"] == {
                                    "street": "West Lexington Street", 
                                    "housenumber": "1412"
                                      }
    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369", 
                                    "2199822370", "2199822284", "2199822281"]

if __name__ == "__main__":
    test()