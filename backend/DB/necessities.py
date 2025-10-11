
from database import engine
from models import Attendance
from sqlmodel import Session 


# ==================== INSERT ATTENDANCE DATA ====================
def insert_attendance_data():
    """Insert all student attendance records"""
    
    # Attendance data for all students
    attendance_data = [
        {
            "student_name": "Akrisha Khanal",
            "username": "akrishakhanal",
            "day_1": "P", "day_2": "P", "day_3": "P", "day_4": "A", "day_5": "P",
            "day_6": "P", "day_7": "P", "day_8": "P", "day_9": "P", "day_10": "P",
            "day_11": "A", "day_12": "P", "day_13": "P", "day_14": "P", "day_15": "P",
            "day_16": "P", "day_17": "P", "day_18": "P", "day_19": "A", "day_20": "P",
            "day_21": "P", "day_22": "P", "day_23": "P", "day_24": "P", "day_25": "P",
            "day_26": "P", "day_27": "P", "day_28": "A", "day_29": "P", "day_30": "P",
            "day_31": "P", "total": 27, "percentage": 87
        },
        {
            "student_name": "Anuprash Subedi",
            "username": "anuprashsubedi",
            "day_1": "P", "day_2": "P", "day_3": "A", "day_4": "P", "day_5": "P",
            "day_6": "P", "day_7": "P", "day_8": "P", "day_9": "P", "day_10": "P",
            "day_11": "P", "day_12": "P", "day_13": "P", "day_14": "A", "day_15": "P",
            "day_16": "P", "day_17": "P", "day_18": "P", "day_19": "P", "day_20": "P",
            "day_21": "A", "day_22": "P", "day_23": "P", "day_24": "P", "day_25": "P",
            "day_26": "P", "day_27": "P", "day_28": "P", "day_29": "P", "day_30": "P",
            "day_31": "P", "total": 28, "percentage": 90
        },
        {
            "student_name": "Ashwin Phuyal",
            "username": "ashwinphuyal",
            "day_1": "P", "day_2": "P", "day_3": "P", "day_4": "P", "day_5": "P",
            "day_6": "A", "day_7": "P", "day_8": "P", "day_9": "P", "day_10": "P",
            "day_11": "P", "day_12": "P", "day_13": "A", "day_14": "P", "day_15": "P",
            "day_16": "P", "day_17": "P", "day_18": "P", "day_19": "P", "day_20": "P",
            "day_21": "P", "day_22": "P", "day_23": "P", "day_24": "P", "day_25": "A",
            "day_26": "P", "day_27": "P", "day_28": "P", "day_29": "P", "day_30": "P",
            "day_31": "P", "total": 28, "percentage": 90
        },
        {
            "student_name": "Jenisha Adhikari",
            "username": "jenishaadhikari",
            "day_1": "P", "day_2": "A", "day_3": "P", "day_4": "P", "day_5": "P",
            "day_6": "P", "day_7": "P", "day_8": "P", "day_9": "P", "day_10": "P",
            "day_11": "P", "day_12": "P", "day_13": "P", "day_14": "P", "day_15": "P",
            "day_16": "A", "day_17": "P", "day_18": "P", "day_19": "P", "day_20": "P",
            "day_21": "P", "day_22": "P", "day_23": "P", "day_24": "P", "day_25": "P",
            "day_26": "P", "day_27": "A", "day_28": "P", "day_29": "A", "day_30": "P",
            "day_31": "P", "total": 27, "percentage": 87
        },
        {
            "student_name": "Grishma Bhatt",
            "username": "grishmabhatt",
            "day_1": "P", "day_2": "P", "day_3": "P", "day_4": "P", "day_5": "P",
            "day_6": "P", "day_7": "P", "day_8": "A", "day_9": "P", "day_10": "P",
            "day_11": "P", "day_12": "P", "day_13": "P", "day_14": "P", "day_15": "P",
            "day_16": "P", "day_17": "P", "day_18": "A", "day_19": "P", "day_20": "P",
            "day_21": "P", "day_22": "P", "day_23": "P", "day_24": "P", "day_25": "P",
            "day_26": "P", "day_27": "P", "day_28": "P", "day_29": "P", "day_30": "A",
            "day_31": "P", "total": 28, "percentage": 90
        },
        {
            "student_name": "Chandan Sharma Thakur",
            "day_1": "P", "day_2": "P", "day_3": "P", "day_4": "P", "day_5": "A",
            "day_6": "P", "day_7": "P", "day_8": "P", "day_9": "P", "day_10": "P",
            "day_11": "P", "day_12": "A", "day_13": "P", "day_14": "P", "day_15": "P",
            "day_16": "P", "day_17": "P", "day_18": "P", "day_19": "P", "day_20": "P",
            "day_21": "P", "day_22": "P", "day_23": "A", "day_24": "P", "day_25": "P",
            "day_26": "P", "day_27": "P", "day_28": "P", "day_29": "P", "day_30": "P",
            "day_31": "P", "total": 28, "percentage": 90
        },
        {
            "student_name": "Bisham Dhakal",
            "day_1": "P", "day_2": "P", "day_3": "P", "day_4": "P", "day_5": "P",
            "day_6": "P", "day_7": "A", "day_8": "P", "day_9": "P", "day_10": "A",
            "day_11": "P", "day_12": "P", "day_13": "P", "day_14": "P", "day_15": "P",
            "day_16": "P", "day_17": "P", "day_18": "P", "day_19": "P", "day_20": "P",
            "day_21": "P", "day_22": "A", "day_23": "P", "day_24": "P", "day_25": "P",
            "day_26": "P", "day_27": "P", "day_28": "P", "day_29": "P", "day_30": "P",
            "day_31": "P", "total": 28, "percentage": 90
        },
        {
            "student_name": "Khemant Raj Adhikari",
            "day_1": "P", "day_2": "P", "day_3": "P", "day_4": "P", "day_5": "P",
            "day_6": "P", "day_7": "P", "day_8": "P", "day_9": "P", "day_10": "P",
            "day_11": "P", "day_12": "P", "day_13": "P", "day_14": "P", "day_15": "A",
            "day_16": "P", "day_17": "P", "day_18": "P", "day_19": "A", "day_20": "P",
            "day_21": "P", "day_22": "P", "day_23": "A", "day_24": "P", "day_25": "P",
            "day_26": "P", "day_27": "P", "day_28": "P", "day_29": "A", "day_30": "P",
            "day_31": "P", "total": 27, "percentage": 87
        },
        {
            "student_name": "Rohan Paudel",
            "day_1": "P", "day_2": "A", "day_3": "P", "day_4": "P", "day_5": "P",
            "day_6": "P", "day_7": "P", "day_8": "P", "day_9": "P", "day_10": "P",
            "day_11": "P", "day_12": "P", "day_13": "P", "day_14": "P", "day_15": "P",
            "day_16": "P", "day_17": "A", "day_18": "P", "day_19": "P", "day_20": "P",
            "day_21": "P", "day_22": "P", "day_23": "P", "day_24": "P", "day_25": "P",
            "day_26": "A", "day_27": "P", "day_28": "P", "day_29": "P", "day_30": "P",
            "day_31": "P", "total": 28, "percentage": 90
        },
        {
            "student_name": "Jonash Chautahat",
            "day_1": "P", "day_2": "P", "day_3": "P", "day_4": "A", "day_5": "P",
            "day_6": "P", "day_7": "P", "day_8": "P", "day_9": "A", "day_10": "P",
            "day_11": "P", "day_12": "P", "day_13": "A", "day_14": "P", "day_15": "A",
            "day_16": "P", "day_17": "P", "day_18": "P", "day_19": "P", "day_20": "P",
            "day_21": "P", "day_22": "P", "day_23": "P", "day_24": "A", "day_25": "P",
            "day_26": "P", "day_27": "P", "day_28": "P", "day_29": "P", "day_30": "P",
            "day_31": "P", "total": 26, "percentage": 84
        },
        {
            "student_name": "Karan K.C",
            "day_1": "A", "day_2": "P", "day_3": "P", "day_4": "P", "day_5": "P",
            "day_6": "P", "day_7": "P", "day_8": "P", "day_9": "P", "day_10": "P",
            "day_11": "P", "day_12": "P", "day_13": "P", "day_14": "P", "day_15": "P",
            "day_16": "P", "day_17": "P", "day_18": "P", "day_19": "P", "day_20": "A",
            "day_21": "P", "day_22": "P", "day_23": "P", "day_24": "P", "day_25": "P",
            "day_26": "P", "day_27": "P", "day_28": "P", "day_29": "P", "day_30": "A",
            "day_31": "P", "total": 28, "percentage": 90
        },
        {
            "student_name": "Robin Man Shrestha",
            "day_1": "P", "day_2": "P", "day_3": "P", "day_4": "P", "day_5": "P",
            "day_6": "P", "day_7": "P", "day_8": "P", "day_9": "P", "day_10": "P",
            "day_11": "A", "day_12": "P", "day_13": "P", "day_14": "P", "day_15": "P",
            "day_16": "P", "day_17": "A", "day_18": "P", "day_19": "P", "day_20": "P",
            "day_21": "P", "day_22": "P", "day_23": "P", "day_24": "A", "day_25": "P",
            "day_26": "P", "day_27": "P", "day_28": "P", "day_29": "A", "day_30": "P",
            "day_31": "P", "total": 27, "percentage": 87
        },
        {
            "student_name": "Aaryan",
            "day_1": "P", "day_2": "P", "day_3": "P", "day_4": "A", "day_5": "P",
            "day_6": "P", "day_7": "P", "day_8": "P", "day_9": "P", "day_10": "P",
            "day_11": "P", "day_12": "P", "day_13": "P", "day_14": "P", "day_15": "P",
            "day_16": "A", "day_17": "P", "day_18": "P", "day_19": "P", "day_20": "P",
            "day_21": "P", "day_22": "A", "day_23": "P", "day_24": "P", "day_25": "P",
            "day_26": "P", "day_27": "P", "day_28": "P", "day_29": "P", "day_30": "P",
            "day_31": "P", "total": 28, "percentage": 90
        },
        {
            "student_name": "Shivshakti Chaudhary",
            "day_1": "P", "day_2": "P", "day_3": "P", "day_4": "P", "day_5": "P",
            "day_6": "P", "day_7": "A", "day_8": "P", "day_9": "P", "day_10": "P",
            "day_11": "P", "day_12": "P", "day_13": "P", "day_14": "P", "day_15": "P",
            "day_16": "A", "day_17": "P", "day_18": "P", "day_19": "P", "day_20": "P",
            "day_21": "A", "day_22": "P", "day_23": "P", "day_24": "P", "day_25": "P",
            "day_26": "P", "day_27": "P", "day_28": "A", "day_29": "P", "day_30": "P",
            "day_31": "P", "total": 27, "percentage": 87
        },
        {
            "student_name": "Umanga Ghimire",
            "day_1": "P", "day_2": "P", "day_3": "P", "day_4": "P", "day_5": "P",
            "day_6": "A", "day_7": "P", "day_8": "P", "day_9": "P", "day_10": "P",
            "day_11": "P", "day_12": "A", "day_13": "P", "day_14": "P", "day_15": "P",
            "day_16": "P", "day_17": "P", "day_18": "P", "day_19": "P", "day_20": "P",
            "day_21": "P", "day_22": "P", "day_23": "P", "day_24": "P", "day_25": "A",
            "day_26": "P", "day_27": "P", "day_28": "P", "day_29": "P", "day_30": "P",
            "day_31": "P", "total": 28, "percentage": 90
        },
        {
            "student_name": "Simran Karki",
            "day_1": "P", "day_2": "P", "day_3": "A", "day_4": "P", "day_5": "P",
            "day_6": "P", "day_7": "P", "day_8": "P", "day_9": "P", "day_10": "A",
            "day_11": "P", "day_12": "P", "day_13": "P", "day_14": "P", "day_15": "P",
            "day_16": "P", "day_17": "P", "day_18": "P", "day_19": "A", "day_20": "P",
            "day_21": "P", "day_22": "P", "day_23": "A", "day_24": "P", "day_25": "P",
            "day_26": "P", "day_27": "P", "day_28": "P", "day_29": "A", "day_30": "P",
            "day_31": "P", "total": 26, "percentage": 84
        },
    ]
    
    # Create session and insert data
    with Session(engine) as session:
        for data in attendance_data:
            attendance_record = Attendance(**data)
            session.add(attendance_record)
        
        session.commit()
        print(f"✅ Successfully inserted {len(attendance_data)} attendance records!")