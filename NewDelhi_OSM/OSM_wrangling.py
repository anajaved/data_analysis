#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
import xml.etree.cElementTree as ET
import datetime

import sqlite3
conn = sqlite3.connect('new_delhi.db')


OSM_FILE = "delhi.osm" 
SAMPLE_FILE = "sample.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_TAGS_PATH = "ways_tags.csv"

#writing the sample file 
'''
k = 25 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag
    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')
'''

#to check which tag names were present & how many 
'''def tag_types(SAMPLE_FILE):
    type_dict={}
    for event, elem in ET.iterparse(SAMPLE_FILE):
        if elem.tag in type_dict.keys():
            type_dict[elem.tag] +=1
        else:
            type_dict[elem.tag]=1
            
    print type_dict'''

#function to find which areas to clean
'''
def what_datatype(SAMPLE_FILE):
    lower = re.compile(r'^([a-z]|_)*$')
    lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
    problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    
    _lower= set()
    _lower_colon= set()
    _other= set()
    _users=set()
    for event, elem in ET.iterparse(SAMPLE_FILE, events=('start',)):
        for each in elem.iter('node'):          
            for child in each.iter('tag'):
    
                info= child.attrib['k']
                v= child.attrib['v']
    
                if re.search(lower,info):
                    keys["lower"] +=1
                    _lower.add(info)
                    #if info == "S":
                        #print "lower_colon:", info, "v:", v
                
                elif re.search(problemchars,info):
                    keys["problemchars"] +=1
        
                elif re.search(lower_colon,info):
                    keys["lower_colon"] +=1
                    _lower_colon.add(info)
                

                else: 
                    keys["other"] +=1
                    _other.add(info)
                    #print "other:", info, v
                    #if info == "S":
                    #    print "lower_colon:", info, "v:", v
                    
            print _other, _lower, _lower_colon
 
'''

#adapting data to the schema for SQL database

node_fields= ['changeset', 'uid', 'timestamp', 'lon', 'version', 'user', 'lat', 'id']
node_tag_fields = ['id', 'key', 'value', 'type']
way_fields = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
way_tag_fields = ['id', 'key', 'value', 'type']
way_node_fields = ['id', 'node_id', 'position']

