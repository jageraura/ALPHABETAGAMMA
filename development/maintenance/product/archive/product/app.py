from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products LIMIT ? OFFSET ?', (per_page, offset)).fetchall()
    total_products = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    conn.close()

    return render_template('index.html', products=products, page=page, total_products=total_products, per_page=per_page)

if __name__ == '__main__':
    app.run(debug=True)
