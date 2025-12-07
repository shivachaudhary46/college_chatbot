"""
API Routers for College Management System 
"""

from . import users
from . import auth 
from . import attendance
from . import fees
from . import marks
from . import courses
from . import assignments
from . import notices
from . import chat

__all__ = [
    "users", 
    "auth",
    "attendance",
    "fees",
    "marks",
    "courses", 
    "assignments",
    "notices",
    "chat"
]