problem_chars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def wrangling_delhi(SAMPLE_FILE, node_fields, node_tag_fields, way_fields, way_tag_fields, way_node_fields, problem_chars):  
    node_attribs = []
    way_attribs = []
    node_tags = []
    way_tags = []
    temp_set=set()
    pos=0
    
    """
    Parameters
    ----------
    SAMPLE_FILE: shortened OSM file
    node_fields, node_tag_fields, way_fields, way_tag_fields:
        list of strings
    problem_chars: regex code to find problem characters

    Returns
    -------
    4 individual lists of dictionaries storing the data
    """

    for event, each_node in ET.iterparse(SAMPLE_FILE, events=('start',)):
            #for node elements
            if each_node.tag== "node":
                for individual in each_node.iter('node'):
                    d= {}
                    for each in individual.attrib.items():
                        if each[0] == 'id':
                            if each[1] in temp_set:
                                continue
                            else:
                                d[each[0]]=each[1].encode('utf-8')
                                temp_set.add(each[1])
                        else:
                            d[each[0]]=each[1].encode('utf-8')
    
                    node_attribs.append(d)
                
                    
                for child in each_node.iter('tag'):
                    uid= each_node.attrib['id'].encode('utf-8')
                    k=child.attrib['k'].encode('utf-8')
                    v=child.attrib['v'].encode('utf-8')
                    temp_dict={}
            
            
                    if "name:" in k:
                        if k != "name:en": continue
                        
                    elif problem_chars.match(k):
                        continue
                    
                    elif (k == 'image') or (k== 'website'):
                        continue
                
                    elif (v == "\u0e15\u0e49\u0e2d\u0e07\u0e44\u0e1b\u0e19\u0e2d\u0e19\u0e41\u0e16\u0e27\u0e19\u0e35\u0e49") or ("IndiaMART.com" in v):
                        continue
                    
                    else:
                        if ":" in k:
                            sep_k= k.split(":",1)
                            temp_dict['id']=uid
                            temp_dict['type']=sep_k[0]
                            temp_dict['key']=sep_k[1]
                            temp_dict['value']=v
                            node_tags.append(temp_dict)
                        

                        else:
                            temp_dict['id']=uid
                            temp_dict['type']='regular'
                            temp_dict['key']=k
                            temp_dict['value']=v
                            node_tags.append(temp_dict)
                    
              
            #for way elements
            elif each_node.tag== "way":
                for individual in each_node.iter('way'):
                    d= {}
                    for each in individual.attrib.items():
                        d[each[0]]=each[1].encode('utf-8')
     
                    way_attribs.append(d)
                    
      
                for child in each_node.iter('tag'):
                    if "k" in child.attrib:
                        uid= each_node.attrib['id'].encode('utf-8')
                        k= child.attrib['k'].encode('utf-8')
                        v=child.attrib['v'].encode('utf-8')
                    
                        temp_dict={}
                
                        if  problem_chars.match(k):
                            continue
                        elif "I'm not sure if this is part of Janpath Lane, or not." in v:
                            continue 
                        else:
                            if ":" in k:
                                sep_k= k.split(":",1)
                                temp_dict['id']=uid
                                temp_dict['type']=sep_k[0]
                                temp_dict['key']=sep_k[1]
                                temp_dict['value']=v
                                way_tags.append(temp_dict)
            
                            else:
                                temp_dict['id']=uid
                                temp_dict['type']='regular'
                                temp_dict['key']=k
                                temp_dict['value']=v
                                way_tags.append(temp_dict)
                                
    #auditing postcodes and possible dashes         
    '''
    for each_dict in node_tags:
        if each_dict['key'] == 'postcode':
            postcode= each_dict['value']
            clean_post=re.findall(r'^(\d{6})-\d{4}$', postcode)
            #print clean_post
            
            if re.match(r'^\d{6}$', postcode):
                print "MATCHED", postcode
            else:
                print "no", postcode
                
            
    for each_d in way_tags:
        if each_d['key'] == 'postcode':
            postcode= each_d['value']
            clean_post=re.findall(r'^(\d{6})-\d{4}$', postcode)
            #print clean_post
            
            if re.match(r'^\d{6}$', postcode):
                print "MATCHED", postcode
            else:
               print "no", postcode
        '''
                            
    #auditing & cleaning phone numbers:        

    for each_dict in node_tags:
        if each_dict['key'] == 'phone':
            phone_value= each_dict['value']
            if re.match(r'^\+([0-9]+\s)*', phone_value):
                if "-" in phone_value:
                    sep_dashes= phone_value.split("-")
                    newphone="".join(sep_dashes)
                    each_dict['value']=newphone
                elif " " in phone_value:
                    sep_spaces= phone_value.split(" ")
                    newphone="".join(sep_spaces)
                    each_dict['value']=newphone
            else:
                continue
                    
    for each_dict in way_tags:
        if each_dict['key'] == 'phone':
            phone_val= each_dict['value']
            if re.match(r'^\+([0-9]+\s)*', phone_val):
                sep= phone_val.split(" ")
                newphone="".join(sep)
                each_dict['value']=newphone

    
    return way_attribs, way_tags, node_attribs, node_tags
    

def change_date(input):
    
    """
    Parameters
    ----------
    input: string in year-month-day format

    Returns
    -------
    string of the year only
    """
    
    for each in input:
        date= each['timestamp']
        sep= date.split("-")
        year=sep[0]
        each['timestamp']=year 
    
    
