import sys
import os
import numpy as np
import pandas as pd
from importlib import reload

import peak_helper as ph
ph = reload(ph)

# Relative path to the DAGN-Blindtest source files

def process_result (coodcsv, rescsv) :
	"""
	Parses a batch of results -
	coodcsv		- csv file containing objid, ra, dec
	rescsv		- csv file containing relative pixel coordinates of the peaks in each band
	"""

	cood_pd = pd.read_csv(coodcsv, usecols=['objid', 'ra', 'dec'], dtype=object)
	doub_pd = pd.read_csv(rescsv, usecols=['objid', 
		'u-type', 'u-peaks',
		'g-type', 'g-peaks',
		'r-type', 'r-peaks',
		'i-type', 'i-peaks']
	, dtype=object)
	
	gres = {}
	for i in range(len(doub_pd['objid'])) :
		objid = doub_pd.loc[i, 'objid'] 
		if doub_pd.loc[i, 'u-type'] == "ERROR" :
			gres[objid] = {'u-n' : 0, 'u-p' : [],
			'g-n' : 0, 'g-p' : [],
			'r-n' : 0, 'r-p' : [],
			'i-n' : 0, 'i-p' : []
			}
			print("{},,,".format(objid))
			continue

		gres[objid] = {}
		for b in "ugri" :
			b_type = b + "-type"
			b_peaks = b + "-peaks"
			tp = doub_pd.loc[i, b_type]
			gres[objid][b+"-n"] = ph.parse_type(doub_pd.loc[i, b_type])
			gres[objid][b+"-p"] = ph.parse_peaks(doub_pd.loc[i, b_peaks], gres[objid][b+"-n"])

		proc_peaks = []
		purity = True
		doub = False
		for b in "ugri" :
			if gres[objid][b+"-n"] == 2 :
				doub = True
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
			bns = np.array([
				gres[objid][b+"-n"] for b in "ugri"
			])
			band = "ugri"[
				np.argmin(np.where(bns == 2, range(-4,0), range(4)))
			]

			o1, o2 = ph.double_peak_ids(objid,
									(cood_pd.loc[i, 'ra'], cood_pd.loc[i, 'dec']),
									band, 
									gres[objid][band + "-p"])
		else :
			o1, o2 = '', ''
		
		print("{},{},{},{}".format(objid, obs_bands, o1, o2))


if __name__ == '__main__':
	if not os.path.isdir("FITS") :
		os.mkdir("FITS")

	print("objid,bands,pid1,pid2")
	for file in sys.argv[1:] :
		pth = os.path.join("Batches", file)
		process_result(os.path.join(pth, file+".csv"), os.path.join(pth, file+"_result.csv"))