# -*- coding: utf-8 -*-
# This file reads the data in DanishContents.csv in search of texts titles 'law'

import csv
f = open("laws.csv", "w+")
f.write('Title,Shelfmark,Date1,Date2\n')
with open('DanishContents.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    titles = [ ]
    for row in reader:
        if 'lov' in row['Title'] or 'Lov' in row['Title']:
            f.write(row['Title'] + ',' + row['Shelfmark'] + ',' + row['Date1'] + ',' + row['Date2'] + '\n')
            title = row['Title']
            if title not in titles:
                titles.append(title)
    titles.sort()
    for item in titles:
        print(item)

