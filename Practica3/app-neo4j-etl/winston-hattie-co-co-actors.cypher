MATCH (hattie:Actor {name: "Winston, Hattie"})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(coactor:Actor)
WITH DISTINCT coactor, hattie
MATCH (actor:Actor)-[:ACTED_IN]->(m2:Movie)<-[:ACTED_IN]-(coactor)
WHERE actor.name <> "Winston, Hattie" AND NOT (actor)-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(hattie)
RETURN DISTINCT actor.name AS actor_name
ORDER BY actor_name
LIMIT 10;