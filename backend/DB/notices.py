from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Notice(SQLModel, table=True):
    """
    Notice and Announcement model for Tribhuvan University
    Stores all official notices and announcements from the college
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    notice_type: str  # e.g., "Exam", "Academic", "Event", "Holiday", "General"
    category: str  # e.g., "CSIT", "BBS", "BA", "All"
    batch: str
    semester: str

    # Dates
    issued_date: datetime = Field(default_factory=datetime.utcnow)
    
    # Status
    is_active: bool = Field(default=True)
    is_urgent: bool = Field(default=True)
    
    # Additional info
    issued_by: str = Field(default="MBMC Admin")
    attachments_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


SAMPLE_DATA = [
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