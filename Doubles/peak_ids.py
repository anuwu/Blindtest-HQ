import sys
import os
import re
import requests
import bs4
import numpy as np
import pandas as pd
from importlib import reload
from astropy.wcs.utils import pixel_to_skycoord


# Relative path to the DAGN-Blindtest source files
sys.path.append(str(os.path.abspath(
	os.path.join(os.getcwd(), "../../Source/DAGN-Blindtest")
	)))

import sdss_scrape as scrap
import fits_proc as fp
scrap = reload(scrap)
fp = reload(fp)


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


def cood_to_objid (cood) :
	""" Takes (ra, dec) coordinates and tries to return an SDSS objid
	if an object is catalogued at that coordinate """

	link = "https://skyserver.sdss.org/dr12/en/tools/explore/summary.aspx?ra={}&dec={}"\
			.format(cood.ra.deg, cood.dec.deg)
	soup = bs4.BeautifulSoup(requests.get(link).text, features='lxml')
	if len(soup.select(".nodatafound")) == 1 :
		return '', ''

	st = str(soup.findAll("td", {"class": "t"})[6])
	return st[st[:-1].rfind('>')+1 : st.rfind('<')]


def peak_to_objid (objid, cood, fitsPath, plist) :
	""" Takes an SDSS objid, path to the FITS file
	and returns the SDSS objids (if they exist) corresponding
	to the pixel coordinates of the peaks in 'plist' """

	cutout = fp.cutout(fitsPath, cood, 40)
	cood1 = pixel_to_skycoord(plist[0][0], plist[0][1], cutout.wcs)
	cood2 = pixel_to_skycoord(plist[1][0], plist[1][1], cutout.wcs)


	return cood_to_objid(cood1), cood_to_objid(cood2)
	# return [(cood1.ra.deg, cood1.dec.deg), (cood2.ra.deg, cood2.dec.deg)]


def parse_result (coodcsv, rescsv) :
	cood_pd = pd.read_csv(coodcsv, usecols=['objid', 'ra', 'dec'], dtype=object)
	doub_pd = pd.read_csv(rescsv, usecols=['objid', 
		'u-type', 'u-peaks',
		'g-type', 'g-peaks',
		'r-type', 'r-peaks',
		'i-type', 'i-peaks',
		'z-type', 'z-peaks']
	, dtype=object)
	
	gres = {}
	for i in range(len(doub_pd['objid'])) :
		objid = doub_pd.loc[i, 'objid'] 
		if doub_pd.loc[i, 'u-type'] == "ERROR" :
			gres[objid] = {'u-n' : 0, 'u-p' : [],
			'g-n' : 0, 'g-p' : [],
			'r-n' : 0, 'r-p' : [],
			'i-n' : 0, 'i-p' : [],
			'z-n' : 0, 'z-p' : []
			}
			print("{},,".format(objid))
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
			bns = np.array([
				gres[objid][b+"-n"] for b in "ugri"
			])
			band = "ugri"[
				np.argmin(np.where(bns == 2, range(-4,0), range(4)))
			]
			
			fits_fold = os.path.join(os.getcwd(), "FITS")
			fits_path = os.path.join(fits_fold, objid + "-{}.fits".format(band))

			if not os.path.exists(fits_path) :
				repoLink = scrap.scrapeRepoLink(objid)
				dlinks = scrap.scrapeBandLinks(repoLink)
				scrap.downloadExtract(objid, 
									band, 
									dlinks[band], 
									os.path.join(os.getcwd(), "FITS"), 
									fits_path)

	
			o1, o2 = peak_to_objid(objid, 
							(cood_pd.loc[i, 'ra'], cood_pd.loc[i, 'dec']),
							fits_path, 
							gres[objid][band + "-p"])
			os.remove(fits_path)
		else :
			o1, o2 = '', ''
		
		print("{},{},{}".format(objid, o1, o2))


if __name__ == '__main__':
	print("objid,pid1,pid2")
	for file in sys.argv[1:] :
		parse_result(os.path.join(file, file+".csv"), os.path.join(file, file+"_result.csv"))