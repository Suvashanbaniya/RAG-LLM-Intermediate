import sqlite3

# Connect to database
conn = sqlite3.connect("family.db")

# Create cursor
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS family (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    relation TEXT,
    details TEXT
)
""")

# Insert data
cursor.execute("""
INSERT INTO family (name, relation, details)
VALUES ('Dev Bahadur Baniya', 'great-grandfather', 'Founder of family lineage')
""")

cursor.execute("""
INSERT INTO family (name, relation, details)
VALUES ('Keshav Baniya', 'grandfather', 'Police Constable - Tikabhairav')
""")

cursor.execute("""
INSERT INTO family (name, relation, details)
VALUES ('Muiya Baniya', 'grandmother', 'Housewife from Lele, Lalitpur')
""")

cursor.execute("""
INSERT INTO family (name, relation, details)
VALUES ('Jeevan Baniya', 'father', 'Born 1973, Seraphat Chhampi Lalitpur')
""")

cursor.execute("""
INSERT INTO family (name, relation, details)
VALUES ('Muiya Khadka Baniya', 'mother', 'Born in Kathmandu')
""")

cursor.execute("""
INSERT INTO family (name, relation, details)
VALUES ('Suvashan Baniya', 'self', 'Student and AI developer')
""")

cursor.execute("""
INSERT INTO family (name, relation, details)
VALUES ('Suman Baniya', 'brother', 'Brother of Suvashan Baniya')
""")

# Save changes
conn.commit()

# Close database
conn.close()

print("Database created successfully!")