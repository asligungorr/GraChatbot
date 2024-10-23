
# Import required libraries
import sqlite3  # For SQLite database operations
import os      # For file and directory operations

# Directory setup
# Creates a 'data' directory if it doesn't exist to store the database file
# exist_ok=True prevents errors if directory already exists
os.makedirs('data', exist_ok=True)

# Database file configuration
data_dir = 'data'  # Directory name for database storage
os.makedirs(data_dir, exist_ok=True)  # Ensure directory exists
db_path = os.path.join(data_dir, 'employee.db')  # Full path to database file

# Database cleanup
# If database file exists, remove it to start fresh
# This ensures we don't have conflicts with existing data
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed existing database file: {db_path}")


# Database initialization
# Create new SQLite database connection
# will create a new database file if it doesn't exist
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Schema Definition
# Creates all necessary tables with appropriate constraints
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

cursor.executescript('''
-- More employees
INSERT INTO employees (emp_no, birth_date, first_name, last_name, gender, hire_date)
VALUES 
(10004, '1954-05-01', 'Christian', 'Koblick', 'M', '1986-12-01'),
(10005, '1955-01-21', 'Kyoichi', 'Maliniak', 'M', '1989-09-12'),
(10006, '1953-04-20', 'Anneke', 'Preusig', 'F', '1989-06-02'),
(10007, '1957-05-23', 'Tzvetan', 'Zielinski', 'F', '1989-02-10'),
(10008, '1958-02-19', 'Saniya', 'Kalloufi', 'M', '1994-09-15'),
(10009, '1952-04-19', 'Sumant', 'Peac', 'F', '1985-02-18'),
(10010, '1963-06-01', 'Duangkaew', 'Piveteau', 'F', '1989-08-24'),
(10011, '1953-11-07', 'Mary', 'Sluis', 'F', '1990-01-22'),
(10012, '1960-10-04', 'Patricio', 'Bridgland', 'M', '1992-12-18'),
(10013, '1963-06-07', 'Eberhardt', 'Terkki', 'M', '1985-10-20'),
(10014, '1956-02-12', 'Berni', 'Genin', 'M', '1987-03-11'),
(10015, '1959-08-19', 'Guoxiang', 'Nooteboom', 'M', '1987-07-02');

-- More departments
INSERT INTO departments (dept_no, dept_name)
VALUES
('d004', 'Production'),
('d005', 'Development'),
('d006', 'Quality Management'),
('d007', 'Sales'),
('d008', 'Research'),
('d009', 'Customer Service');

-- More department managers
INSERT INTO dept_manager (emp_no, dept_no, from_date, to_date)
VALUES
(10004, 'd003', '1986-12-01', '1994-12-01'),
(10006, 'd004', '1989-06-02', '9999-01-01'),
(10009, 'd005', '1985-02-18', '1991-02-18'),
(10013, 'd006', '1985-10-20', '9999-01-01'),
(10014, 'd007', '1987-03-11', '1992-03-11'),
(10015, 'd008', '1987-07-02', '9999-01-01');

-- More department employees
INSERT INTO dept_emp (emp_no, dept_no, from_date, to_date)
VALUES
(10004, 'd003', '1986-12-01', '9999-01-01'),
(10005, 'd004', '1989-09-12', '9999-01-01'),
(10006, 'd004', '1989-06-02', '9999-01-01'),
(10007, 'd005', '1989-02-10', '9999-01-01'),
(10008, 'd005', '1994-09-15', '9999-01-01'),
(10009, 'd005', '1985-02-18', '9999-01-01'),
(10010, 'd006', '1989-08-24', '9999-01-01'),
(10011, 'd006', '1990-01-22', '9999-01-01'),
(10012, 'd007', '1992-12-18', '9999-01-01'),
(10013, 'd007', '1985-10-20', '9999-01-01'),
(10014, 'd008', '1987-03-11', '9999-01-01'),
(10015, 'd008', '1987-07-02', '9999-01-01');

-- More titles with history
INSERT INTO titles (emp_no, title, from_date, to_date)
VALUES
(10004, 'Engineer', '1986-12-01', '1995-12-01'),
(10004, 'Senior Engineer', '1995-12-01', '9999-01-01'),
(10005, 'Senior Staff', '1989-09-12', '9999-01-01'),
(10006, 'Senior Engineer', '1989-06-02', '9999-01-01'),
(10007, 'Senior Staff', '1989-02-10', '9999-01-01'),
(10008, 'Assistant Engineer', '1994-09-15', '1998-09-15'),
(10008, 'Engineer', '1998-09-15', '9999-01-01'),
(10009, 'Engineer', '1985-02-18', '1990-02-18'),
(10009, 'Senior Engineer', '1990-02-18', '9999-01-01'),
(10010, 'Engineer', '1989-08-24', '9999-01-01'),
(10011, 'Staff', '1990-01-22', '1996-01-22'),
(10011, 'Senior Staff', '1996-01-22', '9999-01-01'),
(10012, 'Engineer', '1992-12-18', '9999-01-01'),
(10013, 'Staff', '1985-10-20', '1993-10-20'),
(10013, 'Senior Staff', '1993-10-20', '9999-01-01'),
(10014, 'Engineer', '1987-03-11', '1995-03-11'),
(10014, 'Senior Engineer', '1995-03-11', '9999-01-01'),
(10015, 'Senior Engineer', '1987-07-02', '9999-01-01');

-- More salaries with history
INSERT INTO salaries (emp_no, salary, from_date, to_date)
VALUES
(10004, 53422, '1986-12-01', '1987-12-01'),
(10004, 57628, '1987-12-01', '1988-12-01'),
(10004, 65076, '1988-12-01', '1989-12-01'),
(10005, 66961, '1989-09-12', '1990-09-12'),
(10005, 71046, '1990-09-12', '1991-09-12'),
(10006, 43311, '1989-06-02', '1990-06-02'),
(10006, 46535, '1990-06-02', '1991-06-02'),
(10007, 70728, '1989-02-10', '1990-02-10'),
(10007, 74917, '1990-02-10', '1991-02-10'),
(10008, 40000, '1994-09-15', '1995-09-15'),
(10008, 42000, '1995-09-15', '1996-09-15'),
(10009, 41538, '1985-02-18', '1986-02-18'),
(10009, 45131, '1986-02-18', '1987-02-18'),
(10010, 48271, '1989-08-24', '1990-08-24'),
(10010, 51381, '1990-08-24', '1991-08-24'),
(10011, 45728, '1990-01-22', '1991-01-22'),
(10011, 47017, '1991-01-22', '1992-01-22'),
(10012, 47017, '1992-12-18', '1993-12-18'),
(10012, 51047, '1993-12-18', '1994-12-18'),
(10013, 45145, '1985-10-20', '1986-10-20'),
(10013, 48281, '1986-10-20', '1987-10-20'),
(10014, 46043, '1987-03-11', '1988-03-11'),
(10014, 47913, '1988-03-11', '1989-03-11'),
(10015, 40505, '1987-07-02', '1988-07-02'),
(10015, 42362, '1988-07-02', '1989-07-02');
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Database created successfully at: {os.path.abspath(db_path)}")
print("Sample data has been inserted.")