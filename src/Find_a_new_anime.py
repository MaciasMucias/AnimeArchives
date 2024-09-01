from MAL_API import *
import random
import pandas as pd
from slugify import slugify


def main():
    token = Token('../Tokens/MaciekToken.json')

    anime_selection = get_my_anime(token, ['plan_to_watch'], 'anime_title')
    anime_status_list = []
    for anime in anime_selection:
        anime_with_status = anime_details(token.access_token, anime['node']['id'], ['status', 'alternative_titles'])
        if anime_with_status['status'] == 'not_yet_aired':
            continue
        anime_with_status.pop('main_picture')
        anime_status_list.append(anime_with_status)

    if not anime_status_list:
        print("Musisz poszukać nowych anime")
    else:
        anime_to_watch = random.choice(anime_status_list)
        print(anime_to_watch['title'])
        print(f"https://kissanimefree.cc/watch-anime/{slugify(anime_to_watch['title'], to_lower=True)}/eps/001")


if __name__ == '__main__':
    main()
