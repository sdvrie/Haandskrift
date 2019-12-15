# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import re
import sys

# List of directories to be checked
AMS = os.path.abspath(sys.argv[1] + '/Manuscripts/Den Arnamagnæanske Samling/')
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

langs = [ ]
East = ['da', 'sv']
West = ['non', 'is', 'fo']
German = ['gml', 'nl', 'de']
Latin = ['la']
centuries = { }
centuriesEast = { }
centuriesWest = { }
centuriesGerman = { }
centuriesLatin = { }
listCent = [ ]
total = 0
for collection in collections:
    print(collection)
    for filename in os.listdir(collection):
        tree = ET.parse(collection + '/' + filename)
        root = tree.getroot()
        ns = {'TEI' : 'http://www.tei-c.org/ns/1.0'}
        for place in root.findall('{http://www.tei-c.org/ns/1.0}teiHeader//{http://www.tei-c.org/ns/1.0}fileDesc//{http://www.tei-c.org/ns/1.0}sourceDesc//{http://www.tei-c.org/ns/1.0}head//{http://www.tei-c.org/ns/1.0}origPlace'):
            print("Manuscripts: ", total, "           \r",)
            if (place.text != None and re.search("Danmark", place.text)) or place.get('key') == 'DK' or place.get('key') == '#DK':
                for date in root.findall('{http://www.tei-c.org/ns/1.0}teiHeader//{http://www.tei-c.org/ns/1.0}fileDesc//{http://www.tei-c.org/ns/1.0}sourceDesc//{http://www.tei-c.org/ns/1.0}head//{http://www.tei-c.org/ns/1.0}origDate'):
                     if date.get('when') is not None:
                        century = date.get('when')[:2]
                     if date.get('notBefore') is not None:
                        century = date.get('notBefore')[:2]
                     if century not in centuries.keys():
                        centuries[century] = 0
                        centuriesEast[century] = 0
                        centuriesWest[century] = 0
                        centuriesGerman[century] = 0
                        centuriesLatin[century] = 0
                        listCent.append(century)
                     centuries[century] += 1
                     for lang in root.iter('{http://www.tei-c.org/ns/1.0}textLang'):
                        if lang.get('mainLang') == 'da' or lang.get('mainLang') == 'sv':
                            East = True
                        if lang.get('mainLang') == 'is' or lang.get('mainLang') == 'non' or lang.get('mainLang') == 'fo':
                            West = True
                        if lang.get('mainLang') == 'gml' or lang.get('mainLang') == 'nl' or lang.get('mainLang') == 'de':
                            German = True
                        if lang.get('mainLang') == 'la':
                            Latin = True
                     if East == True:
                        centuriesEast[century] += 1
                        East = False
                     if West == True:
                        centuriesWest[century] += 1
                        West = False
                     if German == True:
                        centuriesGerman[century] += 1
                        German = False
                     if Latin == True:
                        centuriesLatin[century] += 1
                        Latin = False                      
                total += 1


listCent.sort()
centName = [ ]
listMSS = [ ]
listEast = [ ]
listWest = [ ]
listGerman = [ ]
listLatin = [ ]
for item in listCent:
    listMSS.append(centuries[item])
    listEast.append(centuriesEast[item])
    listWest.append(centuriesWest[item])
    listGerman.append(centuriesGerman[item])
    listLatin.append(centuriesLatin[item])
    centName.append(item + '00')

print(len(listMSS))
print(len(listEast))
print(len(listWest))
print(len(listGerman))
print(len(listLatin))

import numpy as np
import matplotlib.pyplot as plt

y_pos = np.arange(7)
width = 0.15

plt.bar(y_pos, listMSS, width, label="Total", color='0.75')
plt.bar(y_pos + width, listEast, width, label="East Norse", color='r')
plt.bar(y_pos + width + width, listWest, width, label="West Norse", color='c')
plt.bar(y_pos + width + width + width, listLatin, width, label="Latin", color='k')
plt.bar(y_pos + width + width + width + width, listGerman, width, label="German/Dutch", color='y')
plt.xticks(y_pos + 0.6 /2, centName)
plt.ylabel('Number of manuscripts')
plt.title('Manuscripts produced in Denmark by century')
plt.legend(loc='best')
    
plt.show()
