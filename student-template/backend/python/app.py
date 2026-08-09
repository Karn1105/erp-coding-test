from flask import Flask, jsonify
import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Configure database connection pool using os.getenv('DATABASE_URL')
# Time Complexity: O(1) for initialization
# Space Complexity: O(K) where K is the pool size (reused connections)
DATABASE_URL = os.getenv('DATABASE_URL')
db_pool = None

if DATABASE_URL:
    try:
        # Initialize a small connection pool to avoid overhead on every request
        db_pool = SimpleConnectionPool(1, 10, DATABASE_URL)
    except Exception as e:
        print(f"Error connecting to database: {e}")

@app.route('/api/inventory/alerts', methods=['GET'])
def get_alerts():
    """
    1. Connect to the database via connection pool.
    2. Query 'inventory' table where quantity <= reorder_level.
    3. Return JSON list of products efficiently.
    """
    if not db_pool:
        return jsonify({"error": "Database connection not configured"}), 500

    conn = None
    try:
        # Get a connection from the pool - O(1) time
        conn = db_pool.getconn()
        
        # Use RealDictCursor to fetch rows directly as dictionaries
        # Time Complexity: O(N) where N is the number of low-stock items returned
        # Space Complexity: O(N) to store the result set in memory before JSON serialization
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
        if conn and db_pool:
            # Return the connection back to the pool
            db_pool.putconn(conn)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
