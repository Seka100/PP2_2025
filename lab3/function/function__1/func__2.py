def get_high_rated_movies(movies):
    return [movie for movie in movies if movie['imdb'] > 5.5]

