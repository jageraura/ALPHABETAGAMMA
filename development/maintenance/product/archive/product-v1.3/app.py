from flask import Flask, render_template, request, redirect, url_for, g, session as flask_session, jsonify
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Database configuration
DATABASE_USERS = 'users.db'
DATABASE_SESSIONS = 'sessions.db'
DATABASE_PRODUCTS = 'products.db'
DATABASE_COMPLETED_ORDERS = 'completed_orders.db'  # Added this line

# Functions to connect to the databases
def get_db_connection(db_name=DATABASE_PRODUCTS):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def get_db(db_name):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_name)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Function to update the session counter
def update_session_counter():
    db = get_db(DATABASE_SESSIONS)
    cursor = db.execute('SELECT value FROM session_counter WHERE id = 1')
    current_value = cursor.fetchone()[0]
    new_value = current_value + 1
    db.execute('UPDATE session_counter SET value = ? WHERE id = 1', (new_value,))
    db.commit()
    return new_value

# Routes
@app.route('/')
def index():
    if 'unique_id' not in flask_session:
        flask_session['unique_id'] = random.randint(100000, 999999)  # Assign a unique random number
    flask_session['last_visit'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_id = update_session_counter()
    store_session_data(flask_session['unique_id'], flask_session['last_visit'])

    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products LIMIT ? OFFSET ?', (per_page, offset)).fetchall()
    total_products = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    conn.close()

    return render_template('index.html', products=products, page=page, total_products=total_products, per_page=per_page)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    session_id = flask_session['unique_id']

    conn = get_db_connection()
    conn.execute('INSERT INTO cart (product_id, session_id, quantity) VALUES (?, ?, ?)', (product_id, session_id, quantity))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Product added to cart!'})

@app.route('/cart')
def cart():
    session_id = flask_session['unique_id']

    conn = get_db_connection()
    cart_items = conn.execute('''
        SELECT p.productname, p.price, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.session_id = ?
    ''', (session_id,)).fetchall()
    conn.close()

    return render_template('cart.html', cart_items=cart_items)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        session_id = flask_session['unique_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        delivery_address = request.form['delivery_address']
        billing_address = request.form['billing_address']
        credit_card_number = request.form['credit_card_number']
        expiration_month = request.form['expiration_month']
        expiration_year = request.form['expiration_year']
        cvv_number = request.form['cvv_number']
        expiration_date = f"{expiration_month}/{expiration_year}"
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO orders (
                session_id, first_name, last_name, email, phone, 
                delivery_address, billing_address, 
                credit_card_number, expiration_date, cvv_number, order_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, first_name, last_name, email, phone, delivery_address, billing_address, credit_card_number, expiration_date, cvv_number, order_date))
        order_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

        cart_items = conn.execute('SELECT * FROM cart WHERE session_id = ?', (session_id,)).fetchall()
        for item in cart_items:
            conn.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)', (order_id, item['product_id'], item['quantity']))

        conn.execute('DELETE FROM cart WHERE session_id = ?', (session_id,))
        conn.commit()
        conn.close()

        # Store completed order in completed_orders.db
        completed_conn = get_db_connection(DATABASE_COMPLETED_ORDERS)
        completed_conn.execute('''
            INSERT INTO orders (
                session_id, first_name, last_name, email, phone, 
                delivery_address, billing_address, 
                credit_card_number, expiration_date, cvv_number, order_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, first_name, last_name, email, phone, delivery_address, billing_address, credit_card_number, expiration_date, cvv_number, order_date))
        completed_order_id = completed_conn.execute('SELECT last_insert_rowid()').fetchone()[0]

        for item in cart_items:
            completed_conn.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)', (completed_order_id, item['product_id'], item['quantity']))

        completed_conn.commit()
        completed_conn.close()

        return redirect(url_for('order_confirmation', order_id=completed_order_id))

    return render_template('checkout.html')

@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    # Retrieve order details from completed_orders.db
    completed_conn = get_db_connection(DATABASE_COMPLETED_ORDERS)
    order = completed_conn.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,)).fetchone()
    order_items = completed_conn.execute('''
        SELECT p.productname, p.price, oi.quantity
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    ''', (order_id,)).fetchall()
    completed_conn.close()

    return render_template('order_confirmation.html', order=order, order_items=order_items)

@app.route('/cart_count')
def cart_count():
    session_id = flask_session['unique_id']

    conn = get_db_connection()
    count = conn.execute('SELECT SUM(quantity) FROM cart WHERE session_id = ?', (session_id,)).fetchone()[0]
    conn.close()

    return jsonify({'count': count or 0})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        session_value = request.form['session_value']
        flask_session['username'] = username  # Store the username in session
        db = get_db(DATABASE_USERS)
        db.execute('INSERT INTO users (username, email, session_value) VALUES (?, ?, ?)', (username, email, session_value))
        db.commit()
        return redirect(url_for('index'))  # Redirect to index page after registration
    return render_template('register.html')

@app.route('/users')
def users():
    db = get_db(DATABASE_USERS)
    cursor = db.execute('SELECT * FROM users')
    users_data = cursor.fetchall()
    return render_template('user.html', users=users_data)

@app.route('/sessions')
def sessions():
    db = get_db(DATABASE_SESSIONS)
    cursor = db.execute('SELECT * FROM sessions')
    sessions_data = cursor.fetchall()
    return render_template('session.html', sessions=sessions_data)

@app.route('/products')
def products():
    db = get_db(DATABASE_PRODUCTS)
    cursor = db.execute('SELECT * FROM products')
    products_data = cursor.fetchall()
    return render_template('product.html', products=products_data)

def store_session_data(session_value, last_visit):
    db = get_db(DATABASE_SESSIONS)
    db.execute('INSERT INTO sessions (sessions, datetime) VALUES (?, ?)', (session_value, last_visit))
    db.commit()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10003)
