import sys
import os
import re
import numpy as np
import pandas as pd


file = "Doubles1_result.csv"

tolNeighs = lambda pt, t : [(pt[0]+dx, pt[1]+dy)
						for dx in range(-t, t+1) for dy in range(-t, t+1)
						if dx or dy]

def parse_type (typestr) :
	""" Parses the galaxy type and returns the number of peaks """

	return 2 if typestr == "DOUBLE" else \
	(1 if typestr == "SINGLE" else 0)

def parse_peaks (peakstr, nums) :
	""" Takes the reported peak string, number of peaks
	and returns a list of 2-D tuple coordinates [(Int, Int)] """

	if not nums :
		return []

	open_inds = [r.start() for r in re.finditer('\(', peakstr)]
	close_inds = [r.start() for r in re.finditer('\)', peakstr)]
	comma_inds = [r.start() for r in re.finditer(',', peakstr)]

	plist = [
		(int(peakstr[o+1:cm]), int(peakstr[cm+2:c]))
		for o, cm, c in zip(open_inds, comma_inds, close_inds)
	]
	
	return plist


def main () :
	doub_pd = pd.read_csv(file, usecols=['objid', 
		'u-type', 'u-peaks',
		'g-type', 'g-peaks',
		'r-type', 'r-peaks',
		'i-type', 'i-peaks',
		'z-type', 'z-peaks']
	, dtype=object)
	
	gres = {}
	pure, impure, errors = [], [], []
	for i in range(len(doub_pd['objid'])) :
		objid = doub_pd.loc[i, 'objid'] 
		if doub_pd.loc[i, 'u-type'] == "ERROR" :
			gres[objid] = {'u-n' : 0, 'u-p' : [],
			'g-n' : 0, 'g-p' : [],
			'r-n' : 0, 'r-p' : [],
			'i-n' : 0, 'i-p' : [],
			'z-n' : 0, 'z-p' : []
			}
			errors.append(objid)
			continue

		gres[objid] = {}
		for b in "ugriz" :
			b_type = b + "-type"
			b_peaks = b + "-peaks"
			tp = doub_pd.loc[i, b_type]
			gres[objid][b+"-n"] = parse_type(doub_pd.loc[i, b_type])
			gres[objid][b+"-p"] = parse_peaks(doub_pd.loc[i, b_peaks], gres[objid][b+"-n"])

		proc_peaks = []
		purity = True
		for b in "ugri" :
			if gres[objid][b+"-n"] == 2 :
				if not proc_peaks :
					proc_peaks = [gres[objid][b+"-p"]]
				else :
					pure_all = True
					for pp in proc_peaks :
						p1_1 = pp[0]
						p1_2 = pp[1]
						p2_1, p2_2 = tuple(gres[objid][b+"-p"])

						if not (
							p1_1 in tolNeighs(p2_1, 3) and p1_2 in tolNeighs(p2_2, 3) or \
							p1_1 in tolNeighs(p2_2, 3) and p1_2 in tolNeighs(p2_1, 3)
						) :
							pure_all = False
							break

					if pure_all :
						proc_peaks.append(gres[objid][b+"-p"])
					else :
						purity = False
						break


		if purity :
			pure.append(objid)
		else :
			impure.append(objid)

	print("Pure sampes = {}".format(len(pure)))
	print("Impure samples = {}".format(len(impure))) 
	print("Erroneous samples = {}".format(len(errors)))


if __name__ == '__main__':
	main()