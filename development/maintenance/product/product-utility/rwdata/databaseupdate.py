import sqlite3

def update_item(itemid, itemname=None, price=None, description=None, image1=None, image2=None, image3=None, category1=None, category2=None, category3=None):
    conn = sqlite3.connect('product.db')
    c = conn.cursor()

    # Build the update query based on the provided arguments
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
        c.execute(update_query)
        conn.commit()

    conn.close()

# Example usage:
update_item(1, itemname='Updated Item 1', price=12.99)
update_item(2, description='Updated Description 2', image1='newimage2a.jpg')
