
"""
From Udacity: Data Mangling with MongoDB  Lesson 8 Exercise 1

Parse the file, process only the fields that are listed in the FIELDS dictionary as keys, and return a list of dictionaries
of cleaned values. The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the  same value as 'label'.
- if a value of a field is "NULL", convert it to None
- strip leading and ending whitespace from all fields, if there is any
- if there is a value in 'synonym', it should be converted to an array (list) by stripping the "{}" characters and splitting the string on "|". Rest of the
  cleanup is up to you, e.g. removing "*" prefixes etc. If there is a singular  synonym, the value should still be formatted in a list.
- the output structure should be as follows:
[ { 'label': 'Argiope',
    'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
    'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
    'name': 'Argiope',
    'synonym': ["One", "Two"],
    'classification': {
                      'family': 'Orb-weaver spider',
                      'class': 'Arachnid',
                      'phylum': 'Arthropod',
                      'order': 'Spider',
                      'kingdom': 'Animal',
                      'genus': None
                      }
  },
  { 'label': ... , }, ...
]
"""
import csv
import pprint
import re

DATAFILE = 'data/arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}


def process_file(filename, fields):

    process_fields = fields.keys()
    data = []
    
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            next(reader)

        for line in reader:
            label_value = fix_label(line['rdf-schema#label'])
            output_line =  { 'label': label_value ,
                             'uri': fix_common(line['URI']),
                             'description': fix_common(line['rdf-schema#comment']),
                             'name': fix_name(line['name'], label_value),    # need label to substitute in if name is blank
                             'synonym': fix_synonym(line["synonym"]),
                             'classification':  {
                                    'family':  fix_common(line["family_label"]),
                                    'class':   fix_common(line['class_label']),
                                    'phylum':  fix_common(line['phylum_label']),
                                    'order':   fix_common(line['order_label']),
                                    'kingdom': fix_common(line['kingdom_label']),
                                    'genus':   fix_common(line['genus_label']),
                                                }
                           } 
            data.append(output_line)
    return data

def fix_label(v):
    v = fix_common(v)
    # take out data in parenthesis
    v =  re.sub('\([^)]*\)', "", v)
    v = v.strip()
    return v

def fix_name(v,l):
    if v == "NULL"  or  v.isalpha() == False:
        v = l
    return v

def fix_synonym(v):
    if v == "NULL":
        return None
    v_array = []
    if len(v) > 2  and v[0] == "{" and v[-1] == "}":
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
    else:
        v_array.append(v)
    return v_array

def fix_common(v):
    #  Null test
    if v == "NULL":
        return None
    else:
        if type(v) == "str":
        # Strip whitespace
            v =  v.strip()
    return v


def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]


def test():
    data = process_file(DATAFILE, FIELDS)
    print ("Your first entry:")
    pprint.pprint(data[0])
    first_entry = {
        "synonym": None, 
        "name": "Argiope", 
        "classification": {
            "kingdom": "Animal", 
            "family": "Orb-weaver spider", 
            "order": "Spider", 
            "phylum": "Arthropod", 
            "genus": None, 
            "class": "Arachnid"
        }, 
        "uri": "http://dbpedia.org/resource/Argiope_(spider)", 
        "label": "Argiope", 
        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
    }

    assert len(data) == 76
    
    assert data[17]["name"] == "Ogdenia"
    assert data[48]["label"] == "Hydrachnidiae"
    assert data[14]["synonym"] == ["Cyrene Peckham & Peckham"]
    assert data[0] == first_entry
if __name__ == "__main__":
    test()