from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(host='sql11.freesqldatabase.com',
                             user='sql11189246',
                             password='FFUZryMbY1',
                             db='sql11189246',
                             charset='utf8mb4',
                             autocommit = True,
                             cursorclass = pymysql.cursors.DictCursor)

cursor = connection.cursor()

@get("/admin")
def admin_portal():
	return template("pages/admin.html")

@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')

# store page
@get('/categories')
def list_Categories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, name from categories"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps ({"STATUS": "SUCCESS", "CATEGORIES": result, "CODE":"200"})

    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})


@get('/category/<id>/products')
def get_Products(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from products WHERE category = {0}".format(str(id))
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE":"200"})
    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})

# admin page
@post('/category')
def create_Category():
    try:
        with connection.cursor() as cursor:
            name = request.POST.get("name")
            sql = "INSERT INTO categories VALUES (0,'{0}')".format(name)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "MSG": result, "CODE": "200"})
    except Exception as e:
        print (repr(e))
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})

@delete('/category/<id>')
def delete_Category(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM categories WHERE id = {0}".format(id)
            cursor.execute(sql)
            sql2 = "DELETE FROM products WHERE category = {0}".format(id)
            cursor.execute(sql2)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "MSG": result, "CODE": "200"})
    except pymysql.err.IntegrityError as e:
        print (repr(e))
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})


@post('/product')
def add_Product():
    try:
        with connection.cursor() as cursor:
            t = request.POST.get("title")
            d = request.POST.get("descr")
            p = request.POST.get("price")
            i = request.POST.get("img_url")
            c = request.POST.get("category")
            f = request.POST.get("favorite")
            if f is 'on':
                f = True;
            else:
                f = False;
            sql = "INSERT INTO products VALUES (id,'{0}','{1}',{2},'{3}','{4}',{5})".format(t,d,p,i,c,f)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "MSG": result, "CODE": "200"})
    except Exception as e:
        with connection.cursor() as cursor:
            t = request.POST.get("title")
            d = request.POST.get("descr")
            p = request.POST.get("price")
            i = request.POST.get("img_url")
            c = request.POST.get("category")
            f = request.POST.get("favorite")
            if f is 'on':
                f = True;
            else:
                f = False;
            sql = "UPDATE products SET descr = '{0}', price = {1}, img_url = '{2}', category = '{3}', favorite = {4} WHERE title = '{5}'".format(d, p, i, c, f, t)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "MSG": result, "CODE": "200"})

@get('/products')
def list_Products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from products"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps ({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE":"200"})
    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})

@get('/product/<id>')
def get_Products(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from products WHERE id = {0}".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE":"200"})
    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})


@delete('/product/<id>')
def delete_Product(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM products WHERE id = {0}".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE": "200"})
    except pymysql.err.IntegrityError as e:
        print (repr(e))
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})


#run(host='0.0.0.0', port=argv[1])
run(host='127.0.0.1', port=7000)
