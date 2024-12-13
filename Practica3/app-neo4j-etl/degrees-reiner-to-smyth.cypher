MATCH (start:Director {name: "Reiner, Carl"}), (end:Actor {name: "Smyth, Lisa (I)"})
MATCH path = shortestPath((start)-[*]-(end))
RETURN path;