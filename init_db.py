import sqlite3

# Opret forbindelse til SQLite-database
conn = sqlite3.connect('payments.db')

# Opret tabel til betalinger
conn.execute('''
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    order_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Database and table created successfully!")
