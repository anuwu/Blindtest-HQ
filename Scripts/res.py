"""
Takes in a list of <batch>_result.csv files and
downloads their cutouts
"""

import sys
import os
import numpy as np
import pandas as pd
import urllib.request as req

cutout_dir = "Cutouts"
single_series = lambda x : str(list(x)[0])
raw = None

def download_cutout (ra, dec, path) :
	""" Uses the SDSS cutout service to download the object centred at (ra, dec) to 'path' """

	link = "http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?ra={}&dec={}&width=128&height=128".format(ra, dec)
	req.urlretrieve(link, path)

def batchRes (incsv, outcsv, writer) :
	""" For an input, output csv file pair, downloads the images
	of the galaxies classified as le in any band """

	gal = pd.read_csv(incsv, dtype=object)
	try :
		res = pd.read_csv(outcsv, dtype=object)
	except :
		print(outcsv)
		return


	double_ids = res['objid'][
		(res['u-type'] == "DOUBLE") |
		(res['g-type'] == "DOUBLE") |
		(res['r-type'] == "DOUBLE") |
		(res['i-type'] == "DOUBLE")
	]


	for i, objid in double_ids.iteritems() :
		if raw is not None :
			if (raw['objid'] == objid).any() :
				continue 

		row = gal.loc[gal['objid'] == objid]
		ra = str(list(row['ra'])[0])
		dec = str(list(row['dec'])[0])
		try :
			# download_cutout(ra, dec, os.path.join(cutout_dir, "{}.jpeg".format(str(objid))))
			stat = "success"
		except :
			stat = "fail"

		args = (objid, ra, dec) + tuple([
				res.loc[i]["{}-{}".format(b, col)]
				for b in "ugri"
				for col in ["type", "peaks"]
			]) + (stat, )

		# print("{},{},{},{},\"{}\",{},\"{}\",{},\"{}\",{},\"{}\",{}".format(*args))
		# writer.write("{},{},{},{},\"{}\",{},\"{}\",{},\"{}\",{},\"{}\",{}\n".format(*args))
		writer.write("{},{},{},{},\"{}\",{},\"{}\",{},\"{}\",{},\"{}\"\n".format(*args))


def main (flist) :
	global raw
	if not flist :
		return

	if not os.path.isdir(cutout_dir) :
		os.mkdir(cutout_dir)

	if not os.path.exists('raw_doubles.csv') :
		writer = open('raw_doubles.csv', 'w')
		# writer.write("objid,ra,dec,u-type,u-peaks,g-type,g-peaks,r-type,r-peaks,i-type,i-peaks,status\n")
		writer.write("objid,ra,dec,u-type,u-peaks,g-type,g-peaks,r-type,r-peaks,i-type,i-peaks\n")
		# print("objid,ra,dec,u-type,u-peaks,g-type,g-peaks,r-type,r-peaks,i-type,i-peaks,status")
	else :
		writer = open('raw_doubles.csv', 'a')
		raw = pd.read_csv('raw_doubles.csv', dtype=object)
		
	for res_file in flist :
		print ("\n{}\n".format(res_file))
		resind = res_file.find("_result.csv")
		dirind = res_file.rfind("/")
		batch_name = res_file[dirind+1:resind]
		cood_file = res_file[:resind] + ".csv"
		batchRes (cood_file, res_file, writer)

	writer.close()

if __name__ == '__main__':
	main(sys.argv[1:])
	# print(sys.argv[1:])
