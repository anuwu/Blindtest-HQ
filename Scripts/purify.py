"""
Takes in the raw double file and outputs a file of pure galaxies
"""

import sys
import os
import numpy as np
import pandas as pd
from importlib import reload

import purify_helper as ph
ph = reload(ph)

fits_dir = "FITS"

def process_result (raw_doubles_csv) :
	"""
	Parses a batch of results -
	rescsv		- csv file containing relative pixel coordinates of the peaks in each band
	"""

	raw_pd = pd.read_csv(raw_doubles_csv, usecols=['objid', 'ra', 'dec',
		'u-type', 'u-peaks',
		'g-type', 'g-peaks',
		'r-type', 'r-peaks',
		'i-type', 'i-peaks',
		'status']
	, dtype=object)

	pure_csv, impure_csv = 'pure_pids.csv', 'Impure.csv'
	pure_df, impure_df = None, None
	if not os.path.exists(pure_csv) :
		pure_file = open(pure_csv, 'w')
		pure_file.write('objid,bands,pid1,pid2\n')
	else :
		pure_file = open(pure_csv, 'a')
		pure_df = pd.read_csv(pure_csv, dtype=object)

	if not os.path.exists(impure_csv) :
		impure_file = open(impure_csv, 'w')
		impure_file.write("objid,ra,dec\n")
	else :
		impure_file = open(impure_csv, 'a')
		impure_df = pd.read_csv(impure_csv, dtype=object)
	
	gres = {}
	for i, row in raw_pd.iterrows() :
		objid, ra, dec = tuple(row[['objid', 'ra', 'dec']])

		if not os.path.exists("Cutouts/{}.jpeg".format(objid)) :
			continue

		if pure_df is not None and ((pure_df['objid'] == objid).any() \
		or impure_df is not None and (impure_df['objid'] == objid).any()) :
			print ("{} --> Done".format(objid))
			continue

		if row['u-type'] == "ERROR" :
			gres[objid] = {'u-n' : 0, 'u-p' : [],
			'g-n' : 0, 'g-p' : [],
			'r-n' : 0, 'r-p' : [],
			'i-n' : 0, 'i-p' : []
			}
			print("{},,,".format(objid))
			impure_file.write("{},{},{}\n".format(objid, ra, dec))
			continue

		gres[objid] = {}
		for b in "ugri" :
			b_type = b + "-type"
			b_peaks = b + "-peaks"
			gres[objid][b+"-n"] = ph.parse_type(row[b_type])
			gres[objid][b+"-p"] = ph.parse_peaks(row[b_peaks], gres[objid][b+"-n"])

		proc_peaks = []
		purity = True
		doub, doub_band, obs_bands = False, None, ''
		for b in "ugri" :
			if gres[objid][b+"-n"] == 2 :
				doub = True
				doub_band = b
				obs_bands += b
				if not proc_peaks :
					proc_peaks = [gres[objid][b+"-p"]]
				else :
					pure_all = True
					for pp in proc_peaks :
						p1_1 = pp[0]
						p1_2 = pp[1]
						p2_1, p2_2 = tuple(gres[objid][b+"-p"])

						truths = [
							x in ph.tolNeighs(y, 3)
							for x in [p1_1, p1_2]
							for y in [p2_1, p2_2]
						]

						if not ((truths[0] and truths[3]) or (truths[1] and truths[2])) :
							pure_all = False
							break

					if pure_all :
						proc_peaks.append(gres[objid][b+"-p"])
					else :
						purity = False
						break

		o1, o2 = ph.double_peak_ids(objid, (ra, dec), doub_band, gres[objid][doub_band + '-p']) \
				if doub and purity \
				else (None, None)

		if None in [o1, o2] :
			impure_file.write("{},{},{}\n".format(objid, ra, dec))
		else :
			pure_file.write("{},{},{},{}\n".format(objid, obs_bands, o1, o2))

		print("{},{},{},{}".format(objid, obs_bands, o1, o2))

	pure_file.close()
	impure_file.close()


if __name__ == '__main__':
	if not os.path.isdir(fits_dir) :
		os.mkdir(fits_dir)

	print("objid,bands,pid1,pid2")
	process_result(sys.argv[1])

	os.system("rm -rf FITS/")