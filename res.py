import sys
import os
import pandas as pd
import urllib

def batchRes (incsv, outcsv) :
    """ For an input, output csv file pair, downloads the images
    of the galaxies classified as double in any band except the
    z-band """

    gal = pd.read_csv(incsv, usecols=['objid', 'ra', 'dec'], dtype=object)
    res = pd.read_csv(outcsv, usecols=['objid', 'u-type', 'u-peaks',
                                                'g-type', 'g-peaks',
                                                'r-type', 'r-peaks',
                                                'i-type', 'i-peaks',
                                                'z-type', 'z-peaks']
                            , dtype=object)

    print (gal)
    print (res)



def main (flist) :

    print (flist)
    for f in flist :
        i = 1

        while os.path.isdir(os.path.join(f, "{}{}".format(f, i))) :
            fn = "{}{}".format(f, i)
            fp = os.path.join(f, "{}{}".format(f, i))
            print (fn)
            batchRes (os.path.join(fp, fn + ".csv"), os.path.join(fp, fn + "_result.csv"))

            # print (fn)
            i += 1
            break
        break


if __name__ == '__main__':
    main(sys.argv[1:])
