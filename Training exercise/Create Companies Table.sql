CREATE TABLE companies (
	company_id INT AUTO_INCREMENT,
    company_name VARCHAR(255) DEFAULT 'X',
    headquarters_phone_number VARCHAR(255),
    primary key (company_id),
    unique key (headquarters_phone_number)
    );

DROP TABLE companies;

ALTER TABLE companies
MODIFY company_name VARCHAR(255) NULL;

ALTER TABLE companies
CHANGE COLUMN company_name company_name VARCHAR(255) NOT NULL;

INSERT INTO companies( headquarters_phone_number,company_name)
VALUES ('+1 (202) 555-0196','Company A');

SELECT * FROM companies;

ALTER TABLE companies
CHANGE COLUMN headquarters_phone_number headquarters_phone_number VARCHAR(255) NULL;

ALTER TABLE companies
CHANGE COLUMN headquarters_phone_number headquarters_phone_number VARCHAR(255) NOT NULL;