from noaa_sdk import noaa
from Bio import SeqIO, Entrez


import csv
from collections import defaultdict
import sys
import os
from os import listdir
from os.path import isfile, join
import urllib
import ssl

phage_accession_numbers_file = 'data/PhagesDB_accession_numbers.txt'

def getfileswithname(fdir, names):			# make name a list
	return [f for f in listdir(fdir) if isfile(join(fdir, f)) and all([x in f for x in names])]


def get_accession_numbers(fdir = 'data/PhagesDB_accession_numbers.txt'):
	phage_acession_number_dict = defaultdict(list)
	with open(phage_accession_numbers_file) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter='\t')
		line_count = 0
		for row in csv_reader:
			phage_name = row[0]
			for entry in row[1:]:

				if entry != '':
					phage_acession_number_dict[phage_name].append(entry)

	return phage_acession_number_dict


def write_genbank_from_accession_numbers(phage_acession_number_dict):
	phages = list(phage_acession_number_dict.keys())
	for i, phage in enumerate(phages):
		print(f'Phage: {phage} --- {format(i / len(phages) * 100, '.2f')}%')
		for accession_number in phage_acession_number_dict[phage]:
			try:
				handle = Entrez.efetch(db="nucleotide", id=accession_number, rettype="gb", retmode="text")
			except urllib.error.HTTPError:
				print(f'Could not retrieve accession number {accession_number}') 
				continue
			except Exception as e:
				print(f'Some other error occured for accession numbe {accession_number}')
				print(e)
				continue
			EOF = False
			while not EOF:
				line = handle.readline().strip()
				with open(op_dir + accession_number + GB_EXT, "a") as file:
	   		 		file.write(line + '\n')
				if line == '//':
					EOF = True

print('Loading phage accession numbers ...')
phage_acession_number_dict = get_accession_numbers(phage_accession_numbers_file)

dbase = "nucleotide"
Entrez.email = "ejm374@drexel.edu"
batchsize = 100
retmax = 10**9
GB_EXT = '.gb'
op_dir = 'accession_records/'

ssl._create_default_https_context = ssl._create_unverified_context

if True: #Only run if you need to pooulate accession_records directory
	print('Creating genbank files from accession numbers ...')
	write_genbank_from_accession_numbers(phage_acession_number_dict)


for file in getfileswithname(op_dir, GB_EXT):
	for record in SeqIO.parse(op_dir + file, "genbank"):
		print(record)
		quit()8

