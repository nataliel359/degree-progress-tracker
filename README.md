# 🎓 Degree Progress Tracker
A full-stack web application that tracks a student's academic progress across multiple degree programs. It calculates completed credits, missing requirements, and visualizes degree progress in an interactive dashboard.

---

## 🚀 Features
- Student degree progress dashboard
- Multi-degree program tracking
- Completed nd missing course views
- Overall progress calculation
- Login page with JWT authentication
- Protected dashboard route
- Logout support
- PostgreSQL-backend user model

---

## 🏗️ Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- Uvicorn
### Frontend
- React
- JavaScript
- CSS
### Database
- PostgreSQl
### Authentication
- JWT access tokens
- bcrypt password hashing

---

## Environment Variables

Create a `.env` file inside `backend/`:

DATABASE_URL=postgresql://postgres:your_password@localhost:5432/degree_progress
JWT_SECRET_KEY=replace_with_a_long_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=5

---

## ⚙️ Backend Setup (FastAPI)

### 1. Install dependencies
From the `backend/` folder:

pip install fastapi uvicorn

If using a requirements file:

pip install -r requirements.txt

### 2. Run backend server
From the backend/ directory:

.\venv\Scripts\Activate.ps1

uvicorn app.main:app --reload

Backend runs at:

http://127.0.0.1:8000

### 3. Test API
Open in browser or Postman:

http://127.0.0.1:8000/progress

Expected response:

{
  "student": "Natasha Romanoff",
  "major": { ... },
  "minor": { ... }
}

and API docs are available at:

http://127.0.0.1:8000/docs

---

## 🌐 Frontend Setup (React)

### 1. Install dependencies
From the frontend/ folder:

npm install

### 2. Run frontend
.\venv\Scripts\Activate.ps1 (if not already done from the backend)

npm run dev

OR (if Create React App):

npm start

### 3. Open in browser
http://localhost:3000

---

## 🗝️ Authentication Flow

1. Register a user through `POST /auth/register/`
2. Log in through `POST /auth/login`
3. The backend returns a JWT access token
4. The frontend stores the token in `localStorage`
5. Axios attaches the token to protected requests using the `Authorization` header
6. Protected pages redirect unauthenticated users to `/login`
7. Logout removes the token and returns the user to the login page

---

## 📊 API Endpoints

### Auth

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/login` | Log in and receive a JWT |
| GET | `/auth/me` | Get the current authenticated user |

### Progress

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/progress` | Get the authenticated student's progress report |

---

## ⚠️ Notes

### Database
The current database work includes a `users` table for authentication.

Recommended future tables:

- students
- courses
- degrees
- degree_requirements
- student_completed_courses

The dashboard currently still uses mock academic progress data. A future improvement is to connect `/progress` to real student/course records from PostgreSQL.

### UI
The frontend includes:

- A login page styled after the provided UI mockups
- A protected dashboard page
- A red gradient student hero section
- Program progress cards
- Completed and missing course lists

---

## Known Limitations

- Academic progress data is currently mock data.
- JWT tokens are stored in `localStorage`; production apps should consider HttpOnly secure cookies.
- Database migrations are not yet configured with Alembic.
- Password reset and email verification are not implemented.

---

## 🧠 Future Improvements

- Replace mock data with PostgreSQL-backed student records
- Add Alembic migrations
- Add role-based access for students, advisors, and admins
- Add registration page in the frontend
- Add password reset flow
- Add tests for auth and protected routes
- Deploy backend and frontend

---

## 👨‍💻 Author
Built as a degree progress tracking system for academic planning and visualization.
