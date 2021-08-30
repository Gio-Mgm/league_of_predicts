#!/usr/bin/env python

#Descrition
"""Use multiple colum for create additional coherent data"""

#Import
import pandas as pd 

#Paternity
__author__ = "Dewynter Antoine"
__copyright__ = "Copyright 2021, League_of_Predict"
__credits__ = ["DEWYNTER Antoine", "MALGHEM Giovanny", "BILLET Kevin","MEYER Tanguy","FAYEULLE Michael"]
__license__ = "Open_source"
__version__ = "1"
__maintainer__ = "Dewynter Antoine"
__email__ = "Dewynter.cyber@outlook.fr"
__status__ = "Developement"

#Import Data
dfmatch = pd.read_csv(f"data/02_intermediate/dataclear.csv",index_col=0) 
number_of_champ = 10

def get_total_sbire_by_champ(df,number_of_champ):
    """
    Add columns that count sbire kills of each players
    Parameters : df => Dataframe, number_of_champ => number of champions
    Return : Modified dataframe
    """
    for i in range(1,(number_of_champ + 1)):
        df[f'total_sbire_kill_{i}'] = df[f'sbireskill_{i}'] + df[f'jungsbirekill_{i}']
        df.drop([f'sbireskill_{i}',f'jungsbirekill_{i}'], axis=1)
    return df

def get_total_item_score_by_champ(df,number_of_champ):
    """
    Add columns that count the total item score of each players
    Parameters : df => Dataframe, number_of_champ => number of champions
    Return : Modified dataframe
    """
    for i in range(1,(number_of_champ +1 )):
        df[f'item_total_score_{i}'] = df[f'item1_{i}'] ** 2 + df[f'item2_{i}'] ** 2 + df[f'item3_{i}'] ** 2 + df[f'item4_{i}'] ** 2 + df[f'item5_{i}'] ** 2 + df[f'item6_{i}'] ** 2
        df.drop([f'item1_{i}',f'item2_{i}',f'item3_{i}',f'item4_{i}',f'item5_{i}',f'item6_{i}',], axis=1)
    return df

dfmatch = get_total_sbire_by_champ(dfmatch,number_of_champ)
dfmatch = get_total_item_score_by_champ(dfmatch,number_of_champ)

#Save data
dfmatch.to_csv("data/03_cleaned_data/cleaned_data.csv")