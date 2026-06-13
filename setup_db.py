import sqlite3

# 1. Connect to database (creates file if not exists)
conn = sqlite3.connect("family.db")

# 2. Create cursor (this is what you forgot)
cursor = conn.cursor()

# 3. Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS family (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    relation TEXT,
    details TEXT
)
""")

# 4. Insert data
cursor.execute("""
INSERT INTO family (name, relation, details)
VALUES ('Jeevan Baniya', 'father', 'Born 1973')
""")

# 5. Save changes
conn.commit()

# 6. Close connection
conn.close()