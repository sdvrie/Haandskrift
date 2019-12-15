# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import re

# List of directories to be checked
AMS = os.path.abspath('/Users/Sean/handrit.is/Manuscripts/Den Arnamagnæanske Samling/')
AM02 = os.path.abspath(AMS + '/AM/AM02/da/')
AM04 = os.path.abspath(AMS + '/AM/AM04/da/')
AM08 = os.path.abspath(AMS + '/AM/AM08/da/')
AM12 = os.path.abspath(AMS + '/AM/AM12/da/')
ACC = os.path.abspath(AMS + '/Acc/da/')
KR = os.path.abspath(AMS + '/Kr/da/')
RASK = os.path.abspath(AMS + '/Rask/da/')
STEPH = os.path.abspath(AMS + '/Steph/da/')
KG = os.path.abspath(AMS + '/KG/da/')

collections = [AM02, AM04, AM08, AM12, ACC, KR, RASK, STEPH, KG]

f= open("origPlace.csv", "w+")
f.write("Shelfmark,origPlace,key\n")

for collection in collections:
    for filename in os.listdir(collection):
        tree = ET.parse(collection + '/' + filename)
        root = tree.getroot()
        ns = {'TEI' : 'http://www.tei-c.org/ns/1.0'}
        for shelfmark in root.findall('{http://www.tei-c.org/ns/1.0}teiHeader/{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}sourceDesc/{http://www.tei-c.org/ns/1.0}msDesc/{http://www.tei-c.org/ns/1.0}msIdentifier/{http://www.tei-c.org/ns/1.0}idno'):
            print(shelfmark.text)
            try:
                f.write(shelfmark.text.replace(',', ' ') + ',')
            except:
                f.write(filename + ',')
        placement = False
        for place in root.findall('{http://www.tei-c.org/ns/1.0}teiHeader/{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}sourceDesc/{http://www.tei-c.org/ns/1.0}msDesc/{http://www.tei-c.org/ns/1.0}head/{http://www.tei-c.org/ns/1.0}origPlace'):
            placement = True
            try:
                re.sub('\s+', ' ', place.text).strip()
                f.write(place.text.replace(',', ' ').replace(';',' ').replace('\n','') + ',' + place.key + '\n')
            except:
                try:
                    re.sub('\s+', ' ', place.text).strip()
                    f.write(place.text.replace(',', ' ').replace(';',' ').replace('\n','') + ',NONE\n')
                except:
                    f.write("NONE,NONE\n")
        if placement == False:
            f.write("NONE,NONE\n")
