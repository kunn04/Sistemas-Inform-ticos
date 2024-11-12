create or replace function actualizaCarritoFunct()
returns trigger
as $$
begin
	
	if (tg_op = 'INSERT' or tg_op = 'UPDATE') then
	
		update orders o
		set netamount = (
			select SUM(od.price * od.quantity)
			from orderdetail od
			where od.orderid = o.orderid
		);
		UPDATE orders o
    	SET totalamount = netamount + (netamount * (o.tax / 100));

	elsif (tg_op = 'DELETE') then
		
		update orders o
		set netamount = (
			select SUM(od.price * od.quantity)
			from orderdetail od
			where od.orderid = o.orderid
		);
		UPDATE orders o
    	SET totalamount = netamount + (netamount * (o.tax / 100));
	end if;

	return null;
end;
$$ language plpgsql;

create or replace trigger actualizaCarrito
after insert or update or delete on orderdetail
for each row
execute function actualizaCarritoFunct();
