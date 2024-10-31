from flask import Flask, jsonify, request, make_response
import csv
import sqlite3
import datetime
from io import StringIO

app = Flask(__name__)

# Opret forbindelse til SQLite-database
def get_db_connection():
    conn = sqlite3.connect('payments.db')
    conn.row_factory = sqlite3.Row
    return conn

# Opret en ny betaling
@app.route('/payments', methods=['POST'])
def create_payment():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO payments (amount, currency, payment_method, order_id, user_id, status, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (data['amount'], data['currency'], data['payment_method'], data['order_id'], data['user_id'], 'modtaget', datetime.datetime.now()))
    conn.commit()
    conn.close()
    return jsonify({"message": "Payment created successfully"}), 201

# Hent alle betalinger
@app.route('/payments', methods=['GET'])
def get_payments():
    conn = get_db_connection()
    payments = conn.execute('SELECT * FROM payments').fetchall()
    conn.close()
    return jsonify([dict(payment) for payment in payments])

# Hent specifik betaling
@app.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    conn = get_db_connection()
    payment = conn.execute('SELECT * FROM payments WHERE payment_id = ?', (payment_id,)).fetchone()
    conn.close()
    if payment is None:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify(dict(payment))

# Slet en specifik betaling
@app.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM payments WHERE payment_id = ?', (payment_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Payment deleted successfully"}), 204

# Eksporter til CSV
@app.route('/payments/csv', methods=['GET'])
def export_payments_csv():
    conn = get_db_connection()
    payments = conn.execute('SELECT * FROM payments').fetchall()
    conn.close()
    
    # Use StringIO to create a file-like object
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Payment ID', 'Amount', 'Currency', 'Payment Method', 'Order ID', 'User ID', 'Status', 'Timestamp'])
    for payment in payments:
        writer.writerow(payment)
    
    # Get the CSV data from StringIO object
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=payments.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
