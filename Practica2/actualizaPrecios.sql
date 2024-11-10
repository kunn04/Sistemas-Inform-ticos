CREATE OR REPLACE PROCEDURE calculateOrderTotal(IN p_orderid INT)
LANGUAGE plpgsql
AS $$
DECLARE
    order_total NUMERIC := 0;
BEGIN
    SELECT SUM(od.price * od.quantity)
    INTO order_total
    FROM orderdetail od
    WHERE od.orderid = p_orderid;

    UPDATE orders
    SET totalamount = order_total
    WHERE orderid = p_orderid;
END
$$;

-- Llamar al procedimiento para cada pedido en la tabla orders
DO $$
DECLARE
    o_id INT;
BEGIN
    FOR o_id IN SELECT orderid FROM orders
    LOOP
        CALL calculateOrderTotal(o_id);
    END LOOP;
END
$$;
