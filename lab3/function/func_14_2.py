def is_high_rated(movie):
    return movie['imdb'] > 5.5

def get_high_rated_movies(movies):
    return [m for m in movies if m['imdb'] > 5.5]

def get_movies_by_category(movies, category):
    return [m for m in movies if m['category'].lower() == category.lower()]

def get_average_imdb(movies):
    if not movies:
        return 0
    return sum(m['imdb'] for m in movies) / len(movies)

def get_average_imdb_by_category(movies, category):
    filtered = [m for m in movies if m['category'].lower() == category.lower()]
    return get_average_imdb(filtered)
