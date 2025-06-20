from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'product.db'  # Your existing database

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    items = query_db('SELECT id, productname, price, description, image, image2, image3, product_type, product_subtype, product_alttype FROM products')
    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10004)
