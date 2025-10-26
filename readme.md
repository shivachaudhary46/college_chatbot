# Student Management System - Complete Architecture

student_system/
│
├── app/                          # Main package
│   ├── __init__.py              # Empty file
│   ├── config.py                # Settings & environment variables
│   ├── database.py              # Database engine & session
│   ├── models.py                # SQLModel definitions
│   ├── schemas.py               # Pydantic request/response models
│   ├── crud.py                  # Database operations (Create, Read, Update, Delete)
│   ├── utilities.py             # Authentication & JWT tokens
│   ├── chatbot.py               # AI chatbot logic
│   └── main.py                  # FastAPI app & all routes
│
├── run.py                       # Start the server
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
└── database.db                  # SQLite database (auto-created)



# Database Schema (SQLModel) 

user table
├── id (Primary Key)
├── username (Unique)
├── full_name
├── email
├── batch
├── program
├── hashed_password
├── disabled
└── created_at

attendance table
├── id (Primary Key)
├── user_id (Foreign Key → user.id)
├── month
├── semester
├── total (%)
├── attendee_status
└── created_at

marks table
├── id (Primary Key)
├── user_id (Foreign Key → user.id)
├── semester
├── subject
├── total_marks
├── grade
├── status
├── exam_date
└── created_at

fees table
├── id (Primary Key)
├── user_id (Foreign Key → user.id)
├── semester
├── total_paid
├── amount_due
├── payment_status
├── last_payment_date
└── created_at


chatbot_college_websites/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point & configuration
│   ├── config.py            # Configuration settings
│   ├── dependencies.py      # Shared dependencies
│   │
│   ├── api/                 # API layer
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chatbot.py   # Chatbot endpoints
│   │   │   ├── students.py  # Student CRUD endpoints
│   │   │   └── admin.py     # Admin endpoints
│   │   └── deps.py          # Route dependencies
│   │
│   ├── core/                # Core functionality
│   │   ├── __init__.py
│   │   ├── database.py      # Database connection
│   │   └── security.py      # Auth & security
│   │
│   ├── models/              # Database models (SQLAlchemy/ORM)
│   │   ├── __init__.py
│   │   ├── student.py
│   │   ├── conversation.py
│   │   └── user.py
│   │
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── student.py
│   │   ├── chatbot.py
│   │   └── user.py
│   │
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── chatbot_service.py
│   │   ├── student_service.py
│   │   └── ai_service.py
│   │
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── helpers.py
│
├── backend/                 # If you have additional backend code
├── frontend/                # Frontend code
├── learning/                # ML/AI models & training
├── tests/                   # Test files
│   ├── __init__.py
│   ├── test_api/
│   └── test_services/
├── .env
├── .gitignore
├── requirements.txt
└── README.md