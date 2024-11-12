-- Función 'actualizaCarritoFunct' que se ejecutará como trigger
create or replace function actualizaCarritoFunct()
returns trigger
as $$
begin
	
    -- Verifica si la operación es una inserción o actualización en la tabla 'orderdetail'
	if (tg_op = 'INSERT' or tg_op = 'UPDATE') then
	
        -- Actualiza el 'netamount' en la tabla 'orders' para reflejar el nuevo subtotal
        -- Calcula la suma de precio * cantidad para cada producto en el pedido
		update orders o
		set netamount = (
			select SUM(od.price * od.quantity)
			from orderdetail od
			where od.orderid = o.orderid
		);
		
        -- Actualiza 'totalamount' en la tabla 'orders' para reflejar el total con impuestos
        -- Calcula el total sumando el subtotal (netamount) más el impuesto
		UPDATE orders o
    	SET totalamount = netamount + (netamount * (o.tax / 100));

    -- Verifica si la operación es una eliminación en la tabla 'orderdetail'
	elsif (tg_op = 'DELETE') then
		
        -- Actualiza el 'netamount' para reflejar el cambio tras la eliminación de un producto
		update orders o
		set netamount = (
			select SUM(od.price * od.quantity)
			from orderdetail od
			where od.orderid = o.orderid
		);
		
        -- Actualiza el 'totalamount' para reflejar el cambio tras la eliminación
        -- Vuelve a calcular el total incluyendo impuestos después de actualizar 'netamount'
		UPDATE orders o
    	SET totalamount = netamount + (netamount * (o.tax / 100));
	end if;

	-- Retorna null ya que el trigger es de tipo AFTER y no se necesita modificar el registro procesado
	return null;
end;
$$ language plpgsql;

-- Crea el trigger 'actualizaCarrito' en la tabla 'orderdetail'
-- Este trigger se ejecuta después de cada inserción, actualización o eliminación de un registro
-- Llama a la función 'actualizaCarritoFunct' para recalcular los montos del pedido correspondiente
create or replace trigger actualizaCarrito
after insert or update or delete on orderdetail
for each row
execute function actualizaCarritoFunct();
