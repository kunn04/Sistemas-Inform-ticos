--Ejecución de ANALYZE 
ANALYZE orders;

-- Crea un índice en la columna 'status' de la tabla 'orders'
CREATE INDEX idx_orders_status ON orders (status);

-- Estudio del plan de ejecución de la consulta con índice en la columna 'status'
EXPLAIN
select count(*)
from orders
where status is null;
select count(*)
from orders
where status ='Shipped';

-- Estudio del plan de ejecución de la segunda consulta con índice en la columna 'status'
EXPLAIN
select count(*)
from orders
where status ='Paid';
select count(*)
from orders
where status ='Processed';

-- Elimina el índice creado en la columna 'status' de la tabla 'orders'
DROP INDEX IF EXISTS idx_orders_status;