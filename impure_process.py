"""
Written to work using the raw_doubles.csv file and the Pure.csv file
but I haven't tested it

Have written functions to check objids that have already been processed
because multiprocessing is unreliable and some don't finish at all!
"""

import sys
import os
import logging
import numpy as np
import pandas as pd
import multiprocessing as mp
from importlib import reload

import peak_helper as ph
ph = reload(ph)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_procd_ids (pidsfile) :
	""" Reads the result csv file (if it exists)
	and determines the index where the processing would resume """

	return [] if not os.path.exists(pidsfile) \
	else list(pd.read_csv(pidsfile, usecols=['objid', 'pid1', 'pid2'], dtype=object)['objid'])

def procs_fin (procs) :
	""" Waits for processes to finish """

	if procs != [] :
		print("Waiting for results to get logged...")
		for i, p in enumerate(procs) :
			p.join()
			print("{} --> Logged".format(i+1))

	print("Stopped!")

def process_result (raw_doubles_csv, impure_csv, pidsfile, procd_ids) :
	"""
	Parses a batch of results -
	coodcsv			- csv file containing objid, ra, dec
	rescsv			- csv file containing relative pixel coordinates of the peaks in each band
	pidsfile		- Name of the csv file where the results would be written
	procds_ids 		- ids that have already been processed
	"""

	impure_pd = pd.read_csv(pure_csv, usecols=['objid', 'bands', 'pid1', 'pid2'], dtype=object)
	raw_pd = pd.read_csv(rescsv, usecols=['objid', 'ra', 'dec', 
		'u-type', 'u-peaks',
		'g-type', 'g-peaks',
		'r-type', 'r-peaks',
		'i-type', 'i-peaks',
		'status']
	, dtype=object)
		
	procs = []
	raw_ids = [
		i for i,objid 
		in enumerate(list(raw_pd['objid']))
		if objid not in procd_ids
	]
		
	l = len(raw_ids)
	for j, i in enumerate(raw_ids) :
		if str(list(pure_pd.loc[i]['bands'])[0]) != '' :
			continue

		objid = raw_pd.loc[i, 'objid']
		line = str(raw_pd.loc[i])
		print("Object {} of {}".format(j+1, l))
		print(line[:line.rfind('\n')])

		bands = input("Enter the band : ")
		if not bands :
			bands, o1, o2 = '', '', ''
			log.info("{},{},{},{}".format(objid, bands, o1, o2))
		elif bands == "stop" :
			procs_fin(procs)
			exit()
		else :
			print("Fired process!")
			def csv_writer (objid, cood, bands, typestr, peakstr) :
				nums = ph.parse_type(typestr)
				plist = ph.parse_peaks(peakstr, nums)
				o1, o2 = ph.double_peak_ids(objid, cood, bands[0], plist)
				log.info("{},{},{},{}".format(objid, bands, o1, o2))

			proc = mp.Process(target=csv_writer, args=(objid,
											(cood_pd.loc[i, 'ra'], cood_pd.loc[i, 'dec']),
											bands,
											raw_pd.loc[i, bands[0]+"-type"],
											raw_pd.loc[i, bands[0]+"-peaks"],
											)
			)
			procs.append(proc)
			proc.start()
		
		print(35*"-")

	procs_fin(procs)

if __name__ == '__main__':
	if not os.path.isdir("FITS") :
		os.mkdir("FITS")

	impure_csv = sys.argv[1]
	raw_doubles_csv = sys.argv[2]

	pidsfile = "Impure_pids.csv" 
	if not os.path.exists(pidsfile) :
		fileHandler = logging.FileHandler(pidsfile, mode='w')
		for h in log.handlers :
			log.removeHandler(h)
		log.addHandler(fileHandler)
		log.info("objid,bands,pid1,pid2")
	else :
		fileHandler = logging.FileHandler(pidsfile, mode='a')
		for h in log.handlers :
			log.removeHandler(h)
		log.addHandler(fileHandler)

	procd_ids = get_procd_ids(pidsfile)
	process_result(raw_doubles_csv,
				pure_csv,
				pidsfile,
				procd_ids)
