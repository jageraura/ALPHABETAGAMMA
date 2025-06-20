import sqlite3

def update_item(id, productname=None, price=None, description=None, image=None, image2=None, image3=None, product_type=None, product_subtype=None, product_alttype=None):
    conn = sqlite3.connect('product.db')
    c = conn.cursor()

    # Build the update query based on the provided arguments
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
        update_query = f"UPDATE items SET {', '.join(updates)} WHERE itemid = {itemid}"
        c.execute(update_query)
        conn.commit()

    conn.close()

# Example usage:
update_item(1, productname='Updated Item 1', price=12.99)
update_item(2, description='Updated Description 2', image='newimage2a.jpg')
