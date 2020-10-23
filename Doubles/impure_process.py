import sys
import os
import numpy as np
import pandas as pd
from importlib import reload

import peak_helper as ph
ph = reload(ph)

# Relative path to the DAGN-Blindtest source files

def get_resume (pidsfile) :
	""" Reads the result csv file (if it exists)
	and determines the index where the processing would resume """

	return 0 if not os.path.exists(pidsfile) \
	else len(
		pd.read_csv(pidsfile, usecols=['objid', 'pid1', 'pid2'], dtype=object)
	)

def process_result (coodcsv, rescsv, pidsfile, resume) :
	"""
	Parses a batch of results -
	coodcsv		- csv file containing objid, ra, dec
	rescsv		- csv file containing relative pixel coordinates of the peaks in each band
	pidsfile	- Name of the csv file where the results would be written
	resume 		- index at which processing the result will resume
	"""

	cood_pd = pd.read_csv(coodcsv, usecols=['objid', 'ra', 'dec'], dtype=object)
	doub_pd = pd.read_csv(rescsv, usecols=['objid', 
		'u-type', 'u-peaks',
		'g-type', 'g-peaks',
		'r-type', 'r-peaks',
		'i-type', 'i-peaks',
		'z-type', 'z-peaks']
	, dtype=object)


	if not os.path.exists(pidsfile) :
		outfile = open(pidsfile, "w")
		outfile.write("objid,bands,pid1,pid2\n")
	else :
		outfile = open(pidsfile, "a")
		
	resume = 0 if resume is None else resume
	for i in range(resume, len(doub_pd['objid'])) :
		objid = doub_pd.loc[i, 'objid']
		line = str(doub_pd.loc[i])
		print("Object number --> {}".format(i))
		print(line[:line.rfind('\n')])

		bands = input("Enter the band : ")
		if not bands :
			bands, o1, o2 = '', '', ''
		elif bands == "stop" :
			print("Stopped")
			outfile.close()
			exit()
		else :
			print("Processing...")
			nums = ph.parse_type(doub_pd.loc[i, bands[0]+"-type"])
			plist = ph.parse_peaks(doub_pd.loc[i, bands[0]+"-peaks"], nums)
			o1, o2 = ph.double_peak_ids(objid,
							(cood_pd.loc[i, 'ra'], cood_pd.loc[i, 'dec']),
							bands[0],
							plist)

		outfile.write("{},{},{},{}\n".format(objid, bands, o1, o2))
		print(35*"-")

	outfile.close()

if __name__ == '__main__':
	if not os.path.isdir("FITS") :
		os.mkdir("FITS")

	file = sys.argv[1]
	pth = os.path.join("Batches", file)
	pidsfile = os.path.join(pth, file+"_pids.csv") 
	resume = get_resume(pidsfile)
	
	process_result(os.path.join(pth, file+".csv"), 
				os.path.join(pth, file+"_result.csv"),
				pidsfile,
				resume)