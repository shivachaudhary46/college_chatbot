from datetime import datetime

user_data = [
        {
            "full_name": "Akrisha Khanal",
            "username": "akrisha",
            "email": "akrisha@mbmc.edu.np",
        },
        {
            "full_name": "Jenisha Adhikari",
            "username": "jenisha",
            "email": "jenisha@mbmc.edu.np",
        },
        {
            "full_name": "Grishma Bhatt",
            "username": "grishma",
            "email": "grishma@mbmc.edu.np",
        },
        {
            "full_name": "Chandan Sharma Thakur",
            "username": "chandan",
            "email": "chandan@mbmc.edu.np",
        },
        {
            "full_name": "Shiva Chaudhary",
            "username": "shiva",
            "email": "shiva@college.com",
        },
        {
            "full_name": "Umanga Ghimire",
            "username": "umanga",
            "email": "umanga@college.com",
        },
    ]

attendance_data = [
        {
            "month": "Ashoj",
            "semester": "4th",
            "total": 27, 
            "attendee_status": "satisfied"
        },
        {
            "month": "Ashoj",
            "semester": "4th",
            "total": 21, 
            "attendee_status": "not regular"
        },
        {
            "month": "Ashoj",
            "semester": "4th",
            "total": 25, 
            "attendee_status": "regular"
        },
        {
            "month": "Ashoj",
            "semester": "4th",
            "total": 12, 
            "attendee_status": "not regular"
        },
        {
            "month": "Ashoj",
            "semester": "4th",
            "total": 27, 
            "attendee_status": "satisfied"
        },
        {
            "month": "Ashoj",
            "semester": "4th",
            "total": 25, 
            "attendee_status": "regular"
        },
    ]

fees_data = [
        {
            "semester": "4th",
            "total_paid": 5000,
            "last_payment_date": datetime(2025, 12, 9)
        },
        {
            "semester": "4th",
            "total_paid": 84000,
            "last_payment_date": datetime(2025, 3, 8)
        },
        {
            "semester": "4th",
            "total_paid": 50000,
            "last_payment_date": datetime(2025, 1, 3)
        },
        {
            "semester": "4th",
            "total_paid": 84000,
            "last_payment_date": datetime(2025, 5, 23)
        },
        {
            "semester": "4th",
            "total_paid": 25000,
            "last_payment_date": datetime(2025, 3, 20)
        },
        {
            "semester": "4th",
            "total_paid": 84000,
            "last_payment_date": datetime(2025, 6, 10)
        },
    ]

marks_data = [
        {
            "semester": "4th",
            "subject": "AI",
            "total_marks": 55,
            "grade": "A",
            "exam_date": datetime(2025, 12, 9)
        },
        {
            "semester": "4th",
            "subject": "AI",
            "total_marks": 35,
            "grade": "B",
            "exam_date": datetime(2025, 12, 9)
        },
        {
            "semester": "4th",
            "subject": "AI",
            "total_marks": 23,
            "grade": "C",
            "exam_date": datetime(2025, 12, 9)
        },
        {
            "semester": "4th",
            "subject": "AI",
            "total_marks": 12,
            "grade": "E",
            "exam_date": datetime(2025, 12, 9)
        },
        {
            "semester": "4th",
            "subject": "AI",
            "total_marks": 58,
            "grade": "A",
            "exam_date": datetime(2025, 12, 9)
        },
        {
            "semester": "4th",
            "subject": "AI",
            "total_marks": 45,
            "grade": "B",
            "exam_date": datetime(2025, 12, 9)
        },
  
    ]


notice_data = [
    {
        "title": "Mid-Term Exam of BScCSIT 4th Semester (2080 Batch)",
        "description": "Mid-term examination for Bachelor of Science in Computer Science and Information Technology, 4th semester students of 2080 batch will be held as per the scheduled date.",
        "notice_type": "Exam",
        "category": "CSIT",
        "batch": "2080",
        "semester": "4th",
        "is_active": True,
        "issued_by": "Academic Department",
    },
    {
        "title": "Class Commencement Notice 2082",
        "description": "Classes for all batches will commence from the scheduled date. Students are requested to register before the commencement.",
        "notice_type": "Academic",
        "category": "All",
        "is_active": True,
        "issued_by": "TU Admin",
    },
    {
        "title": "Notice Regarding Mini Research Grants – 2082",
        "description": "Call for mini research grants for students and faculty members. Interested candidates should submit their proposals by the deadline.",
        "notice_type": "Academic",
        "category": "All",
        "is_active": True,
        "is_urgent": True,
        "issued_by": "Research Department",
    },
    {
        "title": "Pre-Board Exam of BA, BBS Second Year (2080 Batch)",
        "description": "Pre-board examination for Bachelor of Arts and Bachelor of Business Studies, second year students of 2080 batch.",
        "notice_type": "Exam",
        "category": "BA, BBS",
        "batch": "2080",
        "semester": "2nd",
        "is_active": True,
        "issued_by": "Examination Board",
    },
    {
        "title": "Mid-Term Exam of BScCSIT 6th Semester (2079 Batch)",
        "description": "Mid-term examination for BScCSIT 6th semester students of 2079 batch will be conducted on scheduled dates.",
        "notice_type": "Exam",
        "category": "CSIT",
        "batch": "2079",
        "semester": "6th",
        "is_active": True,
        "issued_by": "Academic Department",
    },
    {
        "title": "Announcement: EV Technology Training of Trainers",
        "description": "Training program on Electric Vehicle Technology for trainers. Application deadline has been extended.",
        "notice_type": "Event",
        "category": "All",
        "is_active": True,
        "is_urgent": True,
        "issued_by": "Training Department",
    },
    {
        "title": "Gai Jatra Notice 2082",
        "description": "Official notice regarding Gai Jatra celebrations and holidays. All offices will remain closed on the scheduled dates.",
        "notice_type": "Holiday",
        "category": "All",
        "is_active": True,
        "issued_by": "TU Admin",
    },
    {
        "title": "Call for the Proposal for Research Grants to Students & Faculties 2082",
        "description": "Interested students and faculty members are invited to submit proposals for research grants. Detailed guidelines and application forms are available.",
        "notice_type": "Academic",
        "category": "All",
        "is_active": True,
        "is_urgent": True,
        "issued_by": "Research Department",
    },
    {
        "title": "Notice Regarding Viva Voce Examination – BA (JMC) 3rd Year 2078 Batch",
        "description": "Viva Voce examination schedule for Bachelor of Arts in Journalism and Mass Communication, 3rd year students of 2078 batch.",
        "notice_type": "Exam",
        "category": "BA",
        "batch": "2078",
        "semester": "3rd",
        "is_active": True,
        "issued_by": "Examination Board",
    },
    {
        "title": "Pre-Board Exam of BBM Fourth Semester (2080 Batch) and BBM Sixth Semester (2079 Batch)",
        "description": "Pre-board examination for Bachelor of Business Management students of specified batches and semesters.",
        "notice_type": "Exam",
        "category": "BBS",
        "is_active": True,
        "issued_by": "Examination Board",
    },
]