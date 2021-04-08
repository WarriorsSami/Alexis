import mysql.connector
from faker import Faker
import random
import names


# Class Template for Data Base Manager supporting CRUD related operations
class DBHandler(object):
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="userboard"
        )
        self.cursor = self.conn.cursor()
        Faker.seed(random.randint(1, 10000000))
        self.fake = Faker()

    def insert_query(self, table_name, amount):
        if 'employee' in table_name:
            self.insert_employee(amount)
        elif 'customer' in table_name:
            self.insert_customer(amount)
        elif 'order' in table_name:
            self.insert_order(amount)
        elif 'project' in table_name:
            self.insert_project(amount)
        elif 'team' in table_name:
            self.insert_team(amount)

    def insert_employee(self, amount):
        options = ["YES", "NO"]
        query_insert = "INSERT INTO angajat (nume, prenume, adresa, email, manager, sef_proiect," \
                       "departament_id, echipa_id, data_angajare, salariu) VALUES" \
                       "(%(nume)s, %(prenume)s, %(adresa)s, %(email)s, %(manager)s, %(sef_proiect)s," \
                       "%(departament_id)s, %(echipa_id)s, %(data_angajare)s, %(salariu)s)"
        n = int(amount)

        for i in range(0, n):
            nume = names.get_last_name()
            prenume = names.get_first_name()
            adresa = self.fake.address()
            email = self.fake.email()

            departament_id = random.randint(1, 14)
            query_search = "SELECT * FROM departament WHERE id=%(dep_id)s"
            data_dep = {
                'dep_id': departament_id
            }
            self.cursor.execute(query_search, data_dep)
            result = self.cursor.fetchone()
            while result is None:
                departament_id = random.randint(1, 14)
                query_search = "SELECT * FROM departament WHERE id=%(dep_id)s"
                data_dep = {
                    'dep_id': departament_id
                }
                self.cursor.execute(query_search, data_dep)
                result = self.cursor.fetchone()

            echipa_id = random.randint(0, 400)
            query_search = "SELECT * FROM echipa WHERE id=%(team_id)s"
            data_team = {
                'team_id': echipa_id
            }
            self.cursor.execute(query_search, data_team)
            result = self.cursor.fetchone()
            while result is None:
                echipa_id = random.randint(1, 7)
                query_search = "SELECT * FROM echipa WHERE id=%(team_id)s"
                data_team = {
                    'team_id': echipa_id
                }
                self.cursor.execute(query_search, data_team)
                result = self.cursor.fetchone()

            is_manager = random.randint(0, 1)
            is_leader = random.randint(0, 1)

            if is_manager == 0:
                query_select = "SELECT * FROM angajat WHERE departament_id=%(dep_id)s AND manager=%(manager)s"
                data_manager = {
                    'dep_id': departament_id,
                    'manager': options[is_manager]
                }
                self.cursor.execute(query_select, data_manager)
                result = self.cursor.fetchone()
                if result is not None:
                    is_manager = 1

            if is_leader == 0:
                query_select = "SELECT * FROM angajat WHERE echipa_id=%(team_id)s AND sef_proiect=%(leader)s"
                data_leader = {
                    'team_id': echipa_id,
                    'leader': options[is_leader]
                }
                self.cursor.execute(query_select, data_leader)
                result = self.cursor.fetchone()
                if result is not None:
                    is_leader = 1

            salariu = str(random.randint(1000, 10000)) + ".00"
            year = random.randint(2009, 2021)
            data = str(year)
            month = random.randint(1, 12)
            if month < 10:
                data += "-0" + str(month)
            else:
                data += "-" + str(month)
            day = random.randint(1, 28)
            if day < 10:
                data += "-0" + str(day)
            else:
                data += "-" + str(day)
            # data = str(year) + "-" + str(month) + "-" + str(day)
            # print(data)

            data_employee = {
                'nume': nume,
                'prenume': prenume,
                'adresa': adresa,
                'email': email,
                'manager': options[is_manager],
                'sef_proiect': options[is_leader],
                'departament_id': departament_id,
                'echipa_id': echipa_id,
                'data_angajare': data,
                'salariu': salariu
            }
            self.cursor.execute(query_insert, data_employee)

        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def insert_customer(self, amount):
        n = int(amount)
        query = "INSERT INTO client (prenume, nume, adresa, email) VALUES (%(prenume)s, %(nume)s, %(adresa)s, " \
                "%(email)s) "

        for i in range(0, n):
            data_client = {
                'prenume': names.get_first_name(),
                'nume': names.get_last_name(),
                'adresa': self.fake.address(),
                'email': self.fake.email()
            }
            self.cursor.execute(query, data_client)

        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def insert_order(self, amount):
        query_insert = "INSERT INTO comanda (data_finalizare, client_id, produs_id, echipa_id)" \
                       "VALUES (%(data_fin)s, %(cl_id)s, %(pr_id)s, %(tm_id)s)"
        n = int(amount)

        for i in range(0, n):
            year = random.randint(2009, 2022)
            data = str(year)
            month = random.randint(1, 12)
            if month < 10:
                data += "-0" + str(month)
            else:
                data += "-" + str(month)
            day = random.randint(1, 28)
            if day < 10:
                data += "-0" + str(day)
            else:
                data += "-" + str(day)

            client = random.randint(1, 2000)
            query_search = "SELECT * FROM client WHERE client_id=%(sc_id)s LIMIT 1"
            data_client = {
                'sc_id': client
            }
            self.cursor.execute(query_search, data_client)
            result = self.cursor.fetchone()
            while result is None:
                client = random.randint(1, 2000)
                data_client = {
                    'sc_id': client
                }
                self.cursor.execute(query_search, data_client)
                result = self.cursor.fetchone()

            product = random.randint(1, 20)
            query_search = "SELECT * FROM produs WHERE id=%(sp_id)s AND disponibil=\"YES\""
            data_produs = {
                'sp_id': product
            }
            self.cursor.execute(query_search, data_produs)
            result = self.cursor.fetchone()
            while result is None:
                product = random.randint(1, 20)
                data_produs = {
                    'sp_id': product
                }
                self.cursor.execute(query_search, data_produs)
                result = self.cursor.fetchone()

            team = random.randint(1, 6000)
            query_search = "SELECT * FROM echipa WHERE id=%(st_id)s AND " \
                           "id NOT IN (SELECT echipa_id FROM proiect WHERE finalizat=\"WORKING\")"
            data_team = {
                'st_id': team
            }
            self.cursor.execute(query_search, data_team)
            result = self.cursor.fetchone()
            while result is None:
                team = random.randint(1, 5000)
                data_team = {
                    'st_id': team
                }
                self.cursor.execute(query_search, data_team)
                result = self.cursor.fetchone()

            data_order = {
                'data_fin': data,
                'cl_id': client,
                'pr_id': product,
                'tm_id': team
            }
            self.cursor.execute(query_insert, data_order)

        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def insert_project(self, amount):
        it_list = ['Java', 'Python', 'Programming', 'React JS', 'Socket', 'Django',
                   'C++', 'C#', 'Embedded Systems', 'Java Servlets', 'Java Applets', 'Speech Recognizer',
                   'AI Dev', 'Machine Learning', 'Functional Programming', 'Transfer Protocol',
                   'Regex Editor', 'REST API', 'Login App', 'CRUD', 'GUI Swing', 'Bootstrap',
                   'TailWindCss', 'JDBC', 'DB Manager', 'Flask Tech', 'Angular JS', 'JQuery',
                   'Ajax', 'IDE', 'Game Engine', 'Chat Log', 'HTML Editor', 'Numpy', 'Faker Generator']

        query_insert = "INSERT INTO proiect (tip, deadline, echipa_id, finalizat) " \
                       "VALUES (%(tip)s, %(data)s, %(team)s, %(state)s)"
        options = ["WORKING", "DONE"]
        n = int(amount)

        for i in range(0, n):
            state = random.randint(0, 1)
            team = random.randint(1, 5000)
            query_select = "SELECT * FROM echipa WHERE id=%(team_id)s LIMIT 1"
            if state == 0:
                query_select = "SELECT * FROM echipa WHERE id=%(team_id)s AND id NOT IN" \
                               "(SELECT echipa_id FROM proiect WHERE finalizat=\"WORKING\") LIMIT 1"

            data_team = {
                'team_id': team
            }
            self.cursor.execute(query_select, data_team)
            result = self.cursor.fetchone()
            while result is None:
                team = random.randint(1, 5000)
                data_team = {
                    'team_id': team
                }
                self.cursor.execute(query_select, data_team)
                result = self.cursor.fetchone()

            data_project = {
                'tip': self.fake.sentence(nb_words=2, ext_word_list=it_list),
                'data': self.fake.date_this_decade(),
                'team': team,
                'state': options[state]
            }
            self.cursor.execute(query_insert, data_project)

        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def insert_team(self, amount):
        query_insert = "INSERT INTO echipa (denumire) VALUES (%(name)s)"
        n = int(amount)

        for i in range(0, n):
            data_team = {
                'name': self.fake.company()
            }
            self.cursor.execute(query_insert, data_team)

        self.conn.commit()
        self.cursor.close()
        self.conn.close()
