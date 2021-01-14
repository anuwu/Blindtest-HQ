import sys
import os
import re
import requests
import bs4
import warnings
from importlib import reload

from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord, Angle
from astropy import units as u
from astropy.utils.exceptions import AstropyWarning
from astropy.wcs.utils import pixel_to_skycoord

#sys.path.append(os.path.abspath(
#	os.path.join(os.getcwd(), "../../DAGN-Blindtest")
#))

warnings.simplefilter('ignore', category=AstropyWarning)

import sdss_scrape as scrap
import plane_coods as pc
scrap = reload(scrap)

tolNeighs = lambda pt, t : pc.tolNeighs(pt, t) + [pt]

def cutout (fitsPath, cood, rad) :
    """
    Performs cutout of FITS file -
        fitsPath            - Directory where FITS file is present
        cood                - (ra, dec) of the object
        rad                 - Radius (in arcseconds) of the cutout
    """

    try :
        hdu = fits.open(fitsPath, memmap=False)[0]
    except Exception as e :
        return None

    wcs = WCS(hdu.header)
    position = SkyCoord(ra=Angle(cood[0], unit=u.deg),
                    dec=Angle(cood[1], unit=u.deg))
    size = u.Quantity((rad, rad), u.arcsec)

    return Cutout2D(hdu.data, position, size, wcs=wcs)

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
		return None

	st = str(soup.findAll("td", {"class": "t"})[6])
	return st[st[:-1].rfind('>')+1 : st.rfind('<')]


def peak_to_objid (objid, cood, fitsPath, plist) :
	""" Takes an SDSS objid, path to the FITS file
	and returns the SDSS objids (if they exist) corresponding
	to the pixel coordinates of the peaks in 'plist' """

	# cutout = fp.cutout(fitsPath, cood, 40)
	ct = cutout(fitsPath, cood, 40)
	cood1 = pixel_to_skycoord(plist[0][0], plist[0][1], ct.wcs)
	cood2 = pixel_to_skycoord(plist[1][0], plist[1][1], ct.wcs)

	os.remove(fitsPath)
	return cood_to_objid(cood1), cood_to_objid(cood2)

def double_peak_ids (objid, cood, band, plist) :
	"""
	Returns the object ids corresponding to
	the double peaks in a band -
	objid 		- objid of double detection
	cood 		- coordinate of the object
	band  		- one of 'ugri'
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
