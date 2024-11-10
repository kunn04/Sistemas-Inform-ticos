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

CREATE OR REPLACE PROCEDURE calculateAmountsOrders()
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE orders o
    SET netamount = (
        SELECT SUM(od.price)
        FROM orderdetail od
        WHERE od.orderid = o.orderid
    ),
    totalamount = netamount + (netamount * (o.tax / 100));
END
$$;;

CALL calculatePricesOrderdetail();

CALL calculateAmountsOrders();
