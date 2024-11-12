-- Eliminar índices existentes (si existen)
DROP INDEX IF EXISTS idx_orders_customerid;
DROP INDEX IF EXISTS idx_orders_orderdate;
DROP INDEX IF EXISTS idx_customers_customerid;
DROP INDEX IF EXISTS idx_customers_country;
DROP INDEX IF EXISTS idx_orders_customerid_orderdate;
DROP INDEX IF EXISTS idx_customers_customerid_country;

-- Crear nuevos índices individuales necesarios
CREATE INDEX idx_orders_customerid ON orders (customerid);
CREATE INDEX idx_orders_orderdate ON orders (orderdate);
CREATE INDEX idx_customers_customerid ON customers (customerid);
CREATE INDEX idx_customers_country ON customers (country);

-- Estudio del plan de ejecución de la consulta con índices individuales
EXPLAIN
SELECT COUNT(DISTINCT state) AS num_estados
FROM customers c
JOIN orders o ON c.customerid = o.customerid
WHERE o.orderdate >= '2017-01-01' AND o.orderdate < '2018-01-01'
AND c.country = 'Spain';

-- Eliminar índices individuales
DROP INDEX IF EXISTS idx_orders_customerid;
DROP INDEX IF EXISTS idx_orders_orderdate;
DROP INDEX IF EXISTS idx_customers_customerid;
DROP INDEX IF EXISTS idx_customers_country;

-- Crear nuevos índices compuestos
CREATE INDEX idx_orders_customerid_orderdate ON orders (customerid, orderdate);
CREATE INDEX idx_customers_customerid_country ON customers (customerid, country);

-- Estudio del plan de ejecución de la consulta con índices compuestos
EXPLAIN
SELECT COUNT(DISTINCT state) AS num_estados
FROM customers c
JOIN orders o ON c.customerid = o.customerid
WHERE o.orderdate >= '2017-01-01' AND o.orderdate < '2018-01-01'
AND c.country = 'Spain';