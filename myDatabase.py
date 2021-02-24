import sqlite3
import csv
import os
import random

database_name ="ecco-site.database"
def connect(databases=database_name):

    connecting = sqlite3.connect(databases)
    connecting.row_factory = sqlite3.Row

    return connecting

def create_tables(database):

    sql = """
    
    DROP TABLE IF EXISTS jewelry;
    CREATE TABLE jewelry (
            id integer unique primary key autoincrement,
            name text,
            description text,
            category text,
            inventory integer,
            unit_cost number
            );
    """

    database.executescript(sql)
    database.commit()

def sample_data(database):

    cursor = database.cursor()
    cursor.execute("DELETE FROM jewelry")

    # read sample product data from takkies.csv
    jewelry = {}
    id = 0
    first = True  # flag
    sql = "INSERT INTO jewelry (id, name, description, category, inventory, unit_cost) VALUES (?, ?, ?, ?, ?, ?, ?)"
    with open(os.path.join(os.path.dirname(__file__), 'jewelry.csv')) as fd:
        reader = csv.DictReader(fd)
        for row in reader:
            if row['Title'] is not '':
                if first:
                    inv = 0  # inventory of first item (Ocean Blue Shirt) is zero
                    first = False
                else:
                    inv = int(random.random()*100)
                cost = int(random.random()*200) + 0.95
                description = "<p>" + row['Body (HTML)'] + "</p>"
                data = (id, row['Title'], description,  row['Tags'], inv, cost)
                cursor.execute(sql, data)
                jewelry[row['Title']] = {'id': id, 'name': row['Title'], 'description': description, 'category': row['Tags'], 'inventory': inv, 'unit_cost': cost}
                id += 1

    database.commit()

    return jewelry

if __name__=="__main__":
    database = connect(database_name)
    create_tables(database)
    sample_data(database)


def connect(databases = database_name):
	myconnecction = sqlite3.connect(databases)
	myconnecction.row_factory = sqlite3.Row

	return myconnecction


class Products:
	def __init__(self):
		self.database = connect()

	def show_all_tables(self):
		database = self.database
		mycursor= database.cursor()
		sql = """
		SELECT id,name,price FROM takkies
		
		SELECT id,name,price FROM fashion
		
		SELECT id,name, price FROM bicycles
		 
		SELECT id,name, price FROM jewelry
		ORDER BY name
		 """
		mycursor.execute(sql)
		results = mycursor.fetchall()
		return results


if __name__=="__main__":
	myProducts = Products()
	rows = myProducts.show_all_tables()
	print([dict(p) for p in rows])


def connect(databases = database_name):
    connection = sqlite3.connect(databases, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


class Product:
    def __init__(self, product_name=None, database=connect()):
        self.product_name = product_name
        self.cursor = database.cursor()

    def return_items(self):

        mycursor= self.cursor
        mycursor.execute(f"SELECT * FROM {self.product_name}")
        products = mycursor.fetchall()
        return products

    def show_all_items(self):
        mycursor= self.cursor
        sql = """
        SELECT id,name,price, description,img_url FROM takkies
        
        SELECT id,name,price, description,img_url FROM fashion
        
        SELECT id,name, price, description,img_url FROM bicycles
         
        SELECT id,name, price, description,img_url FROM jewelry
        ORDER BY name
         """
        mycursor.execute(sql)
        results = mycursor.fetchall()
        return results

class myUser:
    def __init__(self, database=connect()):
        self.cursor = database.cursor()
        self.database = database

    def add(self, firstname, surname, email, password):
        sql = f"INSERT INTO User(firstname, surname, email, password) VALUES(?,?,?,?)"
        data=(firstname, surname, email, password)
        mycursor= self.cursor
        mycursor.execute(sql, data)
        self.database.commit()
        

    def verify(self, email ,password):
        sql = f"SELECT email , password FROM User WHERE email='{email}' AND password='{password}'"
        mycursor= self.cursor
        mycursor.execute(sql)
        result = mycursor.fetchall()
        row_count =  len(result)
        print(row_count)
        if row_count == 1 :
            return True
        else:
            return False




class Review:
    def __init__(self):
        pass

    def __repr__(self):
        pass


