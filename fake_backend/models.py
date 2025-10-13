from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# ============= Attendance Information Table =============
class Attendance(SQLModel, table=True):
    """
    Attendance model for 2080 Batch Ashoj Month CSIT 4th semester
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    student_name: str = Field(index=True)
    batch: str = Field(default="2080")
    month: str = Field(default="Ashoj")
    semester: str = Field(default="4th")
    program: str = Field(default="CSIT")
    
    # 31 days of attendance
    day_1: str
    day_2: str
    day_3: str
    day_4: str
    day_5: str
    day_6: str
    day_7: str
    day_8: str
    day_9: str
    day_10: str
    day_11: str
    day_12: str
    day_13: str
    day_14: str
    day_15: str
    day_16: str
    day_17: str
    day_18: str
    day_19: str
    day_20: str
    day_21: str
    day_22: str
    day_23: str
    day_24: str
    day_25: str
    day_26: str
    day_27: str
    day_28: str
    day_29: str
    day_30: str
    day_31: str
    
    total: int
    percentage: int
    
