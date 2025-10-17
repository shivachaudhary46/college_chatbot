from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # ==================== import module =======================
    from database import create_all_db_tables, SessionDep, engine
    from utilities import insert_data

    # ==================== MODEL DEFINITION ====================
    from models import User


# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    # Create tables
    print("Creating database tables...")
    create_all_db_tables()
    
    # Insert data
    print("Inserting data...")
    insert_data()
    
    print("✅ Database setup complete!")