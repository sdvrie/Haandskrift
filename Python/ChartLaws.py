# -*- coding: utf-8 -*-
# This code takes the information from laws.csv and visualizes on a timeline
import csv

with open('laws.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        date = row['date1'] + row['date2'] / 2
        
                
