# -*- coding: utf-8 -*-
"""
Ethan Moyer

Go here for help.
https://github.com/stewartwatts/noaahist
"""

import csv

with open("infile.txt", 'w') as r:
    with open('phagedata/PhagesDB_Data.txt', "r") as f:
        
        for phage in csv.DictReader(f, delimiter='\t'):        
            name = phage['Phage Name']
            host = phage['Host'][0:13]        
            annotated = phage['Annotation Status']
            
            country = phage['Found Country'].lower()
            
            lat_str = phage['Found GPS Lat'].strip()
            lon_str = phage['Found GPS Long'].strip()
            
            if len(lat_str) > 0 and lat_str.find(' ') > lat_str.find('.'):
                lat = float(lat_str[:-2].strip())
                lat = -1 * lat if not lat_str.find('W') else lat
            else:
                lat = None
                
            if len(lon_str) > 0 and lat_str.find(' ') > lat_str.find('.'):
                lon = float(lon_str[:-2].strip())
                lon = -1 * lon if lon_str.find('S') else lon
            else:
                lon = None
                
            if (host == "Mycobacterium" and annotated == "In GenBank" and 
                (country == "united states" or country == "us" or country == "usa" or country == "u.s.a." or 
                country == "united states of america")) and lat is not None and lon is not None:
                                              
                #finds year 
                year = phage['Year Found']
                #r.write(zip OR lat,lon | date OR startdate,enddate | field1,field2,...)
                r.write(name + '|' + year + "0101," + year + "1231" + '|' + str(lat) + ',' + str(lon) + '|' + 'MAX,MIN,SKC,STP,ALT,PCP01' + '\n')
