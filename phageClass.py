from noaa_sdk import noaa
from Bio import SeqIO, Entrez


import csv
from collections import defaultdict
import sys
import os
import ssl

phage_accession_numbers_file = 'data/PhagesDB_accession_numbers.txt'

def get_accession_numbers(fdir = 'data/PhagesDB_accession_numbers.txt'):
	phage_acession_number_dict = defaultdict(list)
	with open(phage_accession_numbers_file) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter='\t')
		line_count = 0
		for row in csv_reader:
			phage_name = row[0]
			for entry in row[1:]:
				phage_acession_number_dict[phage_name].append(entry)
	return phage_acession_number_dict


phage_acession_number_dict = get_accession_numbers(phage_accession_numbers_file)

dbase = "nucleotide"
Entrez.email = "ejm374@drexel.edu"
batchsize = 100
retmax = 10**9
GB_EXT = ".gb"
op_dir = 'accession_records/'

ssl._create_default_https_context = ssl._create_unverified_context

for phages in list(phage_acession_number_dict.keys()):
	for accession_numbers in phage_acession_number_dict[phages]:
		handle = Entrez.efetch(db="nucleotide", id=accession_numbers, rettype="gb", retmode="text")
		EOF = False
		while not EOF:
			line = handle.readline().strip()
			print(line)
			if line == '//':
				EOF = True
		quit()
