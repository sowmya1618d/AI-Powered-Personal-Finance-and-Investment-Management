"""
Database initialization script
Run this script to create all tables in MySQL database
"""
import sys
sys.path.append('..')

from database.connection import init_db, engine
from database.models import Base


def main():
    """Initialize database tables"""
    print("🔄 Creating database tables...")
    
    try:
        # Create all tables
        init_db()
        print("✅ Database initialization completed successfully!")
        print(f"📊 Database: {engine.url}")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
