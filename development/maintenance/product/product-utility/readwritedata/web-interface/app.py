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
    items = query_db('SELECT itemid, itemname, price, description, image1, image2, image3, category1, category2, category3 FROM items')
    return render_template('index.html', items=items)

@app.route('/update/<int:itemid>', methods=['GET', 'POST'])
def update(itemid):
    if request.method == 'POST':
        itemname = request.form.get('itemname')
        price = request.form.get('price')
        description = request.form.get('description')
        image1 = request.form.get('image1')
        image2 = request.form.get('image2')
        image3 = request.form.get('image3')
        category1 = request.form.get('category1')
        category2 = request.form.get('category2')
        category3 = request.form.get('category3')

        updates = []
        if itemname:
            updates.append(f"itemname = '{itemname}'")
        if price:
            updates.append(f"price = {price}")
        if description:
            updates.append(f"description = '{description}'")
        if image1:
            updates.append(f"image1 = '{image1}'")
        if image2:
            updates.append(f"image2 = '{image2}'")
        if image3:
            updates.append(f"image3 = '{image3}'")
        if category1:
            updates.append(f"category1 = '{category1}'")
        if category2:
            updates.append(f"category2 = '{category2}'")
        if category3:
            updates.append(f"category3 = '{category3}'")

        if updates:
            update_query = f"UPDATE items SET {', '.join(updates)} WHERE itemid = {itemid}"
            db = get_db()
            db.execute(update_query)
            db.commit()

        return redirect(url_for('index'))

    item = query_db('SELECT * FROM items WHERE itemid = ?', [itemid], one=True)
    return render_template('update.html', item=item)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10004)
