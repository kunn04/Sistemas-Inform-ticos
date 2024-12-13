import time

from neo4j import GraphDatabase
import sqlalchemy as sa

class SQL:
    
    def __init__(self, drivername="postgresql", username="alumnodb", password="1234", host="127.0.0.1", port="5432", database="si1"):
        connection_url = f"{drivername}://{username}:{password}@{host}:{port}/{database}"
        self.db_engine = sa.create_engine(connection_url, echo=False)
    

    def _connect(self):
        """Conectando a la base de datos."""
        self.db_conn = self.db_engine.connect()
    
    def _disconnect(self):
        """Desconectando de la base de datos."""
        self.db_conn.close()


    def _apply_select(self, query, params=None):
        """Ejecutar una consulta SELECT en la base de datos."""
        if params:
            return list(self.db_conn.execute(sa.text(query), params))
        return list(self.db_conn.execute(sa.text(query)))
    
class EtlFromPostgresToNeo4j:
    """Clase para transformar datos relacionales de películas a una base de datos de grafos"""

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.delete_all_nodes()
        self.create_all_constraints()
        self.sql = SQL()

    def transform_postgres_to_neo4j(self):
        """
        Transformar la base de datos relacional de películas a una base de datos de grafos
        """
        # Obtener todos los datos de PostgreSQL y obtener las 20 películas más vendidas de EE.UU.
        db_result = self.best_selling_movies_usa()
        print("Procesando filas de la base de datos ...")
        start_time = time.time()
        for row_movie in db_result:
            dict_movie = row_movie._asdict()
            print("....................")
            print(dict_movie)
            # Insertar película en GraphDB
            node_movie = self.create_and_return_movie(dict_movie)
            # Insertar todos los actores
            self.insert_all_actors(dict_movie, node_movie)
            # Insertar todos los directores
            self.insert_all_directors(dict_movie, node_movie)

        print("Fin del proceso ETL...")
        f_string_order = f"Proceso terminado ... {time.time() - start_time} segundos ..."
        print(f_string_order)
    
    def insert_all_actors(self, dict_movie, node_movie):
        """Insertar todos los actores que participaron en la película"""
        db_actors = []
        
        self.sql._connect()

        query = """
            SELECT
                        ima.actorid,
                        ima.actorname
                    FROM
                        imdb_actormovies imam
                    JOIN imdb_actors ima ON imam.actorid = ima.actorid
                    WHERE imam.movieid = :movieid;
        """
        
        try:
            movie_id = dict_movie.get('movieid')
            if not movie_id:
                print("Error: movieid no está definido o no es váslido.")
                return

            db_actors = self.sql._apply_select(query, {'movieid': movie_id})

            if not db_actors:
                print("No se encontraron actores para esta película.")
                return

        except Exception as e:
            print(f"Error ejecutando la consulta: {e}")
            return

        for row_actor in db_actors:
            dict_actor = row_actor._asdict()
            print("....................")
            print(dict_actor)
            self.create_and_return_actor(dict_actor, node_movie)

        self.sql._disconnect()

    

    def insert_all_directors(self, dict_movie, node_movie):
        """Insertar los directores que dirigieron la película"""
        db_directors = []

        self.sql._connect()

        query = """
            SELECT
                        imd.directorid,
                        imd.directorname
                    FROM
                        imdb_directormovies imdm
                    JOIN imdb_directors imd ON imdm.directorid = imd.directorid
                    WHERE imdm.movieid = :movieid;
        """

        try:
            movie_id = dict_movie.get('movieid')
            if not movie_id:
                print("Error: movieid no está definido o es inválido.")
                return
            db_directors = self.sql._apply_select(query, {'movieid': movie_id})

            if not db_directors:
                print("No se encontraron directores para esta película.")
                return
            
        except Exception as e:
            print(f"Error ejecutando la consulta: {e}")
            return
        finally:
            self.sql._disconnect()
        
        for row_director in db_directors:
            dict_director = row_director._asdict()
            self.create_and_return_director(dict_director, node_movie)

    def create_and_return_director(self, dict_director, node_movie):
        """ Crear nodo Persona Director"""
        with self.driver.session() as session:
            node_director = session.execute_write(self._create_and_return_director, dict_director)
            session.execute_write(self._create_and_return_directed, node_movie, node_director)
            return node_director

    def create_and_return_actor(self, dict_actor, node_movie):
        """ Crear nodo Actor """
        with self.driver.session() as session:
            node_actor = session.execute_write(self._create_and_return_actor, dict_actor)
            session.execute_write(self._create_and_return_acted_in, node_movie, node_actor)
            return node_actor
    
    def create_and_return_movie(self, dict_movie: dict):
        """ Crear nodo Película """
        with self.driver.session() as session:
            movie = session.execute_write(self._create_and_return_movie, dict_movie)
            return movie

    def delete_all_nodes(self):
        """Eliminar todos los nodos de la base de datos"""
        with self.driver.session() as session:
            session.execute_write(self._delete_all_nodes)

    def create_all_constraints(self):
        """ Crear restricciones y índices """
        with self.driver.session() as session:
            session.run(
            "CREATE CONSTRAINT actor_id_unique IF NOT EXISTS FOR (a:Actor) REQUIRE a.actorid IS UNIQUE"
            )
            session.run(
            "CREATE CONSTRAINT director_id_unique IF NOT EXISTS FOR (d:Director) REQUIRE d.directorid IS UNIQUE"
            )
            
            session.run(
            "CREATE CONSTRAINT movie_id_unique IF NOT EXISTS FOR (m:Movie) REQUIRE m.movieid IS UNIQUE"
            )
            
            session.run(
                "CREATE INDEX actor_id IF NOT EXISTS FOR (a:Actor) ON (a.actorid)")

        
            session.run(
            "CREATE INDEX director_id IF NOT EXISTS FOR (d:Director) ON (d.directorid)"
            )
            
            session.run(
            "CREATE INDEX movie_id IF NOT EXISTS FOR (m:Movie) ON (m.movieid)"
            )
            
          
    @staticmethod
    def _create_and_return_directed(tx, node_movie, node_director):
        
        query = """
            MATCH (m:Movie {movieid: $movieid})
            MATCH (d:Director {directorid: $directorid})
            CREATE (d)-[:DIRECTED]->(m)
            RETURN d, m"""

        movieid = node_movie["m"]["movieid"]
        directorid = node_director["d"]["directorid"]
        result = tx.run(query, movieid=movieid, directorid=directorid)
        print(f"Relación DIRECTED creada entre {node_director['d']['name']} y {node_movie['m']['movietitle']}")
     
        return result.single()
   
    @staticmethod
    def _create_and_return_acted_in(tx, node_movie, node_actor):
        query = """
            MATCH (m:Movie {movieid: $movieid})
            MATCH (a:Actor {actorid: $actorid})
            CREATE (a)-[:ACTED_IN]->(m)
            RETURN a, m
        """
        
        movieid = node_movie["m"]["movieid"]
        actorid = node_actor["a"]["actorid"]
        
       
        result = tx.run(query, movieid=movieid, actorid=actorid)
        print(f"Relación ACTED_IN creada entre {node_actor['a']['name']} y {node_movie['m']['movietitle']}")
        return result.single()

    @staticmethod
    def _create_and_return_actor(tx, dict_actor):
        
        query = """
        MERGE (a:Actor {actorid: $actorid})
        ON CREATE SET a.name = $actorname
        RETURN a
        """

        result = tx.run(query, actorid=dict_actor['actorid'], actorname=dict_actor['actorname'])
        return result.single()

    @staticmethod
    def _create_and_return_director(tx, dict_director):
        
        query = """
        MERGE (d:Director {directorid: $directorid})
        ON CREATE SET d.name = $directorname
        RETURN d
        """
        
        result = tx.run(query, directorid=dict_director['directorid'], directorname=dict_director['directorname'])
        return result.single()

    @staticmethod
    def _create_and_return_movie(tx, movietitle: dict):
        query = """
                CREATE (m:Movie { 
                    movietitle: $title, 
                    movieid: $movieid
                })
                RETURN m
                """
        result = tx.run(query, title=movietitle['title'], movieid=movietitle['movieid'])
    
        return result.single()

    @staticmethod
    def _delete_all_nodes(tx):
        tx.run("MATCH (n) DETACH DELETE n")

    def best_selling_movies_usa(self):
        """Método que ejecuta la consulta en la base de datos para obtener las 20 películas más vendidas de EE.UU."""

        result = None

        self.sql._connect()

        query = """SELECT 
                        m.movietitle AS title,
                        m.year,
                        m.movieid,
                        SUM(i.sales) AS total_sales
                    FROM 
                        imdb_movies m
                    JOIN 
                        imdb_moviecountries mc ON m.movieid = mc.movieid
                    JOIN 
                        products p ON m.movieid = p.movieid
                    JOIN 
                        inventory i ON p.prod_id = i.prod_id
                    WHERE 
                        mc.country = 'USA'  
                    GROUP BY 
                        m.movieid, m.movietitle, m.year
                    ORDER BY 
                        total_sales DESC
                    LIMIT 20"""
        
        try:
            result = self.sql._apply_select(query)

            if not result:
                print("No se encontraron resultados.")
                return None
            return result
        except Exception as e:
            print(f"Error ejecutando la consulta: {e}")
            return None
        finally:
            self.sql._disconnect()

    def close(self):
        """
        Cerrar la conexión del driver
        """
        self.driver.close()


if __name__ == "__main__":
    URI = "bolt://127.0.0.1:7687"
    USER = "neo4j"
    PASSWORD = "1234"
    convert = EtlFromPostgresToNeo4j(URI, USER, PASSWORD)
    try:
        convert.transform_postgres_to_neo4j()
    finally:
        convert.close()