#cleaning data
def clean_data (data):

    """
    Parameters
    ----------
    data: takes in a list of the 4 individual lists created above

    Returns
    -------
    audited/cleaned strings 
    """

    way=data[0]
    w_tags=data[1]
    node=data[2]
    n_tags=data[3]
    
    
    #standardizing names 
    for each in n_tags:
        lower = each['value'].lower()
        k_lower= each['key'].lower()
        
        if "bank" in lower or "Bank" in lower:
            each['value'] = "bank"

        if "pharmacy" in lower:
            each['value'] = 'pharmacy'
        
        if "hospital" in lower:
            each['value']='hospital'
            
        if 'school' in lower:
            each['value']='school'
        
        if ('fuel' in lower) or ('oil' in lower) or ('petrol' in lower):
            each['value']='fuel'
            
        if 'park' in lower:
            each['value']='park'
        
        if ('clinic' in lower) or ('dr' in lower) or ('doctor' in lower):
            each['value']= 'clinic'
        
        if 'hotel' in lower:
            each['value']='hotel'

        if ('fast_food' in lower) or ('pizza' in lower) or ('street_vendor' in lower) or ('restaurant' in lower):
            each['value']= 'food'
        
        if 'cinema' in lower:
            each['value']='cinema'
        
    #changing dates to year 
    change_date(way)  
    change_date(node) 
    
    for each in n_tags:
        if (each['key']== 'city') and ('delh' in each['value'].lower()):
            each['value'] = "New Delhi"
        
        if 'police' in each['value'].lower():
            each['value'] = 'police'
        
        if each['key']== 'state':
            each['value']='Delhi'

            
    return way, w_tags, node, n_tags


#writing .csv files 
def save_file (parsed, node_fields, node_tag_fields, way_fields, way_tag_fields):

    """
    Parameters
    ----------
    parsed: takes in a list of the 4 individual lists created above
    node_fields, node_tag_fields, way_fields, way_tag_fields:
        list of strings

    Returns
    -------
    creates 4 distinct .csv files 
    """
    
    way=parsed[0]
    w_tags=parsed[1]
    node=parsed[2]
    n_tags=parsed[3]
    
    
    with open("nodes.csv", 'w') as f:
        write = csv.DictWriter(f, fieldnames=node_fields)
        write.writeheader()
        for each in node:
            write.writerow(each)
            
    with open("nodes_tags.csv", 'w') as g:
        write = csv.DictWriter(g, fieldnames=node_tag_fields)
        write.writeheader()
        for each in n_tags:
            write.writerow(each)
            
    with open("ways.csv", 'w') as h:
        write = csv.DictWriter(h, fieldnames=way_fields)
        write.writeheader()
        for each in way:
            write.writerow(each)
            
    with open("ways_tags.csv", 'w') as i:
        write = csv.DictWriter(i, fieldnames=way_tag_fields)
        write.writeheader()
        for each in w_tags:
            write.writerow(each)
            
            
#'new_delhi.db' database tables        
def make_database(conn):
    cur = conn.cursor()
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS nodes (
        changeset INTEGER,
        uid INTEGER,
        timestamp TEXT,
        lon REAL,
        version INTEGER,
        user TEXT,
        lat REAL,
        id INTEGER PRIMARY KEY NOT NULL
    ); ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS nodes_tags (
        id INTEGER,
        key TEXT,
        value TEXT,
        type TEXT,
        FOREIGN KEY (id) REFERENCES nodes(id)
    ); ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ways (
        id INTEGER PRIMARY KEY NOT NULL,
        user TEXT,
        uid INTEGER,
        version TEXT,
        changeset INTEGER,
        timestamp TEXT
    ); ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ways_tags (
        id INTEGER NOT NULL,
        key TEXT NOT NULL,
        value TEXT NOT NULL,
        type TEXT,
        FOREIGN KEY (id) REFERENCES ways(id)
    ); ''')
    
    conn.commit()
    conn.close()
    
    

data= wrangling_delhi(SAMPLE_FILE, node_fields, node_tag_fields, way_fields, way_tag_fields, way_node_fields, problem_chars) 
parsed = clean_data (data)
save_file (parsed, node_fields, node_tag_fields, way_fields, way_tag_fields)
make_database(conn)
