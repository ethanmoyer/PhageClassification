# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 15:13:49 2018

@author: dgolla
"""
import csv
from Bio import SeqIO

#searches for phages that have temperature data against the GenBank phages

#use this when the file is formatted
for seq_record in SeqIO.parse("allPhages.seq", "genbank"):
    
    with open("genelist/" + seq_record.name + ".csv", 'w') as r:
    
        layout = ['GeneID', 'Description', 'Protein Sequence']
        writer = csv.DictWriter(r, fieldnames=layout)
        writer.writeheader()
        
        #add geneID to a list
        for x in range(0, len(seq_record.features)):
            temp = seq_record

            if str(seq_record.features[x].type) == "CDS" and str(seq_record.features[x]).find("translation") != -1 and str(seq_record.features[x]).find("protein_id") != -1:
                proteinSeq = seq_record.features[x].qualifiers['translation'][0]
                proteinID = seq_record.features[x].qualifiers['protein_id'][0]
                note = ""
                if str(seq_record.features[x]).find("note") != -1:
                    note = seq_record.features[x].qualifiers['note'][0]
                #print(proteinSeq + " " + proteinID + " " + note)
                writer.writerow({'GeneID': proteinID, 'Description': note, 'Protein Sequence': proteinSeq})       


