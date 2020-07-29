# -*- coding: utf-8 -*-
import csv
import os

geneDictionary = {}

with open("Genetic Data Collection/GenesDict.csv") as geneDict:
    spamreader = csv.reader(geneDict, delimiter=',', quotechar='|')
    for row in spamreader:
        if row != [] and row[0] != "sequence":
            geneDictionary[row[0]] = row[1]
        
relevantPhages = []

for i in range(1, 11):
    with open(("Environmental Data Collection/weather/all" + str(i) + ".csv"), "r") as weatherCSV:
        rowreader = csv.reader(weatherCSV, delimiter=',', quotechar='|')
        for row in rowreader:
            if row[0] != "NAME" and row[0] not in relevantPhages:
                relevantPhages.append(row[0])
                
phageToAccession = {}

with open("Environmental Data Collection/phagedata/PhagesDB_Data.txt" , "r") as f:
    for phage in csv.DictReader(f, delimiter='\t'):
        name = phage['Phage Name']
        accession = phage['Accession #']
        if phage['Phage Name'] in relevantPhages:
            phageToAccession[name] = accession

for phage in relevantPhages:
    accession = phageToAccession[phage]
    

frequencies = {}

        
with open("Genetic Data Collection/phagesToGenes.csv", "w") as phageGenes:
    writer = csv.writer(phageGenes)
    writer.writerow(["Phage Names", "Genes"])
    fileList = os.listdir("Genetic Data Collection/genelist/")
    for phage in relevantPhages:
        accession = phageToAccession[phage]
        
        phageRow = [phage]
        
        if accession + ".csv" in fileList:
            with open("Genetic Data Collection/genelist/" + accession + ".csv") as geneFile:
                genereader = csv.reader(geneFile, delimiter=',', quotechar='|')
                for gene in genereader:
                    if (gene[len(gene) - 1] != "Protein Sequence"):
                        sequence = gene[len(gene) - 1]
                        
                        if (geneDictionary[sequence] not in frequencies.keys()):
                            frequencies[geneDictionary[sequence]] = 0
                            
                        frequencies[geneDictionary[sequence]] += 1
                        phageRow.append(geneDictionary[sequence])
                    
        else:
            phageRow.append("*")
            
        writer.writerow(phageRow)
            