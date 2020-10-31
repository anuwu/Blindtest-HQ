"""
Keeps only band for the download cutout jpegs
"""

import os
import sys
import pandas as pd

bands_df = pd.read_csv(os.path.join("Data", "Stripe-82", "stripe82_pids.csv"), dtype=object)[['objid', 'bands']]
for batch in sys.argv[1:] :
        df = pd.read_csv(os.path.join("Batches", batch, "{}.csv".format(batch)), dtype=object) 
        resfold = os.path.join("Batches", batch, "Results")
        for _, row in df.iterrows() :
                objid = row['objid']
                loc = bands_df['objid'] == row['objid']
                conf_bands = list(bands_df[loc]['bands'])[0]
                non_bands = [b for b in "ugri" if b not in conf_bands]
                for b in non_bands :
                        respic = os.path.join(resfold, "{}-{}_result.png".format(objid, b))
                        if os.path.exists(respic) :
                                os.remove(respic)
