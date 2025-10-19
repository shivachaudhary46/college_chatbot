# ==================== import module =======================
from database import create_all_db_tables, SessionDep, engine
from necessities import insert_attendance_data

# ==================== MODEL DEFINITION ====================
from models import Attendance


# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    # Create tables
    print("Creating database tables...")
    create_all_db_tables()
    
    # Insert attendance data
    print("Inserting attendance data...")
    insert_attendance_data()
    
    print("✅ Database setup complete!")