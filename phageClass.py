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

# Given a directory and a list of names, return those file names which are in the given directory and contain the names.
def getfileswithname(fdir, names):
	return [f for f in listdir(fdir) if isfile(join(fdir, f)) and all([x in f for x in names])]


# Given a file location of a file with phage names along with their accession number, return a dictionary with phages as the keys and their accession numbers as keys.
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


# Given a phage-accession dictionary, parse GenBank and write separate gb files in the given directory.
def write_genbank_from_accession_numbers(phage_acession_number_dict, fdir='accession_records/'):
	phages = list(phage_acession_number_dict.keys())
	for i, phage in enumerate(phages):
		print(f'Phage: {phage} --- {round(i / len(phages) * 100, 2)}%')
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
				line = handle.readline()
				with open(fdir + accession_number + GB_EXT, "a") as file:
	   		 		file.write(line)
				if line == '//':
					EOF = True
			break

print('Loading phage accession numbers ...')
phage_acession_number_dict = get_accession_numbers(phage_accession_numbers_file)

dbase = "nucleotide"
Entrez.email = "ejm374@drexel.edu"
batchsize = 100
retmax = 10**9
GB_EXT = '.gb'
op_dir = 'accession_records/'

ssl._create_default_https_context = ssl._create_unverified_context

if False: #Only run if you need to pooulate accession_records directory
	print('Creating genbank files from accession numbers ...')
	write_genbank_from_accession_numbers(phage_acession_number_dict, fdir=op_dir)


for file in getfileswithname(op_dir, GB_EXT):
	for record in SeqIO.parse(op_dir + file, "genbank"):
		a = record
	quit()

