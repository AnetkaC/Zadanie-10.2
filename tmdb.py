import requests
import random
import os
API_TOKEN = os.environ.get("TMDB_API_TOKEN", "")

def call_tmdb_api(endpoint):
   full_url = f"https://api.themoviedb.org/3/{endpoint}"
   headers = {
       "Authorization": f"Bearer {API_TOKEN}"
   }
   response = requests.get(full_url, headers=headers)
   response.raise_for_status()
   return response.json()

def get_poster_url(poster_api_path, size="w342"): # str 24 materiałów
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}{poster_api_path}"


def get_movies_list(list_type):
   return call_tmdb_api(f"movie/{list_type}")


def get_movies(list_type, how_many):
    data = get_movies_list(list_type)
    return random.sample(data["results"], how_many)


def get_single_movie(movie_id):
    return call_tmdb_api(f"movie/{movie_id}")


def get_single_movie_cast(movie_id):
    return call_tmdb_api(f"movie/{movie_id}/credits")["cast"]


def get_movie_images(movie_id):
    return call_tmdb_api(f"movie/{movie_id}/images")


def search(search_query):
    base_url = "https://api.themoviedb.org/3/"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    endpoint = f"{base_url}search/movie/?query={search_query}"

    response = requests.get(endpoint, headers=headers)
    response = response.json()
    return response['results']


def get_airing_today():
    endpoint = "https://api.themoviedb.org/3/tv/airing_today"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    response = response.json()
    return response['results']