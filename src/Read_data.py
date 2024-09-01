# In BIOS I've set auto boot for 4AM
# This script is set to be launched at 4:15AM


import json
import time
import psutil
import datetime
import pathlib
import os
import traceback
import pandas as pd
from MAL_API import *
print("STARTING MAL ANALYSIS")
try:
    # for every token in the tokens folder
    for path in pathlib.Path(r"D:\Informatyka\MalDB\Tokens").iterdir():
        token = Token(path)
        # get the anime from user profile or log that it failed
        try:
            my_anime = get_my_anime(token, ['watching', 'completed', 'on_hold'], 'list_updated_at')
        except UnrefreshableTokenError:
            with open(r"D:\Informatyka\MalDB\Error.log", "a") as log:
                log.write(str(datetime.date.today()) + '\n')
                log.write(f"{path.stem} could not be \n\n")
            continue

        # if it succeeded then parse it into a pandas DataFrame and save to a .csv file
        rows_list = [{'id': anime['node']['id'],
                      'name': anime['node']['title'],
                      'episodes_watched': anime['list_status']['num_episodes_watched'],
                      'score': anime['list_status']['score']} for anime in my_anime]

        df = pd.DataFrame(rows_list).set_index('id')
        save_path = rf"D:\Informatyka\MalDB\WeabooArchives\{path.stem[:-5]}"
        if not pathlib.Path(save_path).is_dir():
            os.mkdir(save_path)
        df.to_csv(save_path + "/" + str(datetime.date.today()) + ".csv")


# if any exception occurs log it to the error file
except Exception:
    with open(r"D:\Informatyka\MalDB\Error.log", "a") as log:
        log.write(str(datetime.date.today()) + '\n')
        traceback.print_exc()
        traceback.print_exc(file=log)
        log.write("\n\n")

