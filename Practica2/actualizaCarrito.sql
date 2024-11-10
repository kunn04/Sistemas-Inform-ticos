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
		),	
		totalamount = (
            SELECT SUM(od.price * od.quantity) 
            FROM orderdetail od
            WHERE od.orderid = o.orderid
		) + (o.netamount * (o.tax / 100))
        WHERE o.orderid = NEW.orderid; 

	elsif (tg_op = 'DELETE') then
		
		update orders o
		set netamount = (
			select SUM(od.price * od.quantity)
			from orderdetail od
			where od.orderid = o.orderid
		),
		totalamount = (
            SELECT SUM(od.price * od.quantity)
            FROM orderdetail od
            WHERE od.orderid = o.orderid
		) + (o.netamount * (o.tax / 100))
	where o.orderid = old.orderid;
	end if;

	return null;
end;
$$ language plpgsql;

create or replace trigger actualizaCarrito
after insert or update or delete on orderdetail
for each row
execute function actualizaCarritoFunct();
