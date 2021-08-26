import streamlit as st
import matplotlib.pyplot as plt
from src.streamlit.classes import Match, roles
from src.ocr.cropping import crop_numericals
from src.ocr.detection import extract_results

state = st.session_state
if 'pred_blue' not in state:
    state.pred_blue = None
if 'is_hidden_form' not in state:
    state.is_hidden_form = True

# streamlit settings
st.set_page_config(
    page_title="League Of Predicts",
    layout='wide',
    initial_sidebar_state='expanded'
)

def update_pred():
    state.pred_blue = None


def check_proba(curr_val, ref_ocr):
    if ref_ocr[0] == curr_val:
        thresh = 70
        proba = ref_ocr[1]
        if proba < thresh:
            st.warning(f'Veuillez vérifier manuellement cette valeur, {proba}% de certitude')


def execute_v3(res_ocr=None):
    title = st.success("Bienvenue sur la V3")
    match = Match()
    if res_ocr:
        with st.form("Données à entrer"):
            match.set_attr('timer', st.text_input("Veuillez entrer la durée actuelle de la partie",
                                                help="En minutes: 11 ou 11:20",
                                                value=res_ocr['time']['time_min'][0] +
                                                ':' + res_ocr['time']['time_sec'][0]))
            check_proba(str(match.timer).split('.'), res_ocr['time']['time_min'])
            blue, red = st.columns(2)
            columns = [[blue, 'blue'], [red, 'red']]
            for column in columns:
                with column[0]:
                    team = getattr(match, f'{column[1]}_team')
                    team.set_attr('towers', st.text_input(f"Veuillez entrer les tours détruites par l'équipe {column[1]}",
                                                        help=f"Nombre entier entre 1 et 11 inclus",
                                                        value=res_ocr['score'][f'{column[1]}_turrets'][0]))
                    check_proba(team.towers, res_ocr['score'][f'{column[1]}_turrets'])
                    team.set_attr('golds', st.text_input(f"Veuillez entrer les golds de l'équipe {column[1]}",
                                                        help="Exemple: 21.3k",
                                                        value=res_ocr['gold'][f'{column[1]}_golds'][0]))
                    check_proba(team.golds, res_ocr['gold'][f'{column[1]}_golds'])
                    for role in roles:
                        champ = getattr(team, role)
                        champ.set_attr('kda', st.text_input(f'Kda du {role} de l\'équipe {column[1]} ?',
                                                            help='Format Kills/Deaths/Assists',
                                                            value=res_ocr['kda'][f'{column[1]}_{role}_kda'][0]))
                        check_proba(champ.kills+'/'+champ.deaths+'/'+champ.assists,
                                    res_ocr['kda'][f'{column[1]}_{role}_kda'])
                        champ.set_attr('creeps', st.text_input(f'Creeps du {role} de l\'équipe {column[1]} ?',
                                                            help='Nombre entier',
                                                            value=res_ocr['cs'][f'{column[1]}_{role}_cs'][0]))
                        check_proba(champ.creeps, res_ocr['cs'][f'{column[1]}_{role}_cs'])
            submitted = st.form_submit_button("Submit")
            if submitted:
                if match.is_complete_match():
                    if match.is_valid_match():
                        # x = [match.blue_team.golds, match.red_team.golds, match.timer,
                        #      match.blue_team.score, match.red_team.score]
                        # pred_blue = model.predict_proba([x])[0][0]
                        pred_blue = 0.62
                        state.pred_blue = pred_blue
                    else:
                        st.error('Au moins un des KDA est incorrect, veuillez vérifier svp')
                else:
                    st.error('Remplissez correctement tous les champs svp')
        if state.pred_blue:
            if state.pred_blue >= 0.5:
                st.info(f"L'équipe bleue est en train de gagner.\n"
                        f"Sa probabilité de victoire est de {state.pred_blue * 100}%.")
                st.slider("Probabilité de victoire", 0., 100., state.pred_blue*100, format='%f%%' )
            else:
                st.error(f"L'équipe rouge est en train de gagner."
                        f"Sa probabilité de victoire de l'équipe rouge est de {(1 - state.pred_blue) * 100}%.")
                st.slider("Probabilité de victoire", 0., 100., (1-state.pred_blue)*100, format='%f%%')
            st.button("Nouvelle recherche ?", on_click=update_pred)


import os
import time
import cv2
import numpy as np
import requests
import json
from PIL import Image

API_PATH = "http://127.0.0.1:8000"
# image = cv2.imread(file_path)
res_ocr = ""
im = st.file_uploader("Image")
if im:
    img = Image.open(im)
    st.image(img, use_column_width="auto")
    # imag = numpy.array(imag)  # Ce qu'on enverra a l'api pour l'ocr
    # print(type(imag))
    # st.write(type(imag))
    # imag
    # st.image(imag, width=250)

    ###############################################################################
    # imag = numpy.array(imag)
    # imag_path = '../data/ocr/screenshot.png'
    # im = Image.fromarray(imag)
    # file_details = {"FileName": im.name, "FileType": im.type}
    # with open(f'temp_img.png', "wb") as f:
    #     f.write(im.getbuffer())
    # #return st.success("Saved File:{} to tempDir".format(im.name))
    # r = requests.get(API_PATH + '/upload_image')
    # #st.write(res_ocr, res_ocr.json())
    # st.write(r.text)


    # start = time.time()
    # res = requests.post(
    #     API_PATH + '/upload_image/', data={'image': np.array(imag)})
    # st.write(res, res.text)
    # end = time.time()
    # st.sidebar.write(f"Avec API : {end - start}s")

    start = time.time()
    temp_im = os.path.join("data/ocr",'temp_img.png')
    with open(temp_im, "wb") as f:
        f.write(im.getbuffer())
    temp_img = Image.open(temp_im)
    crop_numericals(temp_img)
    res_ocr = extract_results()
    state.is_hidden_form = True
    end = time.time()
    st.sidebar.write(f"Sans API: {end - start}s")



    ###############################################################################

st.title("Welcome to League of Predicts")
pages = [f'V{i}' for i in range(1, 6)]
page = st.sidebar.radio('Page', pages, index=2)
if page == pages[2]:
    state.is_hidden_form and execute_v3() or execute_v3(res_ocr)
else:
    st.error("Mauvais choix")
