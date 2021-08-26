import pandas as pd
import json
import timeit
import os

start = timeit.default_timer()

folder = os.listdir("data/02transform_data/select_data_match/")
dataclear = pd.DataFrame()
cpt = 0

for filename in folder :

    cpt += 1
    dfmatch = pd.read_csv(f"data/02transform_data/select_data_match/{filename}",index_col=0) 
    dataclear = pd.concat([dataclear,dfmatch])
    print (cpt,"/" ,len(folder))

dataclear.to_csv("./data/02transform_data/dataclear.csv")
print (cpt)
stop = timeit.default_timer()

print('Time: ', stop - start) 