# -*- coding: utf-8 -*-
# This script extracts all manuscripts containing Danish texts and places their contents in a CSV file
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

f = open("DanishContents.csv","w+")
f.write("Title,Class,Language,Shelfmark,Date1,Date2\n")

items = 0
for collection in collections:
    for filename in os.listdir(collection):
        tree = ET.parse(collection + '/' + filename)
        root = tree.getroot()
        shelfmark = root.find('.//{http://www.tei-c.org/ns/1.0}msIdentifier/{http://www.tei-c.org/ns/1.0}idno').text
        dating = root.find('.//{http://www.tei-c.org/ns/1.0}head/{http://www.tei-c.org/ns/1.0}origDate')
        try:
            if dating.get('when'):
                date1 = dating.get('when')
                date2 = date1
            elif dating.get('notBefore'):
                date1 = dating.get('notBefore')
                date2 = dating.get('notAfter')
            else:
                date1 = ''
                date2 = ''
        except:
            date1 = ''
            date2 = ''
        for item in root.findall('.//{http://www.tei-c.org/ns/1.0}textLang[@mainLang="da"]...'):
            try:
                title = item.find('./{http://www.tei-c.org/ns/1.0}title').text.replace(',', ' ').replace('\n', ' ').strip()
                title = re.sub(' +', ' ',title)
            except:
                title = ''
            item_class = item.get('class')
            if item_class == None:
                item_class = ''
            try:
                language = item.find('.{http://www.tei-c.org/ns/1.0}textLang').text.replace(',', ' ').replace('\n', ' ').strip()
                language = re.sub(' +', ' ', language)
            except:
                language = ''
            f.write(title + ',' + item_class + ',' + language + ',' + shelfmark + ',' + date1 + ',' + date2 + '\n')
            items += 1
print('Total: ', items)
            
