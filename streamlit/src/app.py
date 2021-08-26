import streamlit as st
from classes import Match, roles
import requests
from PIL import Image
import numpy as np

state = st.session_state
if 'pred_blue' not in state:
    state.pred_blue = None


def update_pred():
    state.pred_blue = None


def check_proba(curr_val, ref_ocr):
    if ref_ocr[0] == curr_val:
        thresh = 70
        proba = ref_ocr[1]
        if proba < thresh:
            st.warning(f'Veuillez vérifier manuellement cette valeur, {proba}% de certitude')


def execute_app():
    st.success("Bienvenue sur la V3")
    match = Match()
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
                    pred_blue = requests.get('', json=team.list_attributes_values()).json
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


st.title("Welcome to League of Predicts")
imagee = st.file_uploader("Entrez l'image de la partie à analyser")
if imagee:
    imag = Image.open(imagee)
    st.image(imag, width=250)
    res_ocr = requests.get('', json=np.array(imag)).json
    execute_app()
