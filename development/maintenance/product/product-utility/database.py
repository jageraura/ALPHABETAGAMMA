import sqlite3

conn = sqlite3.connect('product.db')  # Database name
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE items (
    itemid INTEGER PRIMARY KEY,
    itemname TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    image1 TEXT,
    image2 TEXT,
    image3 TEXT,
    category1 TEXT,
    category2 TEXT,
    category3 TEXT
)
''')

# Insert 22 sample data items
sample_items = [
    ('Item 1', 9.99, 'Description 1', 'image1a.jpg', 'image1b.jpg', 'image1c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 2', 19.99, 'Description 2', 'image2a.jpg', 'image2b.jpg', 'image2c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 3', 29.99, 'Description 3', 'image3a.jpg', 'image3b.jpg', 'image3c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 4', 39.99, 'Description 4', 'image4a.jpg', 'image4b.jpg', 'image4c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 5', 49.99, 'Description 5', 'image5a.jpg', 'image5b.jpg', 'image5c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 6', 59.99, 'Description 6', 'image6a.jpg', 'image6b.jpg', 'image6c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 7', 69.99, 'Description 7', 'image7a.jpg', 'image7b.jpg', 'image7c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 8', 79.99, 'Description 8', 'image8a.jpg', 'image8b.jpg', 'image8c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 9', 89.99, 'Description 9', 'image9a.jpg', 'image9b.jpg', 'image9c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 10', 99.99, 'Description 10', 'image10a.jpg', 'image10b.jpg', 'image10c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 11', 109.99, 'Description 11', 'image11a.jpg', 'image11b.jpg', 'image11c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 12', 119.99, 'Description 12', 'image12a.jpg', 'image12b.jpg', 'image12c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 13', 129.99, 'Description 13', 'image13a.jpg', 'image13b.jpg', 'image13c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 14', 139.99, 'Description 14', 'image14a.jpg', 'image14b.jpg', 'image14c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 15', 149.99, 'Description 15', 'image15a.jpg', 'image15b.jpg', 'image15c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 16', 159.99, 'Description 16', 'image16a.jpg', 'image16b.jpg', 'image16c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 17', 169.99, 'Description 17', 'image17a.jpg', 'image17b.jpg', 'image17c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 18', 179.99, 'Description 18', 'image18a.jpg', 'image18b.jpg', 'image18c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 19', 189.99, 'Description 19', 'image19a.jpg', 'image19b.jpg', 'image19c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 20', 199.99, 'Description 20', 'image20a.jpg', 'image20b.jpg', 'image20c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 21', 209.99, 'Description 21', 'image21a.jpg', 'image21b.jpg', 'image21c.jpg', 'Category A', 'Category B', 'Category C'),
    ('Item 22', 219.99, 'Description 22', 'image22a.jpg', 'image22b.jpg', 'image22c.jpg', 'Category A', 'Category B', 'Category C')
]

c.executemany('''
INSERT INTO items (itemname, price, description, image1, image2, image3, category1, category2, category3)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', sample_items)

conn.commit()
conn.close()
