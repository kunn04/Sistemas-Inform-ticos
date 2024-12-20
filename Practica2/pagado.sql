-- Función que se ejecutará como trigger para actualizar el stock y las ventas de un producto.
create or replace function pagadoFunct()
returns trigger
as $$
begin
	
	if (new.status = 'Paid') then
	
		update inventory i
		set
			stock = i.stock - od.quantity,
			sales = i.sales + od.quantity
		from orderdetail od
		where od.prod_id = i.prod_id and od.orderid = new.orderid;
	
	update customers c
	set balance = c.balance - o.totalamount
	from orders o
	where o.orderid = new.orderid and c.customerid = o.customerid;

	end if;

	return null;
end;
$$ language plpgsql;

-- Crea el trigger 'pagado' en la tabla 'orders' que se ejecuta después de actualizar el estado de un pedido a 'Paid'.
create or replace trigger pagado
after update of status on orders
for each row
when (new.status = 'Paid')
execute function pagadoFunct();
