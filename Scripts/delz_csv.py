import pandas as pd
import sys

def delz (csv) :
        print ("objid,u-type,u-peaks,g-type,g-peaks,r-type,r-peaks,i-type,i-peaks")
        df = pd.read_csv(csv, dtype=object)
        # df[['objid', 'u-type', 'u-peaks', 'g-type', 'g-peaks', 'r-type', 'r-peaks', 'i-type', 'i-peaks']].to_csv(csv, index=False)
        for i, row in df.iterrows() :
                objid = row['objid']
                ut = row['u-type']
                up = row['u-peaks']
                gt = row['g-type']
                gp = row['g-peaks']
                rt = row['r-type']
                rp = row['r-peaks']
                it = row['i-type']
                ip = row['i-peaks']       

                print("{},{},\"{}\",{},\"{}\",{},\"{}\",{},\"{}\"".format(objid, ut, up, gt, gp, rt, rp, it, ip))

if __name__ == "__main__" :
        delz(sys.argv[1])
