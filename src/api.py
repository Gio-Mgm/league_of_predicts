########################
#    DEPENDENCIES      #
########################

# pip install fastapi
# pip install uvicorn[standard]
# pip install pickle5
# pip install joblib

########################
#       IMPORTS        #
########################

from fastapi import FastAPI, File, UploadFile

import joblib
import sys
import os
import numpy as np
sys.path.append('../src')
from ocr.cropping import crop_numericals
from ocr.detection import extract_results
import pandas as pd
import pickle5 as pickle
from database import Database
from PIL import Image
from config import USER, PASSWORD # Build your own config file

app = FastAPI()

# Connect to SQL
DB_NAME = 'lol_db'
filename = '/home/apprenant/Documents/simplon_dev/python_sql/lol_api/regression_logistique'

########################
#      API ROUTES      #
########################


# Route test
@app.get("/")
async def root():
    return {"msg": "Hello World"}

#------------------------------------#
# GET requests

@app.get('/matchs')
async def get_all_matchs():
    """
    Get the list of all matchs
    """
    db = Database('localhost', USER, PASSWORD, DB_NAME)
    # Connection to the db
    con = db.db_connection()
    cursor = con.cursor()
    use_query = "USE {}".format(DB_NAME)
    query = """
            SELECT * FROM game LIMIT 1000
            """
    cursor.execute(use_query)
    cursor.execute(query)
    matchs = cursor.fetchall()
    db.disconnect_db()
    cursor.close()

    return {'matchs': matchs}


@app.get('/match_id/{match_id}')
async def get_one_match(match_id):
    """
    Get all timelines about a particuliar match
    """
    db = Database('localhost', USER, PASSWORD, DB_NAME)
    # Connection to the db
    con = db.db_connection()
    cursor = con.cursor()
    use_query = "USE {}".format(DB_NAME)
    query = """
            SELECT * FROM game WHERE match_ID = %s
            """
    cursor.execute(use_query)
    cursor.execute(query, (match_id,))
    match = cursor.fetchall()
    db.disconnect_db()
    cursor.close()
    return {'match_id': match}

@app.get('/predicts/{blue_gold}/{red_gold}/{timeline}/{blue_kills}/{red_kills}')
async def get_predictions(blue_gold :int, red_gold :int, timeline :int, blue_kills :int, red_kills :int):
    """
    Predict the win rate by timeline
    """

    classifier = joblib.load(open(filename, 'rb'))
    predictions = classifier.predict([[blue_gold, red_gold, timeline, blue_kills, red_kills]])
    predictions_proba = classifier.predict_proba([[blue_gold, red_gold, timeline, blue_kills, red_kills]])

    print(predictions)
    print(predictions_proba)

    labels = ["Lose","Win"]
    data = {
        'Blue Win' : {
            'Probabilities' : predictions_proba[0][1]
        },
        'Blue lose' : {
            'Probabilities' : predictions_proba[0][0]
        },
        'Prediction' : labels[predictions[0]]

    }

    return data


@app.post('/upload_image/')
async def upload_image(data):
    """
        Upload image
    """
    # print(data)
    # with open('temp_img', "wb") as f:
    #     f.write(data.image.getbuffer())
    #data['image'].save("temp_img.png")
    crop_numericals(data["image"])
    return {"res": extract_results()}

@app.post('/predict/}')
async def predict_who_win(match):
    """
        Predict who_win with probabilities
    """
    data_picture = [
        match.timer, match.blue_team_towers, match.red_team_towers, match.blue_team_golds, match.red_team_golds,
        match.blue_team_top_kills, match.blue_team_top_deaths, match.blue_team_top_assists,
        match.blue_team_jgl_kills, match.blue_team_jgl_deaths, match.blue_team_jgl_assists,
        match.blue_team_mid_kills, match.blue_team_mid_deaths, match.blue_team_mid_assists,
        match.blue_team_adc_kills, match.blue_team_adc_deaths, match.blue_team_adc_assists,
        match.blue_team_sup_kills, match.blue_team_sup_deaths, match.blue_team_sup_assists,
        match.red_team_top_kills, match.red_team_top_deaths, match.red_team_top_assists,
        match.red_team_jgl_kills, match.red_team_jgl_deaths, match.red_team_jgl_assists,
        match.red_team_mid_kills, match.red_team_mid_deaths, match.red_team_mid_assists,
        match.red_team_adc_kills, match.red_team_adc_deaths, match.red_team_adc_assists,
        match.red_team_sup_kills, match.red_team_sup_deaths, match.red_team_sup_assists
    ]
                    
    classifier = joblib.load(open(filename, 'rb'))
    predictions = classifier.predict([data_picture])
    predictions_proba = classifier.predict_proba([data_picture])

    print(predictions)
    print(predictions_proba)

    labels = ["Lose","Win"]
    data_predict = {
        'Blue Win' : {
            'Probabilities' : predictions_proba[0][1]
        },
        'Blue lose' : {
            'Probabilities' : predictions_proba[0][0]
        },
        'Prediction' : labels[predictions[0]]

    }

    return data_predict
