# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 10:44:00 2018

@author: lukep
"""
import csv


rowForPhages = []

phageToDataRows = {}


    
for i in range(1, 11):
    with open(("W:/archive/all" + str(i) + ".csv"), "r") as weatherCSV:
        rowreader = csv.reader(weatherCSV, delimiter=',', quotechar='|')
        # ROW INDICES:
        #0 - NAME
        #4 - TEMP
        #5 - LO
        #6 - HI
        #16 - SKY CON
        for row in rowreader:
            if (row[0] != "NAME"):
                #if name already exists in phageToDataRows, add it to that phages array of rows
                if row[0] in phageToDataRows.keys():
                    phageToDataRows[row[0]].append(row)
                #otherwise, make a new entry with the phage's name
                else:
                    phageToDataRows[row[0]] = [row]




with open("W:/TheGoodStuff.csv", "r") as csvreader:
    rowreader = csv.reader(csvreader, delimiter=',', quotechar='|')
    for row in rowreader:
        rowForPhages.append(row)
        
for phage in rowForPhages:
    if phage[0] != "Name":
        phageName = phage[0]
        rows = phageToDataRows[phageName]
    
        totalPrec = 0
    
        precIterator = 0
    
        for row in rows:
            if row[11] != "*":
                totalPrec += row[11]
                precIterator += 1
                
        
        if (precIterator > 0):
            avgPrec = totalPrec/precIterator
        else:
            avgPrec = "*"
            
        rowForPhages[rowForPhages.index(phage)].insert(8, avgPrec)
    else:
        rowForPhages[rowForPhages.index(phage)],insert(8, "Precipitation")
        
