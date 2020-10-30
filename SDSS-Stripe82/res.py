import sys
import os
import numpy as np
import pandas as pd
import urllib.request as req

tot = 0
doubs = 0

def download_cutout (ra, dec, path) :
	link = "http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?ra={}&dec={}&width=128&height=128".format(ra, dec)
	req.urlretrieve(link, path)

def batchRes (incsv, outcsv) :
    """ For an input, output csv file pair, downloads the images
    of the galaxies classified as double in any band except the
    z-band """

    global tot, doubs

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

    tot += len(res)
    doubs += len(double_ids)

    for objid in double_ids :
        row = gal.loc[gal['objid'] == objid]
        ra = str(list(row['ra'])[0])
        dec = str(list(row['dec'])[0])
        try :
            download_cutout(ra, dec, os.path.join("DOUBLES", "SDSS_Cutouts", "{}.jpeg".format(str(objid))))
        except :
            tot -= 1
            doubs -= 1
            pass


def main (flist) :
    global tot, doubs

    if not flist :
        return

    tot, doubs = 0, 0
    for f in flist :
        i = 1

        while os.path.isdir(os.path.join(f, "{}{}".format(f, i))) :
            fn = "{}{}".format(f, i)
            fp = os.path.join(f, "{}{}".format(f, i))
            print (fn)
            batchRes (os.path.join(fp, fn + ".csv"), os.path.join(fp, fn + "_result.csv"))

            # print (fn)
            i += 1

    print ("Doubles/Total = {}/{}".format(doubs, tot))


if __name__ == '__main__':
    main(sys.argv[1:])
