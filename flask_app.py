from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'Nyxotique.mysql.pythonanywhere-services.com',
    'user': 'Nyxotique',  # Update with your MySQL username
    'password': 'blackTAIL3',  # Update with your MySQL password
    'database': 'Nyxotique$default'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_postcode_matches', methods=['POST'])
def get_postcode_matches():
    postcode_query = request.form.get('postcode')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = """
    SELECT customer_id, postcode, street_name, house_name, house_number
    FROM freshbins
    WHERE postcode LIKE %s
    """
    params = [f'%{postcode_query}%']
    cursor.execute(query, params)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    matches = [{'id': row[0], 'postcode': row[1], 'street': row[2], 'house': row[3], 'number': row[4]} for row in results]

    return jsonify({'matches': matches})

@app.route('/get_address_data', methods=['POST'])
def get_address_data():
    selected_id = request.form.get('id')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = """
    SELECT customer_id, postcode, street_name, house_name, house_number, bin, date
    FROM freshbins
    WHERE customer_id = %s
    """
    params = [selected_id]
    cursor.execute(query, params)
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        data = {
            'customerId': result[0],
            'postcode': result[1],
            'street': result[2],
            'house': result[3] or result[4],
            'bin': result[5],
            'date': result[6]
        }
        return jsonify(data)
    else:
        return jsonify({'error': 'No data found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
