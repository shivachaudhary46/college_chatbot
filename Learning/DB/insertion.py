from back.LoginBackend.variables import user_data, attendance_data, fees_data, marks_data
from functions import add_user, add_attendance, add_fees, add_marks, get_user_with_all_data

# ========= insert all data to database ==========
def insert_data():

    for i in range(len(user_data)):

        # creating user
        user = add_user(
            user_data[i]["username"], 
            user_data[i]["full_name"], 
            user_data[i]["email"]
        )
        print(f"created user: {user.username}")
        
        attendance = add_attendance(
            user.id, 
            attendance_data[i]["month"], 
            attendance_data[i]["semester"], 
            attendance_data[i]["total"], 
            attendance_data[i]["attendee_status"],# Good Attendance, Regular, Not Consistent
        )

        fee = add_fees(
            user.id, 
            fees_data[i]["semester"],
            fees_data[i]["total_paid"],
            fees_data[i]["last_payment_date"],
        )

        marks = add_marks(
            user.id, 
            marks_data[i]["semester"],
            marks_data[i]["subject"],
            marks_data[i]["total_marks"],
            marks_data[i]["grade"],
            marks_data[i]["exam_date"],
        )

        get_user_with_all_data(user.id)
