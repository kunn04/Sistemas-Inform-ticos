-- Elimina los duplicados en orderdetail según orderid y prod_id, conservando solo el primero
WITH cte AS (
    SELECT ctid, ROW_NUMBER() OVER (PARTITION BY orderid, prod_id ORDER BY ctid) AS rn
    FROM orderdetail
)
DELETE FROM orderdetail
WHERE ctid IN (
    SELECT ctid FROM cte WHERE rn > 1
);

-- Define la clave primaria en orderdetail para orderid y prod_id
ALTER TABLE orderdetail
ADD CONSTRAINT pk_orderdetail
PRIMARY KEY (orderid, prod_id);

-- Establece una clave foránea en inventory que referencia a prod_id de products
ALTER TABLE inventory
ADD CONSTRAINT fk_prod_id
FOREIGN KEY (prod_id) REFERENCES products(prod_id);

-- Define la clave primaria en imdb_actormovies para actorid y movieid
ALTER TABLE imdb_actormovies
ADD CONSTRAINT pk_actormovies
PRIMARY KEY (actorid, movieid);

-- Añade las claves foráneas en orderdetail para orderid y prod_id
ALTER TABLE orderdetail 
ADD CONSTRAINT fk_orderid
FOREIGN KEY (orderid) REFERENCES orders(orderid);

ALTER TABLE orderdetail 
ADD CONSTRAINT fk_prod_id
FOREIGN KEY (prod_id) REFERENCES products(prod_id);

-- Añade claves foráneas en imdb_actormovies para actorid y movieid
ALTER TABLE imdb_actormovies
ADD CONSTRAINT fk_actorid
FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid);

ALTER TABLE imdb_actormovies
ADD CONSTRAINT fk_movieid
FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);

-- Agrega una clave foránea en orders que referencia customerid de customers
ALTER TABLE orders
ADD CONSTRAINT fk_customerid
FOREIGN KEY (customerid) REFERENCES customers(customerid);

-- Añade una columna balance en customers con un valor por defecto de 0.00
ALTER TABLE customers 
ADD COLUMN balance DECIMAL(10, 2) DEFAULT 0.00;

-- Crea una tabla ratings para almacenar las valoraciones de los clientes a las películas
CREATE TABLE ratings (
    customerid INT,
    movieid INT,
    likes BOOLEAN,
    rating_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customerid, movieid),
    FOREIGN KEY (customerid) REFERENCES customers(customerid),
    FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid)
);

-- Amplía el tamaño de la columna password en customers
ALTER TABLE customers 
ALTER COLUMN password TYPE VARCHAR(128);

-- Asigna a cada cliente un balance aleatorio hasta initialBalance
CREATE OR REPLACE PROCEDURE setCustomersBalance (IN initialBalance BIGINT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE customers
    SET balance = FLOOR(RANDOM() * initialBalance);
END
$$;;

-- Llama al procedimiento para establecer balances aleatorios con un máximo de 200
CALL setCustomersBalance(200);
