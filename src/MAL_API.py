import requests
import json

BASE_URL = "https://api.myanimelist.net/v2"


class ExpiredTokenError(Exception):
    pass


class UnrefreshableTokenError(Exception):
    pass


class Token:
    def __init__(self, path_to_token):
        self.access_token = None
        self.refresh_token = None
        self.path = path_to_token
        self.load_token()

    def load_token(self):
        """
        Load the tokens from the file specified at initialisation and store them in correct fields
        Returns:
        """
        token_set = json.load(open(self.path, "r"))
        self.access_token = token_set['access_token']
        self.refresh_token = token_set['refresh_token']

    def refresh_access_token(self):
        """
        Refresh expired access token by requesting a new access and refresh token
        Returns:
        """
        with open("D:/Informatyka/MalDB/.secrets/client_id") as f:
            client_id = f.readline()

        url = 'https://myanimelist.net/v1/oauth2/token'
        data = {
            'client_id': client_id,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        response = requests.post(url, data)
        response.raise_for_status()  # Check whether the requests contains errors
        token_set = response.json()
        response.close()

        with open(self.path, 'w') as file:
            json.dump(token_set, file, indent=4)

        self.access_token = token_set['access_token']
        self.refresh_token = token_set['refresh_token']


def anime_details(token: str, anime_id: int, fields: list[str]) -> dict:
    """
    Args:
        token: Authorization token of the user
        anime_id: Id of the anime
        *fields: Specifies what details are to be returned

    Returns: Dictionary with specified fields as keys

    Possible fields:
        id,
        title,
        main_picture,
        alternative_titles,
        start_date,
        end_date,
        synopsis,
        mean,
        rank,
        popularity,
        num_list_users,
        num_scoring_users,
        nsfw,
        created_at,
        updated_at,
        media_type,
        status,
        genres,
        my_list_status,
        list_status,
        num_episodes,
        start_season,
        broadcast,
        source,
        average_episode_duration,
        rating,
        pictures,
        background,
        related_anime,
        related_manga,
        recommendations,
        studios,
        statistics
    """
    url = BASE_URL + f"/anime/{anime_id}?fields={','.join(fields)}"
    response = requests.get(url, headers={
        'Authorization': f'Bearer {token}'
    })

    try:
        response.raise_for_status()
        anime = response.json()
        response.close()
    except requests.exceptions.HTTPError as e:
        print(anime_id, ": ", str(e))
        if '401' in str(e)[:3]:
            raise ExpiredTokenError
        anime = {'id': None, 'title': 'Missing'}
        anime.update({field: None for field in fields})

    return anime


def request_anime(token: str, status: list[str], sort: str, detailed: bool = True) -> list:
    """
    Args:
        token: Authorization token of the user
        detailed: Should the anime be returned with basic information from users list
        status: A list consisting of elements: watching, completed, on_hold, dropped, plan_to_watch
        sort: list_score, list_updated_at, anime_title, anime_start_date, anime_id

    Returns: List with all of the specified anime
    """
    url = BASE_URL + '/users/@me/animelist'

    anime_list = []

    for element in status:
        parameters = {
            'status': element,
            'sort': sort,
            'limit': 100,
            'offset': 0,
        }

        if detailed:
            parameters['fields'] = 'list_status'

        response = requests.get(url, parameters, headers={
            'Authorization': f'Bearer {token}'
        })

        try:
            response.raise_for_status()
            user = response.json()
            response.close()
            anime_list.extend(user['data'])
        except requests.HTTPError as e:
            if '401' in str(e)[:3]:
                raise ExpiredTokenError
            else:
                raise RuntimeError(f"Unexpected HTTPS error {e}")

        while user['paging'].get('next'):
            url = user['paging'].get('next')
            response = requests.get(url, headers={
                'Authorization': f'Bearer {token}'
            })

            try:
                response.raise_for_status()
                user = response.json()
                response.close()
                anime_list.extend(user['data'])
            except requests.HTTPError as e:
                if '401' in str(e)[:3]:
                    raise ExpiredTokenError
                else:
                    raise RuntimeError(f"Unexpected HTTPS error {e}")

    return anime_list


def get_my_anime(token: Token, status: list[str], sort: str, detailed: bool = True) -> list:
    """
    Read all the specified anime from users list and refresh token if expired
    If it cannot be refreshed within 5 tries raise UnrefreshableTokenError
    Args:
        token: Token object of the user
        detailed: Should the anime be returned with basic information from users list
        status: A list consisting of elements: watching, completed, on_hold, dropped, plan_to_watch
        sort: list_score, list_updated_at, anime_title, anime_start_date, anime_id

    Returns: List with all of the specified anime
    """
    for attempt in range(5):
        try:
            my_anime = request_anime(token.access_token, status, sort, detailed)
        except ExpiredTokenError:
            token.refresh_access_token()
            continue
        break
    else:
        raise UnrefreshableTokenError
    return my_anime
