from pymongo import MongoClient
import pandas as pd

# Conexión a la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['practica3']
collection = db['france']


# Consulta a: Películas de ciencia ficción entre 1994 y 1998
query_a = {
    'genres': {'$in': ['Sci-Fi']},
    'year': {'$gte': '1994', '$lte': '1998'}
}
result_a = list(collection.find(query_a))
df_a = pd.DataFrame(result_a)

print("Consulta A: Películas de ciencia ficción entre 1994 y 1998\n")
for index, row in df_a.iterrows():
    
    title = f"| title:               |  {row.get('title', 'N/A')}"
    genres = f"| genres:              |  {', '.join(row.get('genres', []))}"
    year = f"| year:                |  {row.get('year', 'N/A')}"
    actors = f"| actors:              |  {', '.join(row.get('actors', []))}"
    directors = f"| directors:           |  {', '.join(row.get('directors', []))}"
    related_movies = f"| related_movies:      |  {', '.join(row.get('related_movies', [])) if 'related_movies' in row else 'N/A'}"
    most_related_movies = f"| most_related_movies: |  {', '.join(row.get('most_related_movies', [])) if 'most_related_movies' in row else 'N/A'}"
    max_length = max(len(title), len(genres), len(year), len(actors), len(directors), len(related_movies), len(most_related_movies))
    separator = f"{'='*(max_length+1)}\n"

    title += ' '*(max_length-len(title)) + '|' + '\n'
    genres += ' '*(max_length-len(genres)) + '|' + '\n'
    year += ' '*(max_length-len(year)) + '|' + '\n'
    actors += ' '*(max_length-len(actors)) + '|' + '\n'
    directors += ' '*(max_length-len(directors)) + '|' + '\n'
    related_movies += ' '*(max_length-len(related_movies)) + '|' + '\n'
    most_related_movies += ' '*(max_length-len(most_related_movies)) + '|' + '\n'

    print(separator, end='')
    print(title, end='')
    print(genres, end='')
    print(year, end='')
    print(actors, end='')
    print(directors, end='')
    print(related_movies, end='')
    print(most_related_movies, end='')
    print(separator, end='')
    print("")

print("\n\n\n")

# Consulta b: Películas de drama del año 1998 que empiecen por "The"
query_b = {
    'genres': {'$in': ['Drama']},
    'year': '1998',
    'title': {'$regex': ', The'}
}
result_b = list(collection.find(query_b))
df_b = pd.DataFrame(result_b)
print("\nConsulta B: Películas de drama del año 1998 que empiecen por 'The'\n")
for index, row in df_b.iterrows():
    
    title = f"| title:               |  {row.get('title', 'N/A')}"
    genres = f"| genres:              |  {', '.join(row.get('genres', []))}"
    year = f"| year:                |  {row.get('year', 'N/A')}"
    actors = f"| actors:              |  {', '.join(row.get('actors', []))}"
    directors = f"| directors:           |  {', '.join(row.get('directors', []))}"
    related_movies = f"| related_movies:      |  {', '.join(row.get('related_movies', [])) if 'related_movies' in row else 'N/A'}"
    most_related_movies = f"| most_related_movies: |  {', '.join(row.get('most_related_movies', [])) if 'most_related_movies' in row else 'N/A'}"
    max_length = max(len(title), len(genres), len(year), len(actors), len(directors), len(related_movies), len(most_related_movies))
    separator = f"{'='*(max_length+1)}\n"

    title += ' '*(max_length-len(title)) + ' |' + '\n'
    genres += ' '*(max_length-len(genres)) + ' |' + '\n'
    year += ' '*(max_length-len(year)) + ' |' + '\n'
    actors += ' '*(max_length-len(actors)) + ' |' + '\n'
    directors += ' '*(max_length-len(directors)) + ' |' + '\n'
    related_movies += ' '*(max_length-len(related_movies)) + ' |' + '\n'
    most_related_movies += ' '*(max_length-len(most_related_movies)) + ' |' + '\n'

    print(separator, end='')
    print(title, end='')
    print(genres, end='')
    print(year, end='')
    print(actors, end='')
    print(directors, end='')
    print(related_movies, end='')
    print(most_related_movies, end='')
    print(separator, end='')
    print("")

print("\n\n\n")

# Consulta c: Películas en las que Faye Dunaway y Viggo Mortensen hayan compartido reparto
query_c = {
    'actors': {'$all': ['Dunaway, Faye', 'Mortensen, Viggo']}
}
result_c = list(collection.find(query_c))
df_c = pd.DataFrame(result_c)
print("\nConsulta C: Películas en las que Faye Dunaway y Viggo Mortensen hayan compartido reparto\n")
for index, row in df_c.iterrows():
    
    title = f"| title:               |  {row.get('title', 'N/A')}"
    genres = f"| genres:              |  {', '.join(row.get('genres', []))}"
    year = f"| year:                |  {row.get('year', 'N/A')}"
    actors = f"| actors:              |  {', '.join(row.get('actors', []))}"
    directors = f"| directors:           |  {', '.join(row.get('directors', []))}"
    related_movies = f"| related_movies:      |  {', '.join(row.get('related_movies', [])) if 'related_movies' in row else 'N/A'}"
    most_related_movies = f"| most_related_movies: |  {', '.join(row.get('most_related_movies', [])) if 'most_related_movies' in row else 'N/A'}"
    max_length = max(len(title), len(genres), len(year), len(actors), len(directors), len(related_movies), len(most_related_movies))
    separator = f"{'='*(max_length+1)}\n"

    title += ' '*(max_length-len(title)) + '|' + '\n'
    genres += ' '*(max_length-len(genres)) + '|' + '\n'
    year += ' '*(max_length-len(year)) + '|' + '\n'
    actors += ' '*(max_length-len(actors)) + '|' + '\n'
    directors += ' '*(max_length-len(directors)) + '|' + '\n'
    related_movies += ' '*(max_length-len(related_movies)) + '|' + '\n'
    most_related_movies += ' '*(max_length-len(most_related_movies)) + '|' + '\n'

    print(separator, end='')
    print(title, end='')
    print(genres, end='')
    print(year, end='')
    print(actors, end='')
    print(directors, end='')
    print(related_movies, end='')
    print(most_related_movies, end='')
    print(separator, end='')
    print("")

print("\n\n\n")