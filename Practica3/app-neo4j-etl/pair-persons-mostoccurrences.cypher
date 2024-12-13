MATCH (p1:Actor)-[r1:ACTED_IN|DIRECTED]->(m:Movie)<-[r2:ACTED_IN|DIRECTED]-(p2:Actor)
WHERE p1 <> p2 AND m.movietitle IS NOT NULL
WITH p1, p2, COLLECT(m.movietitle) AS sharedMovies
WHERE SIZE(sharedMovies) > 1
RETURN p1.name AS Person1, p2.name AS Person2, sharedMovies
ORDER BY SIZE(sharedMovies) DESC, Person1, Person2;