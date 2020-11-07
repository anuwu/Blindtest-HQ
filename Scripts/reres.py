"""
Reads in the 'raw_doubles.csv' input
and redownloads the galaxies whose
status has been marked as 'fail'
"""

import os
import pandas as pd
from res import download_cutout

df = pd.read_csv('raw_doubles.csv')

for i, row in df.iterrows() :
	objid = row['objid']
	cutout_path = os.path.join("Cutouts/{}.jpeg".format(objid))
	if row['status'] == 'fail' and not os.path.exists(cutout_path) :
		ra = row['ra']
		dec = row['dec']
		download_cutout(ra, dec, cutout_path)
		print(objid)