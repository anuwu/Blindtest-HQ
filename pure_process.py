"""
Takes in the raw double file and outputs a file of pure galaxies
"""

import sys
import os
import numpy as np
import pandas as pd
from importlib import reload

import peak_helper as ph
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

	pure_file = open("pure_pids.csv", "w")
	impure_file = open("impure.csv", "w")
	pure_file.write("objid,bands,pid1,pid2")
	impure_file.write("objid,ra,dec")

	gres = {}
	for i in range(len(raw_pd['objid'])) :
		objid = (raw_pd.loc[i, 'objid'], 
						raw_pd.loc[i, 'ra'], 
						raw_pd.loc[i, 'dec']
						)
		if raw_pd.loc[i, 'u-type'] == "ERROR" :
			gres[objid] = {'u-n' : 0, 'u-p' : [],
			'g-n' : 0, 'g-p' : [],
			'r-n' : 0, 'r-p' : [],
			'i-n' : 0, 'i-p' : []
			}
			print("{},,,".format(objid))
			impure_file.write("{},{},{}".format(objid, ra, dec))
			continue

		gres[objid] = {}
		for b in "ugri" :
			b_type = b + "-type"
			b_peaks = b + "-peaks"
			tp = raw_pd.loc[i, b_type]
			gres[objid][b+"-n"] = ph.parse_type(raw_pd.loc[i, b_type])
			gres[objid][b+"-p"] = ph.parse_peaks(raw_pd.loc[i, b_peaks], gres[objid][b+"-n"])

		proc_peaks = []
		purity = True
		doub, doub_band = False, None
		for b in "ugri" :
			if gres[objid][b+"-n"] == 2 :
				doub = True
				doub_band = b
				if not proc_peaks :
					proc_peaks = [gres[objid][b+"-p"]]
				else :
					pure_all = True
					for pp in proc_peaks :
						p1_1 = pp[0]
						p1_2 = pp[1]
						p2_1, p2_2 = tuple(gres[objid][b+"-p"])

						if not (
							p1_1 in ph.tolNeighs(p2_1, 3) and p1_2 in ph.tolNeighs(p2_2, 3) or \
							p1_1 in ph.tolNeighs(p2_2, 3) and p1_2 in ph.tolNeighs(p2_1, 3)
						) :
							pure_all = False
							break

					if pure_all :
						proc_peaks.append(gres[objid][b+"-p"])
					else :
						purity = False
						break

		obs_bands = ''
		for b in [b for b in "ugri" if gres[objid][b+"-n"] == 2] :
			obs_bands += b

		if doub and purity :
			o1, o2 = ph.double_peak_ids(objid,
									(raw_pd.loc[i, 'ra'], raw_pd.loc[i, 'dec']),
									doub_band, 
									gres[objid][doub_band + "-p"])
			pure_file.write("{},{},{},{}".format(objid, obs_bands, o1, o2))
		else :
			o1, o2 = '', ''
			impure_file.write("{},{},{}".format(objid, ra, dec))
		
		print("{},{},{},{}".format(objid, obs_bands, o1, o2))

	pure_file.cpose()
	impure_file.ciose()


if __name__ == '__main__':
	if not os.path.isdir(fits_dir) :
		os.mkdir(fits_dir)

	print("objid,bands,pid1,pid2")
	process_result(sys.argv[1])