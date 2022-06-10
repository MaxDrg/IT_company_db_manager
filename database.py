import psycopg2

class Database: 
    def __init__(self, user: str = '0', passwd: str = '0'):
        try:
            self.conn = psycopg2.connect(
  			database = 'postgres',
			user = user,
			password = passwd,
			host = '127.0.0.1',
			port = '5432'
			)
            print ("Database connection established")
            self.success_connection = True
        except Exception as err:
            print(str(err))
            self.success_connection = False

    def get_employees(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT employees.id, employees.name, employees.age, exp_level.name, employees.accepted_in_company 
                                FROM employees
                                INNER JOIN expertise_levels AS exp_level USING (level_id)""")
            return cursor.fetchall()

    def add_employee(self, name: str, level: str, age: int, accepted):
        with self.conn.cursor() as cursor:
            cursor.execute("""CALL add_employee(%s, %s, %s, %s);""", (name, level, age, accepted))
            self.conn.commit()

    def del_employee(self, id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""DELETE FROM tasks WHERE employee = %s;""", (id, ))
            cursor.execute("""DELETE FROM employees WHERE id = %s;""", (id, ))
            self.conn.commit()

    def add_customer(self, name: str, contact: str, owner_name: str, cooperation_start: str):
        with self.conn.cursor() as cursor:
            cursor.execute("""CALL add_customer(%s, %s, %s, %s);""", (name, contact, owner_name, cooperation_start))
            self.conn.commit()

    def get_customers(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT id, name, cooperation_start, owner_name, contact 
                                FROM customers;""")
            return cursor.fetchall()

    def del_customer(self, id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT id FROM projects WHERE customer = %s;""", (id, ))
            projects = cursor.fetchall()
            for project in projects:
                cursor.execute("""DELETE FROM tasks WHERE project = %s;""", (project, ))
            cursor.execute("""DELETE FROM projects WHERE customer = %s;""", (id, ))
            cursor.execute("""DELETE FROM customers WHERE id = %s;""", (id, ))
            self.conn.commit()

    def add_level(self, name: str, salary: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""CALL add_expertise_level(%s, %s);""", (name, salary))
            self.conn.commit()

    def get_levels(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT level_id, name, salary
                                FROM expertise_levels;""")
            return cursor.fetchall()

    def del_level(self, id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT id FROM employees WHERE level_id = %s;""", (id, ))
            employees = cursor.fetchall()
            for employee in employees:
                cursor.execute("""DELETE FROM tasks WHERE customer = %s;""", (employee, ))
            cursor.execute("""DELETE FROM employees WHERE level_id = %s;""", (id, ))
            cursor.execute("""DELETE FROM expertise_levels WHERE level_id = %s;""", (id, ))
            self.conn.commit()

    def add_project(self, project_name: str, technical_task: str, customer: str, price: int, start_time: str):
        with self.conn.cursor() as cursor:
            cursor.execute("""CALL add_project(%s, %s, %s, %s, %s);""", (project_name, technical_task, customer, price, start_time))
            self.conn.commit()

    def get_projects(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT projects.id, projects.project_name, projects.technical_task, projects.start_time, projects.end_time, customers.name, projects.price 
                                FROM projects 
                                INNER JOIN customers
                                ON projects.customer = customers.id;""")
            return cursor.fetchall()

    def del_project(self, id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""DELETE FROM tasks WHERE project = %s;""", (id, ))
            cursor.execute("""DELETE FROM projects WHERE id = %s;""", (id, ))
            self.conn.commit()

    def add_task(self, employee: str, project: str, position: str):
        with self.conn.cursor() as cursor:
            cursor.execute("""CALL add_task(%s, %s, %s);""", (employee, project, position, ))
            self.conn.commit()

    def get_tasks(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT tasks.id, employees.name, projects.project_name, tasks.position
                                FROM tasks
                                INNER JOIN employees
                                ON tasks.employee = employees.id
                                INNER JOIN projects
                                ON tasks.project = projects.id;""")
            return cursor.fetchall()

    def del_task(self, id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""DELETE FROM tasks WHERE id = %s;""", (id, ))
            self.conn.commit()
        
    def get_levels_name(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT name
                                FROM expertise_levels;""")
            return cursor.fetchall()

    def get_customers_name(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT name
                                FROM customers;""")
            return cursor.fetchall()

    def get_employees_name(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT name
                                FROM employees;""")
            return cursor.fetchall()

    def get_employee_level(self, employee_name: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT expertise_levels.name
                                FROM employees
                                INNER JOIN expertise_levels USING(level_id)
                                WHERE employees.name = %s;""", (employee_name, ))
            return cursor.fetchone()

    def get_projects_name(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT project_name
                                FROM projects;""")
            return cursor.fetchall()
    
    def set_end_time(self, id: int, date: str):
        with self.conn.cursor() as cursor:
            cursor.execute("""UPDATE projects 
                                SET end_time = %s 
                                WHERE id = %s;""", (date, id, ))
            self.conn.commit()

    def get_expensive_projects(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM EXPENSIVE_PROJECTS """)
            return cursor.fetchall()
    
    def get_team_leads(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM TEAM_LEADS;""")
            return cursor.fetchall()

    def get_customers_by_phone(self, phone: str):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM get_customers_by_phone(%s);""", (phone, ))
            return cursor.fetchall()

    def get_employees_by_level(self, level: str):
        with self.conn.cursor() as cursor:
            cursor.execute("""select * from get_employees_by_level(%s);""", (level, ))
            return cursor.fetchall()

    def get_other_levels(self, level: str):
        with self.conn.cursor() as cursor:
            cursor.execute("""select salary from expertise_levels where not name = 'Senior';""")
            return cursor.fetchall()

    def get_senior_salary(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""select salary from expertise_levels where name = 'Senior';""")
            return cursor.fetchone()
        
    def update_salary(self, salary: int, level_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""UPDATE expertise_levels SET salary = %s WHERE level_id = %s;""", (salary, level_id, ))
            self.conn.commit()
