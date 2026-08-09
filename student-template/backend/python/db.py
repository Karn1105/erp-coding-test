import os
import psycopg2
from urllib.parse import urlparse

def get_db_connection():
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Parse the DATABASE_URL string if provided (e.g., in production)
        url = urlparse(database_url)
        return psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    else:
        # Fallback to individual environment variables (e.g., local development)
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'erpdb'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'testpass'),
            port=os.getenv('DB_PORT', 5432)
        )
