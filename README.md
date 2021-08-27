```
league_of_predicts
 
 ┣ api
 ┣ data
 ┃ ┣ 01_raw
 ┃ ┣ 02_intermediate
 ┃ ┃ ┣ dataclear.csv
 ┃ ┃ ┗ dataclear2.csv
 ┃ ┣ 03_cleaned_data
 ┃ ┃ ┗ cleaned_data.csv
 ┃ ┗ ocr
 ┃ ┃ ┣ cs
 ┃ ┃ ┃ ┣ blue_adc_cs.png
 ┃ ┃ ┃ ┣ blue_jgl_cs.png
 ┃ ┃ ┃ ┣ blue_mid_cs.png
 ┃ ┃ ┃ ┣ blue_sup_cs.png
 ┃ ┃ ┃ ┣ blue_top_cs.png
 ┃ ┃ ┃ ┣ red_adc_cs.png
 ┃ ┃ ┃ ┣ red_jgl_cs.png
 ┃ ┃ ┃ ┣ red_mid_cs.png
 ┃ ┃ ┃ ┣ red_sup_cs.png
 ┃ ┃ ┃ ┗ red_top_cs.png
 ┃ ┃ ┣ gold
 ┃ ┃ ┃ ┣ blue_golds.png
 ┃ ┃ ┃ ┗ red_golds.png
 ┃ ┃ ┣ kda
 ┃ ┃ ┃ ┣ blue_adc_kda.png
 ┃ ┃ ┃ ┣ blue_jgl_kda.png
 ┃ ┃ ┃ ┣ blue_mid_kda.png
 ┃ ┃ ┃ ┣ blue_sup_kda.png
 ┃ ┃ ┃ ┣ blue_top_kda.png
 ┃ ┃ ┃ ┣ red_adc_kda.png
 ┃ ┃ ┃ ┣ red_jgl_kda.png
 ┃ ┃ ┃ ┣ red_mid_kda.png
 ┃ ┃ ┃ ┣ red_sup_kda.png
 ┃ ┃ ┃ ┗ red_top_kda.png
 ┃ ┃ ┣ score
 ┃ ┃ ┃ ┣ blue_kills.png
 ┃ ┃ ┃ ┣ blue_turrets.png
 ┃ ┃ ┃ ┣ red_kills.png
 ┃ ┃ ┃ ┗ red_turrets.png
 ┃ ┃ ┣ time
 ┃ ┃ ┃ ┣ time_min.png
 ┃ ┃ ┃ ┗ time_sec.png
 ┃ ┃ ┣ temp_img
 ┃ ┃ ┗ temp_img.png
 ┣ img
 ┃ ┣ avg_assists_by_team_last_timeline.png
 ┃ ┣ avg_death_by_team.png
 ┃ ┣ avg_kills_by_team.png
 ┃ ┣ avg_kills_by_team_last_timeline.png
 ┃ ┣ gold_win_loss_by_team.png
 ┃ ┣ gold_win_loss_by_team_last_timeline.png
 ┃ ┣ kills_team_all_timeline.png
 ┃ ┣ kills_team_last_timeline.png
 ┃ ┗ win_team_all_timeline.png
 ┣ notebook
 ┃ ┣ data_analysis.ipynb
 ┃ ┣ linear_regression.ipynb
 ┃ ┣ ml_modeles.ipynb
 ┃ ┣ regression_lineaire_lasso
 ┃ ┣ regression_lineaire_ridge
 ┃ ┣ regression_lineaire_simple
 ┃ ┣ regression_logistique
 ┃ ┗ xgboost
 ┣ src
 ┃ ┣ __pycache__
 ┃ ┃ ┣ api.cpython-38.pyc
 ┃ ┃ ┗ config.cpython-38.pyc
 ┃ ┣ data_cleaning
 ┃ ┃ ┣ 01_invalid_data_cuter.py
 ┃ ┃ ┣ 02_json_to_dataframe.py
 ┃ ┃ ┣ 03_mergedata.py
 ┃ ┃ ┗ 04_end_transform.py
 ┃ ┣ database
 ┃ ┃ ┣ __pycache__
 ┃ ┃ ┃ ┣ Database.cpython-38.pyc
 ┃ ┃ ┃ ┗ __init__.cpython-38.pyc
 ┃ ┃ ┣ Database.py
 ┃ ┃ ┣ Match.py
 ┃ ┃ ┗ __init__.py
 ┃ ┣ ocr
 ┃ ┃ ┣ __pycache__
 ┃ ┃ ┃ ┣ cropping.cpython-38.pyc
 ┃ ┃ ┃ ┗ detection.cpython-38.pyc
 ┃ ┃ ┣ cropping.py
 ┃ ┃ ┗ detection.py
 ┃ ┣ streamlit
 ┃ ┃ ┣ __pycache__
 ┃ ┃ ┃ ┣ __init__.cpython-38.pyc
 ┃ ┃ ┃ ┗ classes.cpython-38.pyc
 ┃ ┃ ┣ test
 ┃ ┃ ┃ ┣ __init__.py
 ┃ ┃ ┃ ┗ test_classes.py
 ┃ ┃ ┣ __init__.py
 ┃ ┃ ┗ classes.py
 ┃ ┣ api.py
 ┃ ┗ config.py
 ┣ utils
 ┃ ┗ functions.py
 ┣ .gitignore
 ┣ README.md
 ┣ app.py
 ┣ regression_logistique
 ┣ requirements.txt
 ┣ temp_img
 ┗ test_api.py
```
