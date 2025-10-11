from typing import Optional
from sqlmodel import SQLModel, Field

class FeePayment(SQLModel, table=True):
    """
    Fee Payment tracking model for 2080 Batch CSIT students
    Maps username to semester-wise fee payment records
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    student_name: str = Field(index=True)
    batch: str = Field(default="2080")
    program: str = Field(default="CSIT")
    
    # 8 semesters fee payment
    sem_1_paid: int = Field(default=0)
    sem_2_paid: int = Field(default=0)
    sem_3_paid: int = Field(default=0)
    sem_4_paid: int = Field(default=0)
    sem_5_paid: int = Field(default=0)
    sem_6_paid: int = Field(default=0)
    sem_7_paid: int = Field(default=0)
    sem_8_paid: int = Field(default=0)
    
    # Financial summary
    total_paid: int = Field(default=0)
    total_due: int = Field(default=0)
    payment_percentage: int = Field(default=0)
    
    # Metadata
    last_payment_date: Optional[str] = None
    payment_status: str = Field(default="Pending")  # Pending, Partial, Completed


SAMPLE_DATA = [
    {
        "username": "akrisha_khanal",
        "student_name": "Akrisha Khanal",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "sem_4_paid": 42000,
        "total_paid": 294000,
        "total_due": 378000,
        "payment_percentage": 44,
    },
    {
        "username": "anuprash_subedi",
        "student_name": "Anuprash Subedi",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "sem_4_paid": 84000,
        "total_paid": 336000,
        "total_due": 336000,
        "payment_percentage": 50,
    },
    {
        "username": "ashwin_phuyal",
        "student_name": "Ashwin Phuyal",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "total_paid": 252000,
        "total_due": 420000,
        "payment_percentage": 38,
    },
    {
        "username": "jenisha_adhikari",
        "student_name": "Jenisha Adhikari",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "sem_4_paid": 84000,
        "sem_5_paid": 42000,
        "total_paid": 378000,
        "total_due": 294000,
        "payment_percentage": 56,
    },
    {
        "username": "grishma_bhatt",
        "student_name": "Grishma Bhatt",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 42000,
        "total_paid": 210000,
        "total_due": 462000,
        "payment_percentage": 31,
    },
    {
        "username": "chandan_sharma_thakur",
        "student_name": "Chandan Sharma Thakur",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "sem_4_paid": 84000,
        "sem_5_paid": 84000,
        "total_paid": 420000,
        "total_due": 252000,
        "payment_percentage": 63,
    },
    {
        "username": "bisham_dhakal",
        "student_name": "Bisham Dhakal",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "sem_4_paid": 84000,
        "total_paid": 336000,
        "total_due": 336000,
        "payment_percentage": 50,
    },
    {
        "username": "khemant_raj_adhikari",
        "student_name": "Khemant Raj Adhikari",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "sem_4_paid": 42000,
        "total_paid": 294000,
        "total_due": 378000,
        "payment_percentage": 44,
    },
    {
        "username": "rohan_paudel",
        "student_name": "Rohan Paudel",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "sem_4_paid": 84000,
        "sem_5_paid": 84000,
        "sem_6_paid": 42000,
        "total_paid": 462000,
        "total_due": 210000,
        "payment_percentage": 69,
    },
    {
        "username": "jonash_chautahat",
        "student_name": "Jonash Chautahat",
        "sem_1_paid": 84000,
        "sem_2_paid": 42000,
        "sem_3_paid": 42000,
        "total_paid": 168000,
        "total_due": 504000,
        "payment_percentage": 25,
    },
    {
        "username": "karan_kc",
        "student_name": "Karan K.C",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "sem_4_paid": 84000,
        "total_paid": 336000,
        "total_due": 336000,
        "payment_percentage": 50,
    },
    {
        "username": "robin_man_shrestha",
        "student_name": "Robin Man Shrestha",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "total_paid": 252000,
        "total_due": 420000,
        "payment_percentage": 38,
    },
    {
        "username": "aaryan",
        "student_name": "Aaryan",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "sem_4_paid": 84000,
        "sem_5_paid": 42000,
        "total_paid": 378000,
        "total_due": 294000,
        "payment_percentage": 56,
    },
    {
        "username": "shivshakti_chaudhary",
        "student_name": "Shivshakti Chaudhary",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 42000,
        "sem_4_paid": 42000,
        "total_paid": 252000,
        "total_due": 420000,
        "payment_percentage": 38,
    },
    {
        "username": "umanga_ghimire",
        "student_name": "Umanga Ghimire",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "sem_4_paid": 84000,
        "sem_5_paid": 84000,
        "total_paid": 420000,
        "total_due": 252000,
        "payment_percentage": 63,
    },
    {
        "username": "simran_karki",
        "student_name": "Simran Karki",
        "sem_1_paid": 84000,
        "sem_2_paid": 84000,
        "sem_3_paid": 84000,
        "sem_4_paid": 42000,
        "total_paid": 294000,
        "total_due": 378000,
        "payment_percentage": 44,
    },
]