def get_average_imdb_by_category(movies, category):
    filtered = get_movies_by_category(movies, category)
    return get_average_imdb(filtered)


