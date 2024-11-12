-- Crea la tabla 'creditcardCustomer' para almacenar los datos de la tarjeta de crédito de los clientes
create table creditcardCustomer (
	customerid INT not null,
	creditcard VARCHAR(50) not null,
	exp_date DATE null,
	cardholder VARCHAR(128) null,
	cvv VARCHAR(3) null,
	constraint pk_creditcardCustomer primary key (customerid, creditcard),
	constraint fk_customerid foreign key (customerid) references customers(customerid)
);

-- Inserta en la nueva tabla 'creditcardCustomer' el 'customerid' y la 'creditcard' de todos los registros de 'customers'
insert into creditcardCustomer(customerid, creditcard)
select customerid, creditcard
from customers;

-- Elimina la columna 'creditcard' de la tabla 'customers'
alter table customers
drop column creditcard;