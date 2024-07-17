CREATE TABLE customers(
	customer_id INT AUTO_INCREMENT,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email_address VARCHAR(255),
    number_of_complaints INT,
    primary key (customer_id)
);

ALTER TABLE customers
ADD COLUMN gender ENUM ('M','F') AFTER last_name;
INSERT INTO customers(first_name, last_name,gender,email_address,number_of_complaints) VALUES ('John','Mackinley','M','johnmackinley@365careers.com',0);

ALTER TABLE customers
CHANGE COLUMN number_of_complaints number_of_complaints INT DEFAULT 0;

INSERT INTO customers(first_name,last_name,gender)
VALUES ('Peter','Figaro','M');

SELECT * FROM customers;
