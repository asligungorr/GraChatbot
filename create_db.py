import sqlite3
import os

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Connect to the database (this will create it if it doesn't exist)
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)

# Set the database file path
db_path = os.path.join(data_dir, 'employee.db')

# Remove the existing database file if it exists
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed existing database file: {db_path}")

# Create a new database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.executescript('''
CREATE TABLE employees (
    emp_no      INTEGER         NOT NULL PRIMARY KEY,
    birth_date  DATE            NOT NULL,
    first_name  VARCHAR(14)     NOT NULL,
    last_name   VARCHAR(16)     NOT NULL,
    gender      CHAR(1)         NOT NULL,    
    hire_date   DATE            NOT NULL
);

CREATE TABLE departments (
    dept_no     CHAR(4)         NOT NULL PRIMARY KEY,
    dept_name   VARCHAR(40)     NOT NULL UNIQUE
);

CREATE TABLE dept_manager (
   emp_no       INTEGER         NOT NULL,
   dept_no      CHAR(4)         NOT NULL,
   from_date    DATE            NOT NULL,
   to_date      DATE            NOT NULL,
   PRIMARY KEY (emp_no, dept_no),
   FOREIGN KEY (emp_no)  REFERENCES employees (emp_no),
   FOREIGN KEY (dept_no) REFERENCES departments (dept_no)
);

CREATE TABLE dept_emp (
    emp_no      INTEGER         NOT NULL,
    dept_no     CHAR(4)         NOT NULL,
    from_date   DATE            NOT NULL,
    to_date     DATE            NOT NULL,
    PRIMARY KEY (emp_no, dept_no),
    FOREIGN KEY (emp_no)  REFERENCES employees   (emp_no),
    FOREIGN KEY (dept_no) REFERENCES departments (dept_no)
);

CREATE TABLE titles (
    emp_no      INTEGER         NOT NULL,
    title       VARCHAR(50)     NOT NULL,
    from_date   DATE            NOT NULL,
    to_date     DATE,
    PRIMARY KEY (emp_no, title, from_date),
    FOREIGN KEY (emp_no) REFERENCES employees (emp_no)
);

CREATE TABLE salaries (
    emp_no      INTEGER         NOT NULL,
    salary      INTEGER         NOT NULL,
    from_date   DATE            NOT NULL,
    to_date     DATE            NOT NULL,
    PRIMARY KEY (emp_no, from_date),
    FOREIGN KEY (emp_no) REFERENCES employees (emp_no)
);
''')

# Insert some sample data
cursor.executescript('''
INSERT INTO employees (emp_no, birth_date, first_name, last_name, gender, hire_date)
VALUES 
(10001, '1953-09-02', 'Georgi', 'Facello', 'M', '1986-06-26'),
(10002, '1964-06-02', 'Bezalel', 'Simmel', 'F', '1985-11-21'),
(10003, '1959-12-03', 'Parto', 'Bamford', 'M', '1986-08-28');

INSERT INTO departments (dept_no, dept_name)
VALUES
('d001', 'Marketing'),
('d002', 'Finance'),
('d003', 'Human Resources');

INSERT INTO dept_manager (emp_no, dept_no, from_date, to_date)
VALUES
(10001, 'd001', '1986-06-26', '9999-01-01'),
(10002, 'd002', '1985-11-21', '9999-01-01');

INSERT INTO dept_emp (emp_no, dept_no, from_date, to_date)
VALUES
(10001, 'd001', '1986-06-26', '9999-01-01'),
(10002, 'd002', '1985-11-21', '9999-01-01'),
(10003, 'd003', '1986-08-28', '9999-01-01');

INSERT INTO titles (emp_no, title, from_date, to_date)
VALUES
(10001, 'Senior Engineer', '1986-06-26', '9999-01-01'),
(10002, 'Staff', '1985-11-21', '9999-01-01'),
(10003, 'Assistant Engineer', '1986-08-28', '9999-01-01');

INSERT INTO salaries (emp_no, salary, from_date, to_date)
VALUES
(10001, 60117, '1986-06-26', '1987-06-26'),
(10002, 65828, '1985-11-21', '1986-11-21'),
(10003, 40006, '1986-08-28', '1987-08-28'),
(10001, 62102, '1987-06-26', '1988-06-25'),
(10002, 69000, '1986-11-21', '1987-11-21'),
(10003, 43616, '1987-08-28', '1988-08-27');
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Database created successfully at: {os.path.abspath(db_path)}")
print("Sample data has been inserted.")