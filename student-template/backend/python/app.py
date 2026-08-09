from flask import Flask, jsonify
from db import get_db_connection
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

@app.route('/api/inventory/alerts', methods=['GET'])
def get_alerts():
    """
    1. Connect to the database using get_db_connection().
    2. Query 'inventory' table where quantity <= reorder_level.
    3. Return JSON list of products.
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT id, name, quantity, reorder_level, sku 
                FROM inventory 
                WHERE quantity <= reorder_level;
            """
            cursor.execute(query)
            alerts = cursor.fetchall()
            
        return jsonify(alerts), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
