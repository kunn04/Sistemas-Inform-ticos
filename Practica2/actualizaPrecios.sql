-- Procedimiento para calcular el precio total de cada línea en orderdetail
CREATE OR REPLACE PROCEDURE calculatePricesOrderdetail()
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE orderdetail od
    SET price = p.price * od.quantity
    FROM products p
    WHERE od.prod_id = p.prod_id;
END
$$;;

-- Procedimiento para calcular netamount y totalamount en orders
CREATE OR REPLACE PROCEDURE calculateAmountsOrders()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Calcula el netamount (subtotal sin impuestos) para cada pedido
    UPDATE orders o
    SET netamount = (
        SELECT COALESCE(SUM(od.price), 0)  -- Suma los precios en orderdetail
        FROM orderdetail od
        WHERE od.orderid = o.orderid
    );

    -- Calcula el totalamount (total con impuestos) usando el netamount actualizado
    UPDATE orders o
    SET totalamount = netamount + (netamount * (o.tax / 100));
END
$$;;

-- Llamada a los procedimientos
CALL calculatePricesOrderdetail();
CALL calculateAmountsOrders();