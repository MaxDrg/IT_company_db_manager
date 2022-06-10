from database import Database
from temporary import Connection

conn = Connection().get()
db = Database(conn['login'], conn['password'])

class Rules:
    def age(self, age: int):
        if age < 18:
            return True
        else:
            return False

    def min_cost(self, cost: int):
        if cost < 20000:
            return True
        else:
            return False

    def min_averange(self, level: str, salary: int):
        summ = salary

        for other_level in db.get_other_levels(level):
            summ += other_level[0] 
        if summ > 2500:
            return False
        else:
            return True
    
    def max_salary(self, salary: int):
        if salary < 10000:
            return True
        else:
            return False

    def team_lead(self, position: str, employee_name: str):
        level = db.get_employee_level(employee_name)[0]
        if position == 'Team lead' and level == 'Junior':
            return True
        else:
            return False

    def check_salarys(self, level: str, salary: int):
        if level == 'Junior':
            return False
        elif level == 'Middle':
            if salary > db.get_senior_salary()[0]:
                return True
        elif level == 'Senior':
            for other_salary in db.get_other_levels():
                if other_salary < salary:
                    return True
        else:
            return False
