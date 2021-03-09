import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

database_name='ecco-site.db'
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_sqlite_db():

    conn = sqlite3.connect(database_name)
    print("database has opened")

    conn.execute("CREATE TABLE IF NOT EXISTS customers(userID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, addr TEXT, password TEXT)")
    print("customers table was created")

    conn.execute("CREATE TABLE IF NOT EXISTS products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT)")
    print("Products was created")

    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")

    print(cur.fetchall())


init_sqlite_db()


@app.route('/add-data/', methods=['POST'])
def add_new_record():
    if request.method == 'POST':
        msg = None
    try:
        post_data = request.get_json()
        name = post_data['name']
        email = post_data['email']
        addr = post_data['addr']
        password = post_data['password']

        with sqlite3.connect(database_name) as con:
            cur = con.cursor()
            con.row_factory=dict_factory
            cur.execute("INSERT INTO customers(name, email, addr, password) VALUES(?, ?, ?, ?)", (name, email, addr, password))
            con.commit()
            msg = name + " successfully added to the table."
    except Exception as e:
        con.rollback()
        msg = "Error occured in insert operation " + str(e)
    finally:
        con.close()
        return {'msg': msg}


@app.route('/show-records/', methods=['GET'])
def list_customers():
    try:
        with sqlite3.connect(database_name) as con:
            con.row_factory = dict_factory
            # con = sqlite3.connect(database_name)
            cur = con.cursor()
            cur.execute("SELECT * FROM customers")
            rows = cur.fetchall()

    except Exception as e:
        print("Something happened when getting data from db:"+str(e))
    return jsonify(rows)


@app.route('/products/', methods = ['POST'])
def insert_products():
    try:
        with sqlite3.connect(database_name) as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("INSERT INTO products(name, description, price, image) VALUES('Jump Suit', 'Jean Jump made with Jean. \n', R250, 'https://i.postimg.cc/P5g6btBQ/gqithiso.jpg')")
            cur.execute("INSERT INTO products(name, description, price, image) VALUES('Shirt', ' Summer Shirt.\n', R120,'https://i.postimg.cc/4dxV2pgM/ntando-Shirt.jpg')")
            cur.execute("INSERT INTO products(name, description, price, image) VALUES('Swimming Costume', '! price all in one Swimming costume available.\n', 'R150', 'https://i.postimg.cc/rprm0D97/andy.jpg')")
            cur.execute("INSERT INTO products(name, description, price, image) VALUES('Poloneck', 'Winter poloneck made with wool.\n', 'R150', 'https://i.postimg.cc/NjC8shQ9/mixednuts.jpg')")
            cur.execute("INSERT INTO products(name, description, price, image) VALUES('Skirt', 'Plitted skirt.\n','R100', 'https://i.postimg.cc/vHVwLyNM/pumpkinseeds.jpg')")
            cur.execute("INSERT INTO products(name, description, price, image) VALUES('Short with T-Shirt', 'This short comes with t-shirt.\n','R300', 'https://i.postimg.cc/KzfBHCp8/cashewnuts1.jpg')")
            cur.execute("INSERT INTO products(name, description, price, image) VALUES('Short Dress', 'Short, tight black dress.\n','R150', 'https://i.postimg.cc/wBZD8hgS/driedpeaches.png')")
            cur.execute("INSERT INTO products(name, description, price, image) VALUES('T-shirt', 'White T-Shirt also available in the other colors.\n','R100', 'https://i.postimg.cc/7YysWtM8/pecan.png')")
            cur.execute("INSERT INTO products(name, description, price, image) VALUES('Dress', 'Long stripped dress .\n','R120', 'https://i.postimg.cc/Pr2xR9sP/peanuts.png')")
            cur.execute("INSERT INTO products(name, description, price, image) VALUES('Leather Jacket', 'Leather Jacket vailable in 3 colors black, brown and white.\n','R180', 'https://i.postimg.cc/63vW9V6Z/cranberries.png')")
            cur.execute("INSERT INTO products(name, description, price, image) VALUES('Long Jacket', 'Long Cream Jacket.\n','R140', 'https://i.postimg.cc/Nf5MZbgD/sunflowerseeds.png')")
            con.commit()
            msg= 'Record successfully added.'
    except Exception as e:
        con.rollback()
        msg = 'Error occurred in insert operation'+str(e)
    finally:
        con.close()
    return jsonify(msg)


@app.route('/show-products/', methods= ['GET'])
def show_products():
    data = []
    try:
        with sqlite3.connect(database_name) as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute('SELECT * FROM products')
            data = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching products from the database")
    finally:
        con.close()
        return jsonify(data)


if __name__=='__main__':
    app.run(debug=True)



# @app.route("/removeProduct/", methods=["GET", "PUT", "DELETE"])
# def single_product(id):
#     conn = sqlite3.connect(database_name)
#     cursor = conn.cursor()
#     product = None
#     if request.method == "GET":
#         cursor.execute("SELECT * FROM products WHERE id=?", (id,))
#         rows = cursor.fetchall()
#         for r in rows:
#             product = r
#         if product is not None:
#             return jsonify(product), 200
#         else:
#             return "Something wrong", 404
#
#     if request.method == "PUT":
#         sql = """UPDATE product
#                 SET name=?,
#                     price=?,
#                     description=?,
#                     image1=?
#                 WHERE id=? """
#
#         post_data = request.get_json()
#         name = post_data['name']
#         price = post_data['price']
#         description = post_data['description']
#         image1 = post_data['image1']
#         updated_product = {
#             "name": name,
#             "price": price,
#             "description": description,
#             "image1": image1,
#         }
#         conn.execute(sql, (name, price, description, image1))
#         conn.commit()
#         return jsonify(updated_product)
#
#     if request.method == "DELETE":
#         sql = """ DELETE FROM product WHERE id=? """
#         conn.execute(sql, (id,))
#         conn.commit()
#         return "The product with id: {} has been deleted.".format(id), 200
#
