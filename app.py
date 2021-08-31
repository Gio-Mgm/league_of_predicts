import os
import requests
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from src.streamlit.classes import Match, roles
from src.ocr.cropping import crop_numericals
from src.ocr.detection import extract_results

state = st.session_state
if 'pred_blue' not in state:
    state.pred_blue = None

# streamlit settings
st.set_page_config(
    page_title="League Of Predicts",
    layout='wide',
    page_icon='lop_icon.png',
    initial_sidebar_state='expanded'
)

def update_pred():
    state.pred_blue = None


def check_proba(curr_val, ref_ocr):
    if ref_ocr[0] == curr_val:
        thresh = 70
        proba = ref_ocr[1]
        if proba < thresh:
            st.warning(f'{round(proba)}% de certitude')


API_PATH = "http://127.0.0.1:8000"

res_ocr = ""
st.sidebar.image("lop_icon.png")
im = st.sidebar.file_uploader("Upload a screenshot")
if im:
    

    # st.file_uploader() returns a memory image file
    # so we need to save it locally for openCV
    temp_im = 'temp_img.png'
    with open(temp_im, "wb") as f:
        f.write(im.getbuffer())

    # image loading
    temp_img = Image.open(temp_im)
    crop_numericals(temp_img)
    res_ocr = extract_results()

    match = Match()
    container = st.container()
    with st.form("Données à entrer"):
        blue, img_col, red = st.columns([.15, .7, .15])
        with img_col:
            match.set_attr('timer', st.text_input(
                "Timer",
                help="En minutes: 11 ou 11:20",
                value=res_ocr['time']['time_min'][0] +
                ':' + res_ocr['time']['time_sec'][0]
            ))
            check_proba(
                str(match.timer).split('.'), res_ocr['time']['time_min']
            )
        columns = [[blue, 'blue'], [red, 'red']]
        for column in columns:
            with column[0]:
                if column[1] == 'blue':
                    st.subheader("Blue Team")
                else:
                    st.subheader("Red Team")
                    
                st.markdown("--------")
                team = getattr(match, f'{column[1]}_team')
                team.set_attr('towers', st.text_input(
                    f"Tours détruites",
                    help=f"Nombre entier entre 1 et 11 inclus",
                    key=f'{column[1]}_turrets',
                    value=res_ocr['score'][f'{column[1]}_turrets'][0], 
                ))
                check_proba(
                    team.towers, res_ocr['score'][f'{column[1]}_turrets'])

                team.set_attr('golds', st.text_input(
                    f"Golds",
                    help="Exemple: 21.3k",
                    key=f'{column[1]}_golds',
                    value=res_ocr['gold'][f'{column[1]}_golds'][0]
                ))
                check_proba(
                    team.golds, res_ocr['gold'][f'{column[1]}_golds'])

                for role in roles:
                    champ = getattr(team, role)
                    champ.set_attr('kda', st.text_input(
                        f'K/D/A {role}',
                        help='Format Kills/Deaths/Assists',
                        key=f'{column[1]}_{role}_kda',
                        value=res_ocr['kda'][f'{column[1]}_{role}_kda'][0]
                    ))
                    check_proba(
                        champ.kills+'/'+champ.deaths+'/'+champ.assists,
                        res_ocr['kda'][f'{column[1]}_{role}_kda']
                    )

                    champ.set_attr('creeps', st.text_input(
                        f'Creeps {role}',
                        help='Nombre entier',
                        key=f'{column[1]}_{role}_cs',
                        value=res_ocr['cs'][f'{column[1]}_{role}_cs'][0]
                    ))
                    check_proba(
                        champ.creeps, res_ocr['cs'][f'{column[1]}_{role}_cs']
                    )

        with img_col:
            img = Image.open(im)
            st.image(img, use_column_width="always")
            submitted = st.form_submit_button("Submit")
        if submitted:
            if match.is_complete_match():
                if match.is_valid_match():
                    res = requests.post(
                        API_PATH + '/predict/', json=match.list_attributes_values()
                    )
                    r = res.json()
                    state.pred_blue = r["Blue_Win"]["Probabilities"]
                else:
                    st.error(
                        'Au moins un des KDA est incorrect, veuillez vérifier svp')
            else:
                st.error('Remplissez correctement tous les champs svp')
    if state.pred_blue:
        if state.pred_blue >= 0.5:
            container.markdown(
                "_L'équipe bleue à de plus grandes chances de victoire._"
            )
        else:
            container.header(
                "_L'équipe rouge à de plus grandes chances de victoire._"
                )
        blue_col, red_col = container.columns([state.pred_blue, 1-state.pred_blue])
        with blue_col:
            st.info(f"{round(state.pred_blue * 100, 2)} %")
        with red_col:
            st.error(f"{100 - round(state.pred_blue * 100, 2)} %")
        st.button("Nouvelle recherche ?", on_click=update_pred)
