SELECT COUNT(DISTINCT state) AS num_estados
FROM customers c
JOIN orders o ON c.customerid = o.customerid
WHERE o.orderdate >= '2017-01-01' AND o.orderdate < '2018-01-01'
AND c.country = 'Spain';




