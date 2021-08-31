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

from fastapi import FastAPI, Request

import joblib
import numpy as np

#from database import Database
#from config import USER, PASSWORD # Build your own config file

app = FastAPI()

# Connect to SQL
DB_NAME = 'lol_db'
filename = '../models/regression_logistique'

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


@app.post('/predict/')
async def predict_who_win(request: Request):
    """
        Predict who_win with probabilities
    """
    match = await request.json()
    data_picture = np.array([
        match["timer"], match["blue_team_towers"], match["red_team_towers"], match["blue_team_golds"], match["red_team_golds"],
        match["blue_team_top_kills"], match["blue_team_top_deaths"], match["blue_team_top_assists"],
        match["blue_team_jgl_kills"], match["blue_team_jgl_deaths"], match["blue_team_jgl_assists"],
        match["blue_team_mid_kills"], match["blue_team_mid_deaths"], match["blue_team_mid_assists"],
        match["blue_team_adc_kills"], match["blue_team_adc_deaths"], match["blue_team_adc_assists"],
        match["blue_team_sup_kills"], match["blue_team_sup_deaths"], match["blue_team_sup_assists"],
        match["red_team_top_kills"], match["red_team_top_deaths"], match["red_team_top_assists"],
        match["red_team_jgl_kills"], match["red_team_jgl_deaths"], match["red_team_jgl_assists"],
        match["red_team_mid_kills"], match["red_team_mid_deaths"], match["red_team_mid_assists"],
        match["red_team_adc_kills"], match["red_team_adc_deaths"], match["red_team_adc_assists"],
        match["red_team_sup_kills"], match["red_team_sup_deaths"], match["red_team_sup_assists"],
    ])

    data_picture = data_picture.astype(np.float64)
    classifier = joblib.load(open(filename, 'rb'))
    predictions = classifier.predict([data_picture])
    predictions_proba = classifier.predict_proba([data_picture])

    labels = ["Lose","Win"]
    data_predict = {
        'Blue_Win' : predictions_proba[0][0],
        'Prediction' : labels[predictions[0]]
    }
    print(predictions, predictions_proba)
    return data_predict
