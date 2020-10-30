import os
import sys
import pandas as pd

sys.path.append(os.path.abspath("../../.."))
import res

def download_row(row) :
        res.download_cutout(row['ra'], row['dec'], "Mou/{}.jpeg".format(row['objid']))
        res.download_cutout(row['ra1'], row['dec1'], "Mou/{}-p1.jpeg".format(row['objid']))
        res.download_cutout(row['ra2'], row['dec2'], "Mou/{}-p2.jpeg".format(row['objid']))

def download_df(df) :
        for i, row in df.iterrows() :
                try :
                        download_row(row)
                        print("{},{},success".format(i, row['objid']))
                except Exception as e :
                        # print("{},{},fail".format(i, row['objid']))
                        print(e)

df = pd.read_csv(sys.argv[1], dtype=object)
# print(df)
download_df(df)
