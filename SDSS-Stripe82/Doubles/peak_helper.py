import sys
import os
import re
import requests
import bs4
from importlib import reload
from astropy.wcs.utils import pixel_to_skycoord

sys.path.append(str(os.path.abspath(
	os.path.join(os.getcwd(), "../../DAGN-Blindtest")
	)))

import sdss_scrape as scrap
import fits_proc as fp
import plane_coods as pc
scrap = reload(scrap)
fp = reload(fp)

tolNeighs = pc.tolNeighs

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

	os.remove(fitsPath)
	return cood_to_objid(cood1), cood_to_objid(cood2)

def double_peak_ids (objid, cood, band, plist) :
	"""
	Returns the object ids corresponding to
	the double peaks in a band -
	objid 		- objid of double detection
	cood 		- coordinate of the object
	band  		- one of 'ugriz'
	plist 		- peak list [(p1x, p1y), (p2x, p1y)]
	"""

	fits_fold = os.path.join(os.getcwd(), "FITS")
	fits_path = os.path.join(fits_fold, objid + "-{}.fits".format(band))

	if not os.path.exists(fits_path) :
		repoLink = scrap.scrapeRepoLink(objid)
		dlinks = scrap.scrapeBandLinks(repoLink)
		scrap.downloadExtract(objid, 
							band, 
							dlinks[band], 
							fits_fold, 
							fits_path)

	return peak_to_objid(objid, 
						cood,
						fits_path, 
						plist)