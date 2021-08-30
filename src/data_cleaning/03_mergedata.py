#!/usr/bin/env python

#Descrition
"""Merge all dataframe to create database"""

#Import
import pandas as pd
import json
import timeit
import os

#Paternity
__author__ = "Dewynter Antoine"
__copyright__ = "Copyright 2021, League_of_Predict"
__credits__ = ["DEWYNTER Antoine", "MALGHEM Giovanny", "BILLET Kevin","MEYER Tanguy","FAYEULLE Michael"]
__license__ = "Open_source"
__version__ = "1"
__maintainer__ = "Dewynter Antoine"
__email__ = "Dewynter.cyber@outlook.fr"
__status__ = "Developement"

start = timeit.default_timer()

#Import data
folder = os.listdir("data/02_intermediate/select_data_match/")
dataclear = pd.DataFrame()
cpt = 0

for filename in folder :
    try:
        cpt += 1
        dfmatch = pd.read_csv(f"data/02_intermediate/select_data_match/{filename}",index_col=0) 
        dataclear = pd.concat([dataclear,dfmatch])
        print (cpt,"/" ,len(folder))
    except:
        #Create and fill logerror
        if not os.path.exists("src/data_cleaning/error_file03.txt"):
            error_list  = open("src/data_cleaning/error_file03.txt", "a+")
            error_list.close()
        print("Match",matchid, "non conforme")
        error_list = open("src/data_cleaning/error_file03.txt","a+")
        error_list.write(matchid)
        error_list.write(e)
        error_list.write("\n")
        error_list.close()

#Save data       
dataclear.to_csv("./data/02_intermediate/dataclear.csv")
print (cpt)

stop = timeit.default_timer()
print('Time: ', stop - start) 