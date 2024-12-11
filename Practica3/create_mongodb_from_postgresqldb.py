from pprint import pprint
from pymongo import MongoClient
from sqlalchemy import create_engine, text

client = MongoClient('localhost', 27017)

db = client['practica3']

# Connect to PostgreSQL
engine = create_engine('postgresql://alumnodb:1234@localhost/si1')

# Define the query
query = text("""
WITH peliculas_base AS (
    SELECT 
        m.movieid AS pelicula_id,
        REGEXP_REPLACE(m.movietitle, '\(\d{4}\)$', '') AS titulo_sin_anio, -- Elimina el año del título
        m.year AS anio,
        ARRAY_AGG(distinct a.actorname) as actors,
        ARRAY_AGG(DISTINCT g.genre) AS generos, -- Listado de géneros
        ARRAY_AGG(DISTINCT d.directorname) AS directores -- Listado de directores
    FROM 
        imdb_movies m
    LEFT JOIN imdb_moviegenres g ON m.movieid = g.movieid -- Relación con géneros
    LEFT JOIN imdb_directormovies dm ON m.movieid = dm.movieid -- Relación con los directores
    LEFT JOIN imdb_directors d ON dm.directorid = d.directorid
    LEFT JOIN imdb_actormovies actm on m.movieid = actm.movieid
    left join imdb_actors a on actm.actorid = a.actorid
    LEFT JOIN imdb_moviecountries mc ON m.movieid = mc.movieid -- Relación con países
    WHERE mc.country = 'France' -- Filtramos solo películas francesas
    GROUP BY m.movieid, m.movietitle, m.year
),
peliculas_relacionadas AS (
    SELECT 
        p1.pelicula_id AS id_original,
        p2.pelicula_id AS id_relacionada,
        p2.titulo_sin_anio AS titulo_relacionado,
        p2.anio AS anio_relacionado,
        (SELECT COUNT(*) FROM UNNEST(p1.generos) g1 WHERE g1 = ANY(p2.generos)) AS coincidencias,
        ARRAY_LENGTH(p1.generos, 1) AS total_generos
    FROM 
        peliculas_base p1
    JOIN peliculas_base p2 ON p1.pelicula_id != p2.pelicula_id -- No relacionarse consigo misma
),
relaciones_clasificadas AS (
    SELECT 
        id_original,
        titulo_relacionado,
        anio_relacionado,
        coincidencias,
        total_generos,
        CASE 
            WHEN coincidencias = total_generos THEN 'relacionadas_100'
            WHEN coincidencias >= total_generos / 2 THEN 'relacionadas_50'
        END AS tipo_relacion
    FROM peliculas_relacionadas
),
relaciones_limitadas AS (
    SELECT 
        id_original,
        tipo_relacion,
        ARRAY_AGG(titulo_relacionado || ' (' || anio_relacionado || ')') AS peliculas_relacionadas
    FROM (
        SELECT 
            rc.id_original,
            rc.tipo_relacion,
            rc.titulo_relacionado,
            rc.anio_relacionado,
            ROW_NUMBER() OVER (PARTITION BY rc.id_original, rc.tipo_relacion ORDER BY rc.anio_relacionado DESC) AS fila
        FROM relaciones_clasificadas rc
    ) subquery
    WHERE fila <= 10 -- Limitamos a las 10 más recientes por categoría
    GROUP BY id_original, tipo_relacion
)
SELECT 
    pb.titulo_sin_anio AS titulo,
    pb.generos AS generos,
    pb.anio AS anio,
    pb.directores AS directores,
    pb.actors as actors,
    rl_100.peliculas_relacionadas AS relacionadas_100,
    rl_50.peliculas_relacionadas AS relacionadas_50
FROM 
    peliculas_base pb
LEFT JOIN relaciones_limitadas rl_100 
    ON pb.pelicula_id = rl_100.id_original AND rl_100.tipo_relacion = 'relacionadas_100'
LEFT JOIN relaciones_limitadas rl_50 
    ON pb.pelicula_id = rl_50.id_original AND rl_50.tipo_relacion = 'relacionadas_50';

""")

# Execute the query and fetch all results
with engine.connect() as connection:
    result = connection.execute(query)
    documents = []
    count = 0
    for row in result:
        document = {
            'title': row[0],
            'genres': row[1],
            'year': row[2],
            'directors': row[3],
            'actors': row[4] if row[4] is not None else [],
            'most_related_movies': row[5] if row[5] is not None else [],
            'related_movies': row[6] if row[6] is not None else []
        }
        documents.append(document)
        print(count)
        count += 1

# Insert documents into MongoDB
collection = db['france']
collection.insert_many(documents)
