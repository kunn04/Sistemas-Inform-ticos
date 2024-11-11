create table creditcardCustomer (
	customerid INT not null,
	creditcard VARCHAR(50) not null,
	exp_date DATE null,
	cardholder VARCHAR(128) null,
	cvv VARCHAR(3) null,
	constraint pk_creditcardCustomer primary key (customerid, creditcard),
	constraint fk_customerid foreign key (customerid) references customers(customerid)
);

insert into creditcardCustomer(customerid, creditcard)
select customerid, creditcard
from customers;


alter table customers
drop column creditcard;