ALTER TABLE customers
ADD COLUMN promo DECIMAL(5, 2);

CREATE OR REPLACE FUNCTION apply_promo_discount() RETURNS TRIGGER AS $$
BEGIN
    -- Pausa de nn segundos
    PERFORM pg_sleep(nn);

    UPDATE orderdetail
    SET price = (SELECT price FROM products WHERE products.prod_id = orderdetail.prod_id) - 
                ((SELECT price FROM products WHERE products.prod_id = orderdetail.prod_id) * (NEW.promo / 100))
    FROM orders
    WHERE orders.customerid = NEW.customerid
    AND orders.orderid = orderdetail.orderid;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_apply_promo_discount
AFTER UPDATE OF promo ON customers
FOR EACH ROW
EXECUTE FUNCTION apply_promo_discount();


-- e. Insertar un sleep en borraCiudad 
CREATE OR REPLACE FUNCTION borraCiudad(city_id INT) RETURNS VOID AS $$
BEGIN
    -- Pausa de nn segundos antes de borrar la ciudad
    PERFORM pg_sleep(nn); 

    DELETE FROM cities WHERE id = city_id;

END;
$$ LANGUAGE plpgsql;

-- f. Crear uno o varios carritos con status NULL
UPDATE orders
SET status = NULL
WHERE customerid IN (SELECT customerid FROM customers LIMIT 2);

-- g. Realizar un SELECT antes y después de actualizar la columna promo
-- (Ejemplo para cliente con ID 1)
-- En una sesión:
SELECT * FROM customers WHERE customerid = 1;

-- En otra sesión:
UPDATE customers
SET promo = 20 -- Aplica un 20% de descuento
WHERE customerid = 1;

-- Repite el SELECT en la primera sesión para observar los cambios

-- h. Comentario sobre los datos visibles durante el sleep
-- Durante el `pg_sleep`, los datos alterados no son visibles porque la transacción aún no se ha completado.
-- Esto se debe al aislamiento transaccional en PostgreSQL (por defecto, READ COMMITTED o SERIALIZABLE).

-- i. Verificar bloqueos mediante pgAdmin o pg_stat_activity
-- Usar el siguiente comando para observar bloqueos:
SELECT * FROM pg_stat_activity WHERE state = 'active';

-- j. Ajustar los puntos de sleep para causar un deadlock
-- Crear un escenario de deadlock ajustando los tiempos de sleep en borraCiudad y el trigger.
-- Explicación: El deadlock ocurre si dos transacciones intentan adquirir recursos que el otro ya posee y ninguna puede continuar.

-- Ejemplo: 
-- Transacción 1 intenta actualizar `promo` mientras Transacción 2 intenta borrar una ciudad asociada a un pedido. 
-- Ambos esperan mutuamente.

-- k. Discusión sobre cómo evitar deadlocks
-- - Diseñar un orden consistente para acceder a los recursos.
-- - Usar tiempos de espera para detectar y resolver deadlocks automáticamente.
-- - Reducir el alcance de las transacciones y los bloqueos.