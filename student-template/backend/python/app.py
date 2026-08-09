from flask import Flask, jsonify
import os
# 1. Import your database connector here
from db import get_db_connection

app = Flask(__name__)

# Note: Your db.py handles configuration via environment variables automatically,
# but you can also configure things here if needed.

@app.route('/api/inventory/alerts', methods=['GET'])
def get_alerts():
    """
    1. Connect to the database.
    2. Query 'inventory' table where quantity <= reorder_level.
    3. Return JSON list of products.
    """
    conn = None
    cursor = None
    try:
        # 1. Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 2. Query 'inventory' table where quantity <= reorder_level
        query = """
            SELECT id, product_name, quantity, reorder_level 
            FROM inventory 
            WHERE quantity <= reorder_level;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Convert database rows into a list of dictionaries
        alerts = []
        for row in rows:
            alerts.append({
                "id": row[0],
                "product_name": row[1],
                "quantity": row[2],
                "reorder_level": row[3]
            })
            
        # 3. Return JSON list of products
        return jsonify(alerts), 200

    except Exception as e:
        # Handle database errors gracefully
        return jsonify({"error": str(e)}), 500
        
    finally:
        # Ensure database resources are always closed
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
