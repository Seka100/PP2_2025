def get_average_imdb(movies):
    if not movies:
        return 0
    total = sum(movie['imdb'] for movie in movies)
    return total / len(movies)

