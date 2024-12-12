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