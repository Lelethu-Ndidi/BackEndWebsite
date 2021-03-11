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

    conn.execute("CREATE TABLE IF NOT EXISTS products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, rate TEXT, price TEXT, image1 TEXT, image2 TEXT)")
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
        msg = "Error occurred in insert operation " + str(e)
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
    with sqlite3.connect(database_name) as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("INSERT INTO products(name, description, rate, price, image1,image2) VALUES('Jump Suit', 'Jean Jump made with Jean. \n','rate: 5/5', R250, 'https://i.postimg.cc/P5g6btBQ/gqithiso.jpg','https://i.postimg.cc/pdk4RZwZ/simkiniwe.jpg')")
        cur.execute("INSERT INTO products(name, description, rate, price, image1,image2) VALUES('Shirt', ' Summer Shirt.\n','rate: 5/5', R120,'https://i.postimg.cc/4dxV2pgM/ntando-Shirt.jpg','https://i.postimg.cc/1zY37jrB/ntiro2-Shirt.jpg')")
        cur.execute("INSERT INTO products(name, description, rate, price, image1,image2) VALUES('Swimming Costume', '! price all in one Swimming costume available.\n','rate: 5/5', 'R150', 'https://i.postimg.cc/rprm0D97/andy.jpg','https://i.postimg.cc/QM9BQ4j4/andyMjk.jpg')")
        cur.execute("INSERT INTO products(name, description, rate, price, image1,image2) VALUES('Poloneck', 'Winter poloneck made with wool.\n', 'rate: 5/5','R150', 'https://i.postimg.cc/3RGh9pQR/lucifer.jpg','https://i.postimg.cc/8ccypgRk/Wara.jpg')")
        cur.execute("INSERT INTO products(name, description, rate, price, image1,image2) VALUES('Skirt', 'Pleated skirt.\n','rate: 5/5','R100', 'https://i.postimg.cc/Wz8xfLRm/zezzy.jpg','https://i.postimg.cc/J0k4Lr8L/zezethu.jpg')")
        cur.execute("INSERT INTO products(name, description, rate, price, image1,image2) VALUES('Short with T-Shirt', 'This short comes with t-shirt.\n','rate: 5/5','R300', 'https://i.postimg.cc/CKfwMD4F/tyaliti-Mr.jpg','https://i.postimg.cc/gkkdX1Kt/mr-Tyaliti.jpg')")
        cur.execute("INSERT INTO products(name, description, rate, price, image1,image2) VALUES('Short Dress', 'Short, tight black dress.\n',rate: 5/5,'R150', 'https://i.postimg.cc/HWSYB0jb/sinyonyo.jpg' ,'https://i.postimg.cc/cL3dxVhc/sinokuhle.jpg')")
        cur.execute("INSERT INTO products(name, description, rate, price, image1,image2) VALUES('T-shirt', 'White T-Shirt also available in the other colors.\n','rate: 5/5','R100', 'https://i.postimg.cc/0j9Ls4Qc/lumkileM.jpg', 'https://i.postimg.cc/BQ6VBH1L/lulu.jpg')")
        cur.execute("INSERT INTO products(name, description, rate, price, image1,image2) VALUES('Dress', 'Long stripped dress .\n','rate: 5/5','R120', 'https://i.postimg.cc/DZMn54FM/jazz.jpg','https://i.postimg.cc/JzQKwhJV/jazznella.jpg')")
        cur.execute("INSERT INTO products(name, description, rate, price, image1,image2) VALUES('Leather Jacket', 'Leather Jacket available in 3 colors black, brown and white.\n','rate: 5/5','R180', 'https://i.postimg.cc/rzXqrpyB/ntandoJacket.jpg','https://i.postimg.cc/sDhXDkDF/ntiro-Jacket.jpg')")
        cur.execute("INSERT INTO products(name, description, rate, price, image1,image2) VALUES('Long Jacket', 'Long Cream Jacket.\n','rate: 5/5','R300', 'https://i.postimg.cc/m2VgC2wm/zeni.jpg','https://i.postimg.cc/kGphPSCj/zeeMdee.jpg')")
        con.commit()
insert_products()


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
#                     image1=?,
#                     image2=?
#                 WHERE id=? """
#
#         post_data = request.get_json()
#         name = post_data['name']
#         price = post_data['price']
#         description = post_data['description']
#         image1 = post_data['image1']
#         image2 = post_data['image2']
#         updated_product = {
#             "name": name,
#             "price": price,
#             "description": description,
#             "image1": image1,
#             "image2 = image2"
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
