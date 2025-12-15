"""
Database connection and query utilities.
Provides connection pooling and helper functions for database operations.
"""

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
import logging

from backend.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """
    Database connection pool manager.
    Handles PostgreSQL connections with connection pooling for better performance.
    """
    
    def __init__(self):
        """Initialize connection pool."""
        self.connection_pool: Optional[pool.SimpleConnectionPool] = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """
        Create a connection pool to the PostgreSQL database.
        Uses settings from config module.
        """
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=settings.database_url
            )
            logger.info("Database connection pool created successfully")
        except Exception as e:
            logger.error(f"Error creating connection pool: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for getting a database connection from the pool.
        Automatically returns connection to pool after use.
        
        Usage:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
        """
        connection = None
        try:
            connection = self.connection_pool.getconn()
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if connection:
                self.connection_pool.putconn(connection)
    
    def execute_query(
        self,
        query: str,
        params: Optional[tuple] = None,
        fetch_one: bool = False,
        fetch_all: bool = False
    ) -> Optional[Any]:
        """
        Execute a SQL query with optional parameters.
        
        Args:
            query: SQL query string
            params: Query parameters as tuple
            fetch_one: If True, return single row
            fetch_all: If True, return all rows
            
        Returns:
            Query results as dict or list of dicts, or None for INSERT/UPDATE
        """
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                
                if fetch_one:
                    result = cursor.fetchone()
                    return dict(result) if result else None
                elif fetch_all:
                    results = cursor.fetchall()
                    return [dict(row) for row in results]
                else:
                    conn.commit()
                    return None
    
    def execute_many(self, query: str, params_list: List[tuple]):
        """
        Execute a query multiple times with different parameters.
        Useful for batch inserts.
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, params_list)
                conn.commit()
    
    def close_pool(self):
        """Close all connections in the pool."""
        if self.connection_pool:
            self.connection_pool.closeall()
            logger.info("Database connection pool closed")


# Global database instance
db = Database()


def get_db() -> Database:
    """
    Dependency function to get database instance.
    Useful for FastAPI dependency injection.
    """
    return db
