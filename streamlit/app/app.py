import streamlit as st
from classes import Match, roles
import matplotlib.pyplot as plt

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


def execute_v3():
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


res_ocr = {
    "time":
    {
        "time_sec":
        [
            "44",
            99.99
        ],
        "time_min":
        [
            "31",
            99.99
        ]
    },
    "score":
    {
        "red_kills":
        [
            "28",
            50.43
        ],
        "red_turrets":
        [
            "7",
            99.99
        ],
        "blue_kills":
        [
            "19",
            100.0
        ],
        "blue_turrets":
        [
            "2",
            100.0
        ]
    },
    "gold":
    {
        "red_golds":
        [
            "57.9k",
            99.75
        ],
        "blue_golds":
        [
            "55.4k",
            99.7
        ]
    },
    "cs":
    {
        "blue_sup_cs":
        [
            "43",
            100.0
        ],
        "red_mid_cs":
        [
            "250",
            100.0
        ],
        "blue_mid_cs":
        [
            "272",
            100.0
        ],
        "red_sup_cs":
        [
            "35",
            100.0
        ],
        "red_top_cs":
        [
            "229",
            100.0
        ],
        "blue_top_cs":
        [
            "176",
            100.0
        ],
        "red_adc_cs":
        [
            "197",
            99.96
        ],
        "red_jgl_cs":
        [
            "173",
            100.0
        ],
        "blue_adc_cs":
        [
            "256",
            100.0
        ],
        "blue_jgl_cs":
        [
            "214",
            97.66
        ]
    },
    "kda":
    {
        "blue_top_kda":
        [
            "1/12/3",
            61.77
        ],
        "blue_jgl_kda":
        [
            "7/4/5",
            99.56
        ],
        "red_sup_kda":
        [
            "0/6/9",
            99.93
        ],
        "blue_mid_kda":
        [
            "4/4/4",
            97.42
        ],
        "blue_adc_kda":
        [
            "6/4/8",
            99.15
        ],
        "blue_sup_kda":
        [
            "1/4/14",
            49.69
        ],
        "red_jgl_kda":
        [
            "7/3/9",
            100.0
        ],
        "red_adc_kda":
        [
            "4/6/3",
            99.78
        ],
        "red_mid_kda":
        [
            "5/3/7",
            99.97
        ],
        "red_top_kda":
        [
            "12/1/5",
            99.68
        ]
    }
}

import cv2
from PIL import Image
import numpy
# image = cv2.imread(file_path)
imagee = st.file_uploader("Image")
if imagee:
    imag = Image.open(imagee)
    # imag
    st.image(imag, width=250)
    # imag = numpy.array(imag)  # Ce qu'on enverra a l'api pour l'ocr
    # print(type(imag))
    # st.write(type(imag))
    # imag
    # st.image(imag, width=250)


st.title("Welcome to League of Predicts")
pages = [f'V{i}' for i in range(1, 6)]
page = st.sidebar.radio('Page', pages, index=2)
if page == pages[2]:
    execute_v3()
else:
    st.error("Mauvais choix")