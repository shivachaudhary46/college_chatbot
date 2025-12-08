<!-- Centered Logo and Title -->
<div align="center">
  <img src="./frontend/assets/readme_assets/chatbot-logo.png" width="300" alt="Chatbot Logo">
</div>


<div align="center">

  <!-- Contributors Badge (example, customize with more info if needed) -->
[![Contributors](https://img.shields.io/badge/-Contributors-blueviolet?style=flat)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


<div align="center">

<!-- Tech badges -->
[![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat&logo=html5&logoColor=white)](#)
[![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=flat&logo=css3&logoColor=white)](#)
[![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)](#)
[![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](#)
[![Pandas](https://img.shields.io/badge/-Pandas-150458?style=flat&logo=pandas&logoColor=white)](#)
[![Scikit-Learn](https://img.shields.io/badge/-Scikit&#32;Learn-F7931E?style=flat&logo=scikitlearn&logoColor=white)](#)
[![PyTorch](https://img.shields.io/badge/-PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)](#)
[![Transformers](https://img.shields.io/badge/-Transformers-FFD700?style=flat)](#)
[![LangChain](https://img.shields.io/badge/-LangChain-47A248?style=flat)](#)
[![Google Generative AI](https://img.shields.io/badge/-Google&#32;GenAI-4285F4?style=flat&logo=google)](#)
[![Groq](https://img.shields.io/badge/-Groq-FF5A1E?style=flat)](#)
[![Pinecone](https://img.shields.io/badge/-Pinecone-03989E?style=flat)](#)
[![SQLite](https://img.shields.io/badge/-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)](#)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-D71F00?style=flat)](#)
[![SQLModel](https://img.shields.io/badge/-SQLModel-21A366?style=flat)](#)
[![PyJWT](https://img.shields.io/badge/-PyJWT-007A69?style=flat)](#)
[![Python-JOSE](https://img.shields.io/badge/-python--jose-5A29E4?style=flat)](#)
[![Cryptography](https://img.shields.io/badge/-Cryptography-333333?style=flat)](#)
[![Crawl4AI](https://img.shields.io/badge/-Crawl4AI-E92B00?style=flat)](#)
[![Pydantic](https://img.shields.io/badge/-Pydantic-6F4BE6?style=flat)](#)



# Introduction

A Smart Chatbot for College Management System revolutionizes campus workflows and student-teacher interaction which leverages AI to provide instant support for campus queries (Q/A) , attendance, assignments, and so on.

It is built using a robust Python, FastAPI, and top ML/AI libraries, stack—HTML, CSS, JS. It designed for scalability, adaptability and very easier to use.


---

# Features for Teachers
- ### Create account
  <div style="display: flex; gap: 28px; justify-content: center;">
    <img src="./frontend/assets/readme_assets/create_account.gif" alt="dashboard" width="340">
  </div>

- ### Student Chatbot & Dashboard
  <div style="display: flex; gap: 18px; justify-content: center;">
    <img src="./frontend/assets/readme_assets/dashboard.png" alt="dashboard" width="340">
    <img src="./frontend/assets/readme_assets/chatbot.png" alt="chatbot" width="340">
  </div>

- ### Attendance Management
  <div style="display: flex; gap: 12px; justify-content: center;">
    <img src="./frontend/assets/readme_assets/attendance_create.gif" alt="Attendance Create" width="180">
    <img src="./frontend/assets/readme_assets/attendance_update.gif" alt="Attendance Update" width="180">
    <img src="./frontend/assets/readme_assets/attendance_delete.gif" alt="Attendance Delete" width="180">
  </div>

- ### Assignment Management
  <div style="display: flex; gap: 12px; justify-content: center;">
    <img src="./frontend/assets/readme_assets/assignment_create.gif" alt="Attendance Create" width="180">
    <img src="./frontend/assets/readme_assets/assignment_update.gif" alt="Attendance Update" width="180">
    <img src="./frontend/assets/readme_assets/assignment_delete.gif" alt="Attendance Delete" width="180">
  </div>

- ### Marks Management
  <div style="display: flex; gap: 12px; justify-content: center;">
    <img src="./frontend/assets/readme_assets/create_mark.gif" alt="Attendance Create" width="180">
    <img src="./frontend/assets/readme_assets/update_mark.gif" alt="Attendance Update" width="180">
    <img src="./frontend/assets/readme_assets/delete_mark.gif" alt="Attendance Delete" width="180">
  </div>

- ### Notice Management
  <div style="display: flex; gap: 12px; justify-content: center;">
    <img src="./frontend/assets/readme_assets/create_notice.gif" alt="Attendance Create" width="180">
    <img src="./frontend/assets/readme_assets/update_notice.gif" alt="Attendance Update" width="180">
    <img src="./frontend/assets/readme_assets/delete_notice.gif" alt="Attendance Delete" width="180">
  </div>


- ### Fee Management
<div style="display: flex; gap: 12px; justify-content: center;">
    <img src="./frontend/assets/readme_assets/create_fee.gif" alt="Attendance Create" width="180">
    <img src="./frontend/assets/readme_assets/update_fee.gif" alt="Attendance Update" width="180">
    <img src="./frontend/assets/readme_assets/delete_fee.gif" alt="Attendance Delete" width="180">
</div>

- ### Course
  <div style="display: flex; gap: 12px; justify-content: center;">
    <img src="./frontend/assets/readme_assets/create_course.gif" alt="Attendance Create" width="180">
    <img src="./frontend/assets/readme_assets/update_course.gif" alt="Attendance Update" width="180">
    <img src="./frontend/assets/readme_assets/delete_course.gif" alt="Attendance Update" width="180">
</div>

- ### Dashboard Overview
  <div style="display: flex; gap: 28px; justify-content: center;">
    <img src="./frontend/assets/readme_assets/teacher_dashboard.png" alt="dashboard" width="340">
  </div>
---

## Chatbot Architecture and Workflow

The chatbot processes user queries through a multi-stage pipeline that categorizes, retrieves, and formats information before delivering responses.

**Query Classification**
When users submit queries regarding college information, attendance records, academic marks, fee details, enrolled courses, or record updates, the system classifies each query into one of the following categories: General Information, College Information, Attendance, Marks, Fees, or Courses Enrolled.

**Data Retrieval**
The system employs a conditional data retrieval strategy:
- For user-specific queries (attendance, marks, fees, enrolled courses), the system fetches data directly from the SQL database.
- For irrelevant or out-of-scope queries, the system performs a web search via DuckDuckGo and returns the search results.
- For general college-related queries, the system retrieves information from a Pinecone vector database. This database was populated using the Crawl4AI API to crawl and index the college website content.

**Response Generation**
Before delivering the final response, the system formats the retrieved documents and passes them to a Large Language Model (LLM) for optimization and natural language generation.

**Response Delivery**
The processed response is then returned to the user.

<p align="center">
  <img src="./frontend/assets/readme_assets/structure.png" alt="System Architecture" width="640">
</p>
Fig: Architecture of chatbot

---

## Database Models

The backend leverages robust, normalized models enabling efficient data management.

<p align="center">
  <img src="./frontend/assets/readme_assets/models_diagram.png" alt="Database Models" width="640">
</p>
Fig: Database models of SQLModel 
---

## Installation

### With Docker


### Manual Installation

First fork this repository 

```bash
# Clone the repo
git clone https://github.com/shivachaudhary46/college_chatbot.git

cd college_chatbot

## NOTE: Python==3.11 or Python==3.10 is Compatible versions

# create new virtual environment 
python3 -m venv venv

# install all neccessary packages 
pip3 install -r requirements.txt 

# check list of packages 
pip3 list 
```

One last step is remaining to complete before we run our app, 

<p align="center">
  <img src="./frontend/assets/readme_assets/error_loading_classifier.png" alt="Database Models" width="640">
</p>

If you see Error Loading model, don't worry, 

<p align="center">
  <img src="./frontend/assets/readme_assets/college_queries.png" alt="Database Models" width="640">
</p>

You can see Classification.ipynb right. First, you have to trained model. Run each cell in classification model, the trained_model will come in backend/data. Run classificiation.ipynb all cells 

<p align="center">
  <img src="./frontend/assets/readme_assets/trained_model.png" alt="Database Models" width="640">
</p>
Fig: Trained_model shown 

to run the app

first go to the
```bash

cd backend 

python app/main.py 

# another way

cd backend

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-exclude backend/logs/*

```

**Frontend:**
```bash
cd frontend
# (Adapt commands for your frontend stack)
npm install
npm start
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
| Docker                   | Manual                        |
|--------------------------|------------------------------|
| Rapid setup              | Customizable configuration   |
| Encapsulated dependencies| Direct control of each part  |
| Easier deployment        | Local installation           |

---

## URLs

**Frontend URL:** [`http://127.0.0.1:5500`](http://127.0.0.1:5500)  
**Backend API:** [`http://127.0.0.1:8000/api/v1/`](http://127.0.0.1:8000/api/v1/)

---

> "Chatbot Logo": Chatbot