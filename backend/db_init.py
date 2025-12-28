"""
Database initialization script.
Run this to create/reset the database.
"""
from database import init_db, engine, Base
from sqlalchemy import inspect

def check_tables():
    """Check which tables exist"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return tables

def init_database():
    """Initialize database - creates all tables"""
    print("Initializing database...")
    print(f"Database URL: {engine.url}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Check created tables
    tables = check_tables()
    print(f"\n✅ Database initialized successfully!")
    print(f"Created {len(tables)} tables:")
    for table in tables:
        print(f"  - {table}")
    
    return tables

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        print("⚠️  Resetting database...")
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("Dropped all existing tables.")
    
    init_database()
    print("\n✨ Database is ready to use!")

