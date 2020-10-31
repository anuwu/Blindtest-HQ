import sys
import os
import numpy as np
import pandas as pd
import urllib.request as req

cutout_dir = "Cutouts"

def download_cutout (ra, dec, path) :
	""" Uses the SDSS cutout service to download the object centred at (ra, dec) to 'path' """

	link = "http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?ra={}&dec={}&width=128&height=128".format(ra, dec)
	req.urlretrieve(link, path)

def batchRes (incsv, outcsv) :
    """ For an input, output csv file pair, downloads the images
    of the galaxies classified as le in any band except the
    z-band """

    gal = pd.read_csv(incsv, usecols=['objid', 'ra', 'dec'], dtype=object)
    res = pd.read_csv(outcsv, usecols=['objid', 'u-type', 'u-peaks',
                                                'g-type', 'g-peaks',
                                                'r-type', 'r-peaks',
                                                'i-type', 'i-peaks',
                                                'z-type', 'z-peaks']
                            , dtype=object)

    double_ids = res['objid'][
        (res['u-type'] == "DOUBLE") |
        (res['g-type'] == "DOUBLE") |
        (res['r-type'] == "DOUBLE") |
        (res['i-type'] == "DOUBLE")
    ]

    
    for i, objid in double_ids.iteritems() :
        row = gal.loc[gal['objid'] == objid]
        ra = str(list(row['ra'])[0])
        dec = str(list(row['dec'])[0])
        try :
            download_cutout(ra, dec, os.path.join(cutout_dir, "{}.jpeg".format(str(objid))))
            stat = "success"
        except :
            stat = "fail"

        args = (objid, ra, dec) + tuple([
        		res.loc[i]["{}-{}".format(b, col)]
        		for b in "ugri"
        		for col in ["type", "peaks"]
        	]) + (stat, )

        print("{},{},{},{},\"{}\",{},\"{}\",{},\"{}\",{},\"{}\",{}".format(*args))

            
def main (flist) :
    if not flist :
        return

    if not os.path.isdir(cutout_dir) :
        os.mkdir(cutout_dir)
        
    print("objid,ra,dec,u-type,u-peaks,g-type,g-peaks,r-type,r-peaks,i-type,i-peaks,status")
    for res_file in flist :
        i = 1
        resind = res_file.find("_result.csv")
        dirind = res_file.rfind("/")
        batch_name = res_file[dirind+1:resind]
        cood_file = res_file[:resind] + ".csv"
        # print (batch_name)
        batchRes (cood_file, res_file)

        # print (fn)
        i += 1

if __name__ == '__main__':
    main(sys.argv[1:])