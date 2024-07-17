SELECT 
    first_name, last_name
FROM
    employees;

SELECT 
    *
FROM
    employees;
    
SELECT 
    dept_no
FROM
    departments;
SELECT 
    *
FROM
    departments;
    
SELECT 
    *
FROM
    employees
WHERE
    first_name = 'Denis'
        OR first_name = 'Elvis';
    
SELECT 
    *
FROM
    employees
WHERE
    first_name = 'Elvis';

SELECT 
    *
FROM
    employees
WHERE
    gender = 'F'
        AND (first_name = 'Kellie'
        OR first_name = 'Aruna');
SELECT 
    *
FROM
    employees
WHERE
    first_name IN ('Elvis' , 'Denis');
SELECT 
    *
FROM
    employees
WHERE
    first_name NOT IN ('Jacob' , 'John', 'Mark');
SELECT 
    *
FROM
    employees
WHERE
    first_name LIKE ('Mark%');
SELECT 
    *
FROM
    employees
WHERE
    hire_date LIKE ('2000%');
SELECT 
    *
FROM
    employees
WHERE
    emp_no LIKE ('1000_');
SELECT 
    *
FROM
    employees
WHERE
    first_name LIKE ('%Jack%');
SELECT 
    *
FROM
    employees
WHERE
    first_name NOT LIKE ('%Jack%');
SELECT 
    *
FROM
    salaries
WHERE
    salary BETWEEN 66000 AND 70000;
SELECT 
    *
FROM
    employees
WHERE
    emp_no NOT BETWEEN '10004' AND '10012';
SELECT 
    *
FROM
    departments
WHERE
    dept_no BETWEEN 'd003' AND 'd006';
SELECT 
    *
FROM
    departments
WHERE
    dept_no IS NOT NULL;
SELECT 
    *
FROM
    employees
WHERE
    gender = 'F'
        AND (hire_date >= '2000-01-01');
SELECT 
    *
FROM
    salaries
WHERE
    salary > 150000;
SELECT DISTINCT
    hire_date
FROM
    employees;
SELECT 
    COUNT(*)
FROM
    salaries
WHERE
    salary >= 100000;
SELECT 
    COUNT(*)
FROM
    dept_manager;
SELECT 
    *
FROM
    employees
ORDER BY hire_date DESC;
SELECT 
    salary, COUNT(emp_no) AS emps_with_same_salary
FROM
    salaries
WHERE
    salary > 80000
GROUP BY salary
ORDER BY salary;
SELECT 
    emp_no
FROM
    salaries
GROUP BY emp_no
HAVING AVG(salary > 12000)
ORDER BY emp_no;
SELECT 
    emp_no, COUNT(from_date) AS number_of_contracts
FROM
    dept_emp
WHERE
    from_date > '2000-01-01'
GROUP BY emp_no
HAVING COUNT(from_date) > 1
ORDER BY emp_no;

INSERT INTO employees

VALUES

(

    999903,

    '1977-09-14',

    'Johnathan',

    'Creek',

    'M',

    '1999-01-01'

);

SELECT 
    *
FROM
    titles
LIMIT 10;
insert into titles (emp_no,title,from_date) values (999903, 'Senior Engineer', '1997-09-01');
SELECT 
    *
FROM
    titles
ORDER BY emp_no DESC
LIMIT 10;
SELECT 
    *
FROM
    dept_emp
LIMIT 10;
insert into dept_emp values(999903,'d005','1997-09-01','9999-01-01');
SELECT 
    *
FROM
    dept_emp
ORDER BY emp_no DESC
LIMIT 10;
insert into employees values (999901,'1986-04-12','John','Smith','M','2011-01-01');
UPDATE employees 
SET 
    first_name = 'Stella',
    last_name = 'Parkinson',
    birth_date = '1990-12-31',
    gender = 'F'
WHERE
    emp_no = 999901;
SELECT 
    *
FROM
    employees
WHERE
    emp_no = 999901;
CREATE TABLE departments_dup (
    dept_no CHAR(4) NOT NULL,
    dept_name VARCHAR(40) NOT NULL
);

SELECT 
    *
FROM
    departments;

INSERT INTO departments_dup
(
    dept_no,
    dept_name
)
SELECT 
	*
FROM 
	departments_dup;

    
COMMIT;
UPDATE departments_dup 
SET 
    dept_no = 'NULL',
    dept_name = 'Quality Control';
ROLLBACK;
UPDATE departments 
SET 
    dept_name = 'Data Analysis'
WHERE
    dept_no = 'd010';
SELECT 
    *
FROM
    titles
WHERE
    emp_no = '999903';
DELETE FROM departments 
WHERE
    dept_no = 'd010';

SELECT 
    COUNT(DISTINCT dept_no)
FROM
    dept_emp;

SELECT 
    SUM(salary)
FROM
    salaries
WHERE
    from_date > '1997-01-01';

 alter table departments_dup change dept_no dept_no VARCHAR(4) NULL;
 alter table departments_dup change dept_name dept_name VARCHAR(40) NULL;
 
 drop table if exists dept_manager_dup;
CREATE TABLE dept_manager_dup (
    emp_no INT(11) NOT NULL,
    dept_no CHAR(4) NULL,
    from_date DATE NOT NULL,
    to_date DATE NULL
);
 INSERT INTO dept_manager_dup
 select * from dept_manager;
 INSERT INTO dept_manager_dup (emp_no, from_date)
 VALUES (999904, '2017-01-01'),(999905, '2017-01-01'),(999906, '2017-01-01'),(999907, '2017-01-01');
DELETE FROM dept_manager_dup 
WHERE
    dept_no = 'd001';
SELECT 
    *
FROM
    dept_manager_dup;
 
DELETE FROM departments_dup 
WHERE
    dept_name = 'Business Analysis';
 
 insert into departments_dup(dept_name) values ('Public Relations');
 insert into departments_dup(dept_no) values('d010'),('d011');
 
 
 
 