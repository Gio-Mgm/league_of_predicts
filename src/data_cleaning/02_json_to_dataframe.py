#Import
import json
import pandas as pd
import numpy as np
import os
import timeit

start = timeit.default_timer()

folder = os.listdir("data/02transform_data/global")
dataclear = pd.DataFrame()
cpt = 0

if not os.path.exists("/data/02transform_data/select_data_match"):
    os.makedirs("/data/02transform_data/select_data_match")

for filename in folder :
    try:
        #Visual intication
        cpt +=1
        matchid = filename.strip("global_.json")
        stop = timeit.default_timer()
        if cpt % 100 == 1 :
            print(cpt,"/",len(folder))
            print('Time: ', round(((stop - start)/60),2)) 
            print('\n')

        #Import Data
        with open(f'./data/02transform_data/global/global_{matchid}.json') as matchglobal:
            matchglobal = json.load(matchglobal)
        with open(f'./data/02transform_data/timeline/timeline_{matchid}.json') as matchtimeline:
            matchtimeline = json.load(matchtimeline)

        COLUMN_NAMES = ["match_ID","timeline","who_win",
                "blue_kill_nashor","blue_kill_herald","blue_kill_fire_drake","blue_kill_air_drake","blue_kill_water_drake","blue_kill_earth_drake","blue_kill_ancient_drake","blue_soul_drake","blue_destr_tower","blue_gold",
                "red_kill_nashor","red_kill_herald","red_kill_fire_drake","red_kill_air_drake","red_kill_water_drake","red_kill_earth_drake","red_kill_ancient_drake","red_soul_drake","red_destr_tower","red_gold",
                "champion_1","level_1","gold_1","kill_1","death_1","assist_1","item1_1","item2_1","item3_1","item4_1","item5_1","item6_1","trinket_1","sbireskill_1","jungsbirekill_1",
                "champion_2","level_2","gold_2","kill_2","death_2","assist_2","item1_2","item2_2","item3_2","item4_2","item5_2","item6_2","trinket_2","sbireskill_2","jungsbirekill_2",
                "champion_3","level_3","gold_3","kill_3","death_3","assist_3","item1_3","item2_3","item3_3","item4_3","item5_3","item6_3","trinket_3","sbireskill_3","jungsbirekill_3",
                "champion_4","level_4","gold_4","kill_4","death_4","assist_4","item1_4","item2_4","item3_4","item4_4","item5_4","item6_4","trinket_4","sbireskill_4","jungsbirekill_4",
                "champion_5","level_5","gold_5","kill_5","death_5","assist_5","item1_5","item2_5","item3_5","item4_5","item5_5","item6_5","trinket_5","sbireskill_5","jungsbirekill_5",
                "champion_6","level_6","gold_6","kill_6","death_6","assist_6","item1_6","item2_6","item3_6","item4_6","item5_6","item6_6","trinket_6","sbireskill_6","jungsbirekill_6",
                "champion_7","level_7","gold_7","kill_7","death_7","assist_7","item1_7","item2_7","item3_7","item4_7","item5_7","item6_7","trinket_7","sbireskill_7","jungsbirekill_7",
                "champion_8","level_8","gold_8","kill_8","death_8","assist_8","item1_8","item2_8","item3_8","item4_8","item5_8","item6_8","trinket_8","sbireskill_8","jungsbirekill_8",
                "champion_9","level_9","gold_9","kill_9","death_9","assist_9","item1_9","item2_9","item3_9","item4_9","item5_9","item6_9","trinket_9","sbireskill_9","jungsbirekill_9",
                "champion_10","level_10","gold_10","kill_10","death_10","assist_10","item1_10","item2_10","item3_10","item4_10","item5_10","item6_10","trinket_10","sbireskill_10","jungsbirekill_10"]
        df = pd.DataFrame(columns=COLUMN_NAMES)

        for i in range (len(matchtimeline["frames"])):
            df.loc[i] = [0,i]+list([0]*171)


        df["match_ID"] = matchglobal["gameId"]

        if matchglobal["teams"][0]["win"] == "Win":
            who_win = "Blue"
        else :
            who_win = "Red"
        df["who_win"] = who_win

        for i in range (0,10,1):
            participantID = matchglobal["participants"][i]["participantId"]
            championID = matchglobal["participants"][i]["championId"]
            df[f"champion_{participantID}"] = f'{championID}'
        
        blueteam = [1,2,3,4,5]

        for frame in range(0,len(matchtimeline["frames"]),1):

            for participant in range(1,11,1):

                #Level and gold 

                participantID = matchtimeline["frames"][frame]['participantFrames'][f"{participant}"]["participantId"]
                df.loc[frame,f'{"level_" + str(participantID)}'] = matchtimeline["frames"][frame]['participantFrames'][f"{participantID}"]["level"]
                df.loc[frame,f'{"gold_" + str(participantID)}'] = matchtimeline["frames"][frame]['participantFrames'][f"{participantID}"]["totalGold"]
                df.loc[frame,f'{"sbireskill_" + str(participantID)}'] = matchtimeline["frames"][frame]['participantFrames'][f"{participantID}"]["minionsKilled"]
                df.loc[frame,f'{"jungsbirekill_" + str(participantID)}'] = matchtimeline["frames"][frame]['participantFrames'][f"{participantID}"]["jungleMinionsKilled"]

            #Team Gold

            blue_gold = df.loc[frame,'gold_1'] + df.loc[frame,'gold_2'] + df.loc[frame,'gold_3'] + df.loc[frame,'gold_4'] + df.loc[frame,'gold_5']
            red_gold =  df.loc[frame,'gold_6'] + df.loc[frame,'gold_7'] + df.loc[frame,'gold_8'] + df.loc[frame,'gold_9'] + df.loc[frame,'gold_10']
            
            df.loc[frame,'blue_gold'] = blue_gold
            df.loc[frame,'red_gold'] = red_gold

            for event in range(0,len(matchtimeline["frames"][frame]["events"]),1):
                
                # Kill Death Assist
                
                if matchtimeline["frames"][frame]["events"][event]["type"] == 'CHAMPION_KILL':
                    killer = str(matchtimeline["frames"][frame]["events"][event]["killerId"])
                    victim = str(matchtimeline["frames"][frame]["events"][event]["victimId"])
                    listasist = []

                    for asist in range(0,len(matchtimeline["frames"][frame]["events"][event]["assistingParticipantIds"]),1):
                        listasist.append(matchtimeline["frames"][frame]["events"][event]["assistingParticipantIds"][asist])
                    
                    if int(killer) !=0:
                        for i in range(frame,len(matchtimeline["frames"]),1) :
                            df.loc[i,f'{"kill_" + killer}'] = df.loc[frame,f'{"kill_" + killer}'] + 1    

                    for i in range(frame,len(matchtimeline["frames"]),1):
                        df.loc[i,f'{"death_" + victim}'] = df.loc[frame,f'{"death_" + victim}'] + 1

                    for helper in listasist : 
                        helper = str(helper)
                        for i in range(frame,len(matchtimeline["frames"]),1):
                            df.loc[i,f'{"assist_" + helper}'] = df.loc[frame,f'{"assist_" + helper}'] + 1
                
                # Building kill

                if matchtimeline["frames"][frame]["events"][event]["type"] == 'BUILDING_KILL':

                    if matchtimeline["frames"][frame]["events"][event]["killerId"] in blueteam:
                        for i in range(frame,len(matchtimeline["frames"]),1):
                            df.loc[i,"blue_destr_tower"] = df.loc[i,"blue_destr_tower"] + 1

                    else:
                        for i in range(frame,len(matchtimeline["frames"]),1):
                            df.loc[i,"red_destr_tower"] = df.loc[i,"red_destr_tower"] + 1

                if matchtimeline["frames"][frame]["events"][event]["type"] == 'ELITE_MONSTER_KILL':

                    # Herald

                    if matchtimeline["frames"][frame]["events"][event]["monsterType"] == 'RIFTHERALD' :

                        if matchtimeline["frames"][frame]["events"][event]["killerId"] in blueteam:
                            for i in range(frame,len(matchtimeline["frames"]),1):
                                df.loc[frame,"blue_kill_herald"] = df.loc[frame,"blue_kill_herald"] + 1

                        else:
                            for i in range(frame,len(matchtimeline["frames"]),1):
                                    df.loc[i,"red_kill_herald"] = df.loc[i,"red_kill_herald"] + 1

                    # Nashor

                    if matchtimeline["frames"][frame]["events"][event]["monsterType"] == 'NASHOR':

                        if matchtimeline["frames"][frame]["events"][event]["killerId"] in blueteam:
                            for i in range(frame,len(matchtimeline["frames"]),1):
                                    df.loc[i,"blue_kill_nashor"] = df.loc[i,"blue_kill_nashor"] + 1

                        else:
                            for i in range(frame,len(matchtimeline["frames"]),1):
                                    df.loc[i,"red_kill_nashor"] = df.loc[i,"red_kill_nashor"] + 1

                    # Drake      

                    if matchtimeline["frames"][frame]["events"][event]["monsterType"] == 'DRAGON' :
                        if matchtimeline["frames"][frame]["events"][event]["monsterSubType"] in ['WATER_DRAGON','EARTH_DRAGON','AIR_DRAGON','FIRE_DRAGON'] :
                            if matchtimeline["frames"][frame]["events"][event]["killerId"] in blueteam :

                                if df.loc[frame,"blue_kill_fire_drake"]+df.loc[frame,"blue_kill_water_drake"]+df.loc[frame,"blue_kill_air_drake"]+df.loc[frame,"blue_kill_earth_drake"] == 3:
                                    for i in range(frame,len(matchtimeline["frames"]),1):
                                        df.loc[i,'blue_soul_drake'] = matchtimeline["frames"][frame]["events"][event]["monsterSubType"]

                                else : 
                                    if matchtimeline["frames"][frame]["events"][event]["monsterSubType"] == "WATER_DRAGON":
                                        for i in range(frame,len(matchtimeline["frames"]),1):
                                            df.loc[i,"blue_kill_water_drake"] = df.loc[i,"blue_kill_water_drake"] + 1

                                    elif matchtimeline["frames"][frame]["events"][event]["monsterSubType"] == "EARTH_DRAGON":
                                        for i in range(frame,len(matchtimeline["frames"]),1):
                                            df.loc[i,"blue_kill_earth_drake"] = df.loc[i,"blue_kill_earth_drake"] + 1

                                    elif matchtimeline["frames"][frame]["events"][event]["monsterSubType"] == "AIR_DRAGON":
                                        for i in range(frame,len(matchtimeline["frames"]),1):
                                            df.loc[i,"blue_kill_air_drake"] = df.loc[i,"blue_kill_air_drake"] + 1

                                    else :
                                        for i in range(frame,len(matchtimeline["frames"]),1):
                                            df.loc[i,"blue_kill_fire_drake"] = df.loc[i,"blue_kill_fire_drake"] + 1


                            else :
                                if df.loc[frame,"red_kill_fire_drake"]+df.loc[frame,"red_kill_water_drake"]+df.loc[frame,"red_kill_air_drake"]+df.loc[frame,"red_kill_earth_drake"] == 3:
                                    for i in range(frame,len(matchtimeline["frames"]),1):
                                        df.loc[frame,'red_soul_drake'] = matchtimeline["frames"][frame]["events"][event]["monsterSubType"]
                                else : 
                                    if matchtimeline["frames"][frame]["events"][event]["monsterSubType"] == "WATER_DRAGON":
                                        for i in range(frame,len(matchtimeline["frames"]),1):
                                            df.loc[i,"red_kill_water_drake"] = df.loc[i,"red_kill_water_drake"] + 1

                                    elif matchtimeline["frames"][frame]["events"][event]["monsterSubType"] == "EARTH_DRAGON":
                                        for i in range(frame,len(matchtimeline["frames"]),1):
                                            df.loc[i,"red_kill_earth_drake"] = df.loc[i,"red_kill_earth_drake"] + 1

                                    elif matchtimeline["frames"][frame]["events"][event]["monsterSubType"] == "AIR_DRAGON":
                                        for i in range(frame,len(matchtimeline["frames"]),1):
                                            df.loc[i,"red_kill_air_drake"] = df.loc[i,"red_kill_air_drake"] + 1

                                    else :
                                        for i in range(frame,len(matchtimeline["frames"]),1):
                                            df.loc[i,"red_kill_fire_drake"] = df.loc[i,"red_kill_fire_drake"] + 1

                    #Elder Drake

                        if matchtimeline["frames"][frame]["events"][event]["monsterSubType"] == 'ELDER_DRAGON':
                            if matchtimeline["frames"][frame]["events"][event]["killerId"] in blueteam :
                                for i in range(frame,len(matchtimeline["frames"]),1):
                                    df.loc[i,'blue_kill_ancient_drake'] == matchtimeline["frames"][frame]["events"][event]["monsterSubType"]
                            else :
                                for i in range(frame,len(matchtimeline["frames"]),1):
                                    df.loc[i,'red_kill_ancient_drake'] == matchtimeline["frames"][frame]["events"][event]["monsterSubType"]

                # Trinket buy

                if matchtimeline["frames"][frame]["events"][event]["type"] == 'ITEM_PURCHASED'and matchtimeline["frames"][frame]["events"][event]["itemId"] in [3340,3363,3364,3330] :
                    participantID = matchtimeline["frames"][frame]["events"][event]["participantId"]
                    for i in range(frame,len(matchtimeline["frames"]),1):
                        df.loc[i,f'{"trinket_" + str(participantID)}'] = matchtimeline["frames"][frame]["events"][event]["itemId"]
                
                # Item buy

                if matchtimeline["frames"][frame]["events"][event]["type"] == 'ITEM_PURCHASED' and matchtimeline["frames"][frame]["events"][event]["itemId"] not in [3340,3363,3364,3330,2010] :
                    participantID = matchtimeline["frames"][frame]["events"][event]["participantId"]
                    

                    # Remove used item
                    try:
                        if matchtimeline["frames"][frame +1]["events"][event]["type"] in ["ITEM_DESTROYED"] and matchtimeline["frames"][frame +1]["events"][event]["timestamp"] == matchtimeline["frames"][frame]["events"][event]["timestamp"] :
                            for i in range(1,6,1):
                                if df.loc[frame,f'{"item" + str(i)+ "_" + str(participantID)}'] == matchtimeline["frames"][frame]["events"][event]["itemId"]:
                                    find_item_slot = i
                                    for i in range(frame,len(matchtimeline["frames"]),1):
                                        df.loc[i,f'{"item" + str(find_item_slot)+ "_" + str(participantID)}'] = 0
                            
                            try:
                                if matchtimeline["frames"][frame +2]["events"][event]["type"] in ["ITEM_DESTROYED"] and matchtimeline["frames"][frame +1]["events"][event]["timestamp"] == matchtimeline["frames"][frame]["events"][event]["timestamp"] :
                                    for i in range(1,6,1):
                                        if df.loc[frame,f'{"item" + str(i)+ "_" + str(participantID)}'] == matchtimeline["frames"][frame]["events"][event]["itemId"]:
                                            find_item_slot = i
                                            for i in range(frame,len(matchtimeline["frames"]),1):
                                                df.loc[i,f'{"item" + str(find_item_slot)+ "_" + str(participantID)}'] = 0
                                    
                                    try:
                                        if matchtimeline["frames"][frame +2]["events"][event]["type"] in ["ITEM_DESTROYED"] and matchtimeline["frames"][frame +1]["events"][event]["timestamp"] == matchtimeline["frames"][frame]["events"][event]["timestamp"] :
                                            for i in range(1,6,1):
                                                if df.loc[frame,f'{"item" + str(i)+ "_" + str(participantID)}'] == matchtimeline["frames"][frame]["events"][event]["itemId"]:
                                                    find_item_slot = i
                                                    for i in range(frame,len(matchtimeline["frames"]),1):
                                                        df.loc[i,f'{"item" + str(find_item_slot)+ "_" + str(participantID)}'] = 0

                                    except: 
                                        pass
                            except:
                                pass
                    except:
                        pass

                    # Find enpty slot
                    empty_item_slot = 1
                    if not df.loc[frame][f'{"item1_" + str(participantID) }'] == 0:
                        empty_item_slot = 2
                        if not df.loc[frame][f'{"item2_" + str(participantID) }'] == 0:
                            empty_item_slot = 3
                            if not df.loc[frame][f'{"item3_" + str(participantID) }'] == 0:
                                empty_item_slot = 4
                                if not df.loc[frame][f'{"item4_" + str(participantID) }'] == 0:
                                    empty_item_slot = 5
                                    if not df.loc[frame][f'{"item5_" + str(participantID) }'] == 0:
                                        empty_item_slot = 6
                                        
                    for i in range(frame,len(matchtimeline["frames"]),1):
                        df.loc[i,f'{"item" + str(empty_item_slot)+ "_" + str(participantID)}'] = matchtimeline["frames"][frame]["events"][event]["itemId"]

                # Item Delete

                if matchtimeline["frames"][frame]["events"][event]["type"] in ["ITEM_DESTROYED"] and matchtimeline["frames"][frame]["events"][event]["participantId"] != 0  :
                    participantID = matchtimeline["frames"][frame]["events"][event]["participantId"]
                    for i in range(1,6,1):
                        if df.loc[frame,f'{"item" + str(i)+ "_" + str(participantID)}'] == matchtimeline["frames"][frame]["events"][event]["itemId"]:
                            find_item_slot = i
                            for i in range(frame,len(matchtimeline["frames"]),1):
                                df.loc[i,f'{"item" + str(find_item_slot)+ "_" + str(participantID)}'] = 0

                if matchtimeline["frames"][frame]["events"][event]["type"] in ["ITEM_UNDO"]:
                    participantID = matchtimeline["frames"][frame]["events"][event]["participantId"]
                    for i in range(1,6,1):
                        if df.loc[frame,f'{"item" + str(i)+ "_" + str(participantID)}'] == matchtimeline["frames"][frame]["events"][event]["beforeId"]:
                            find_item_slot = i
                            df.loc[frame,f'{"item" + str(find_item_slot)+ "_" + str(participantID)}'] = matchtimeline["frames"][frame]["events"][event]["afterId"]


        df.to_csv(f"./data/02transform_data/select_data_match/{matchid}.csv")
        stop = timeit.default_timer()

    except Exception as e:
        print("Match",matchid, "non conforme")
        print (e)
        
stop = timeit.default_timer()

print('Time: ', stop - start) 