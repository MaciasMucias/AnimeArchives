import datetime
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    all_files = dict()

    for directory in pathlib.Path('D:\Informatyka\MalDB\WeabooArchives').iterdir():
        user_files = []

        # read all of the csv files and put them into user files in a form of a tuple consisting of (date, anime_data)
        for file in directory.iterdir():
            user_files.append((datetime.datetime.strptime(str(file)[-14:-4], '%Y-%m-%d').date(), pd.read_csv(file, index_col=0)))

        daily_changes = []

        # if there was less than 2 files then analyzing data is impossible, so just go to the next user
        if len(user_files) < 2:
            continue

        for ind, val in enumerate(user_files[1:]):
            # calculate the difference between this and previous entry
            difference = val[1]['episodes_watched'] - user_files[ind][1]['episodes_watched']
            anime_delta = difference[difference != 0]

            # split the result between continued anime (we get a numerical value as a result) and new anime (we get NaN as a result)
            continued_anime = anime_delta[~anime_delta.isnull()]
            new_anime = anime_delta[anime_delta.isnull()]

            # if its new then all of the episodes already watched are also new
            new_anime = val[1].loc[new_anime.index]['episodes_watched']

            new_episodes = new_anime.append(continued_anime)

            # check how many days have passed since last entry and split all of the new episodes between them
            days_passed = (val[0] - user_files[ind][0]).days

            # append a tuple (date_of_watching, episodes_watched)
            for i in range(days_passed):
                daily_changes.append((user_files[ind][0] + datetime.timedelta(days=i), new_episodes/days_passed))

        dates, episodes_watched = zip(*daily_changes)
        number_of_episodes_watched = list(map(lambda x: x.sum(), episodes_watched))

        plt.bar(dates, number_of_episodes_watched)
        plt.xticks(dates, rotation=90)
        plt.tick_params(axis="both", direction="in", pad=15)
        plt.tight_layout()
        plt.show()

        all_files[str(directory)[15:]] = (user_files[-1], daily_changes)
    print()


if __name__ == '__main__':
    main()
