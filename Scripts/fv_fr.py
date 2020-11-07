"""
Takes a batch result .csv file containing 5 bands and 
converts it into a 4-band csv
"""

import pandas as pd
import sys

def main(csv) :
	df = pd.read_csv(csv, dtype=object)
	cols = ["objid"] + [
		"{}-{}".format(band, ctype)
		for band in "ugri" 
		for ctype in ["type", "peaks"]
	]

	header = cols[0]
	for col in cols[1:] :
		header += ",{}".format(col)
	 
	print(header)
	for i, row in df.iterrows() :
		if row["u-type"] != "ERROR" :
			print("{},{},\"{}\",{},\"{}\",{},\"{}\",{},\"{}\"".format(*tuple(row[cols])))

if __name__ == "__main__" :
	main(sys.argv[1])
