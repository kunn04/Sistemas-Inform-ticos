ALTER TABLE customers
ADD COLUMN promo DECIMAL(5, 2);

CREATE OR REPLACE FUNCTION apply_promo_discount() RETURNS TRIGGER AS $$
BEGIN
	

    UPDATE orderdetail
    SET price = (SELECT price FROM products WHERE products.prod_id = orderdetail.prod_id) - 
                ((SELECT price FROM products WHERE products.prod_id = orderdetail.prod_id) * (NEW.promo / 100))
    FROM orders
    WHERE orders.customerid = NEW.customerid
    AND orders.orderid = orderdetail.orderid;
    RETURN NEW;

	PERFORM pg_sleep(10);

END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_apply_promo_discount
AFTER UPDATE OF promo ON customers
FOR EACH ROW
EXECUTE FUNCTION apply_promo_discount();

CREATE OR REPLACE FUNCTION update_order_netamount_and_total()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE orders
    SET 
        netamount = (SELECT SUM(price * quantity)
                     FROM orderdetail
                     WHERE orderid = NEW.orderid),
        totalamount = netamount + COALESCE(tax, 0) 
    WHERE orderid = NEW.orderid;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_order_netamount_and_total
AFTER UPDATE OF price ON orderdetail
FOR EACH ROW
EXECUTE FUNCTION update_order_netamount_and_total();


