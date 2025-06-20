from flask import Flask, render_template, request, g, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'product.db'

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

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        productname = request.form.get('productname')
        price = request.form.get('price')
        description = request.form.get('description')
        image = request.form.get('image')
        image2 = request.form.get('image2')
        image3 = request.form.get('image3')
        product_type = request.form.get('product_type')
        product_subtype = request.form.get('product_subtype')
        product_alttype = request.form.get('product_alttype')

        updates = []
        if productname:
            updates.append(f"productname = '{productname}'")
        if price:
            updates.append(f"price = {price}")
        if description:
            updates.append(f"description = '{description}'")
        if image:
            updates.append(f"image = '{image}'")
        if image2:
            updates.append(f"image2 = '{image2}'")
        if image3:
            updates.append(f"image3 = '{image3}'")
        if product_type:
            updates.append(f"product_type = '{product_type}'")
        if product_subtype:
            updates.append(f"product_subtype = '{product_subtype}'")
        if product_alttype:
            updates.append(f"product_alttype = '{product_alttype}'")

        if updates:
            update_query = f"UPDATE products SET {', '.join(updates)} WHERE id = {id}"
            db = get_db()
            db.execute(update_query)
            db.commit()

        return redirect(url_for('index'))

    item = query_db('SELECT * FROM products WHERE id = ?', [id], one=True)
    return render_template('update.html', item=item)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10004)
