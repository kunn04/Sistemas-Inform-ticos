WITH cte AS (
    SELECT ctid, ROW_NUMBER() OVER (PARTITION BY orderid, prod_id ORDER BY ctid) AS rn
    FROM orderdetail
)
DELETE FROM orderdetail
WHERE ctid IN (
    SELECT ctid FROM cte WHERE rn > 1
);

ALTER TABLE orderdetail
ADD CONSTRAINT pk_orderdetail
PRIMARY KEY (orderid, prod_id);

ALTER TABLE inventory
ADD CONSTRAINT fk_prod_id
FOREIGN KEY (prod_id) REFERENCES products(prod_id);

ALTER TABLE imdb_actormovies
ADD CONSTRAINT pk_actormovies
PRIMARY KEY (actorid, movieid);

ALTER TABLE orderdetail 
ADD CONSTRAINT fk_orderid
FOREIGN KEY (orderid) REFERENCES orders(orderid);

ALTER TABLE orderdetail 
ADD CONSTRAINT fk_prod_id
FOREIGN KEY (prod_id) REFERENCES products(prod_id);

ALTER TABLE imdb_actormovies
ADD CONSTRAINT fk_actorid
FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid);

ALTER TABLE imdb_actormovies
ADD CONSTRAINT fk_movieid
FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);

ALTER TABLE orders
ADD CONSTRAINT fk_customerid
FOREIGN KEY (customerid) REFERENCES customers(customerid);

ALTER TABLE customers 
ADD COLUMN balance DECIMAL(10, 2) DEFAULT 0.00;

CREATE TABLE ratings (
    customerid INT,
    movieid INT,
    likes BOOLEAN,
    rating_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customerid, movieid),
    FOREIGN KEY (customerid) REFERENCES customers(customerid),
    FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid)
);


ALTER TABLE customers 
ALTER COLUMN password TYPE VARCHAR(128);


CREATE OR REPLACE PROCEDURE setCustomersBalance (IN initialBalance BIGINT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE customers
    SET balance = FLOOR(RANDOM() * initialBalance);
END
$$;;


CALL setCustomersBalance(200)
