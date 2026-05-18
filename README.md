# 🎓 Degree Progress Tracker
A full-stack web application that tracks a student's academic progress across a Computer Science Major and Business Minor. It calculates completed credits, missing requirements, and visualizes degree progress in an interactive dashboard.

---

## 🚀 Features
- Tracks completed vs missing courses
- Separates requirements by category (required, electives, gen-ed, science breadth)
- Calculates credit totals and progress percentage
- REST API built with FastAPI
- Interactive React dashboard
- Mock data for student and degree programs

---

## 🏗️ Tech Stack
### Backend
- Python
- FastAPI
- Uvicorn
### Frontend
- React
- JavaScript
- CSS

---

## ⚙️ Backend Setup (FastAPI)

### 1. Install dependencies
From the `backend/` folder:

pip install fastapi uvicorn

If using a requirements file:

pip install -r requirements.txt

### 2. Run backend server
From the backend/ directory:

uvicorn main:app --reload

Backend runs at:

http://127.0.0.1:8000

### 3. Test API
Open in browser or Postman:

GET http://127.0.0.1:8000/progress

Expected response:

{
  "student": "Natasha Romanoff",
  "major": { ... },
  "minor": { ... }
}

---

## 🌐 Frontend Setup (React)

### 1. Install dependencies
From the frontend/ folder:

npm install

### 2. Configure API
Make sure your frontend calls the backend correctly:

export async function getProgress() {

    const res = await fetch("http://127.0.0.1:8000/progress");
    
    return res.json();
    
}

### 3. Run frontend
npm run dev

OR (if Create React App):

npm start

### 4. Open in browser
http://localhost:3000

---

## 🔄 How It Works

1. Backend generates mock student + degree data
2. /progress endpoint computes:
    - Completed courses
    - Missing courses
    - Credit totals per category
3. Frontend fetches API data on load
4. Dashboard renders:
    - Major & minor progress
    - Progress bars
    - Completed vs missing courses

---

## 📊 API Overview

### GET /progress

Returns:

    - Student name
    - Major progress object
    - Minor progress object
Each program includes:

    - Summary (total credits, completion %, remaining credits)
    - Requirements breakdown:
        - required
        - electives
        - gen_ed
        - science_breadth
    - Completed courses
    - Missing courses

---

## ⚠️ Notes
    - Uses mock data (no database yet)
    - CORS enabled for all origins
    - Backend must be running before frontend fetch works

---

## 🧠 Future Improvements
    - Add PostgreSQL database
    - User authentication
    - Real course input system
    - Degree requirement editor
    - Export progress as PDF
    - Persistent user data

---

## 👨‍💻 Author
Built as a degree progress tracking system for academic planning and visualization.
