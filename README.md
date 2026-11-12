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
- MongoDB Atlas-backed user model

---

## 🏗️ Tech Stack

### Backend
- Python
- FastAPI
- PyMongo
- Uvicorn
### Frontend
- React
- JavaScript
- CSS
### Database
- MongoDB Atlas
### Authentication
- JWT access tokens
- bcrypt password hashing
- Email-based password recovery with single-use reset links

---

## Environment Variables

Create or update a `.env` file inside `backend/`:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-host>/degree_progress?retryWrites=true&w=majority
MONGODB_DB=degree_progress
JWT_SECRET_KEY=replace_with_a_long_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=5
FRONTEND_URL=http://localhost:3000/degree-progress-tracker/
SMTP_HOST=<your-smtp-host>
SMTP_PORT=587
SMTP_USERNAME=<your-smtp-username>
SMTP_PASSWORD=<your-smtp-password>
SMTP_FROM_EMAIL=<your-verified-sender>
```

Create a MongoDB database user and allow the backend host in the Atlas Network Access settings. URL-encode special characters in the database username or password before placing them in `MONGODB_URI`. Keep this file private and do not commit credentials.
Set the SMTP values to credentials from your mail provider. Use the deployed
frontend URL, including `/degree-progress-tracker/`, for `FRONTEND_URL` in
production.

---

## ⚙️ Backend Setup (FastAPI)

### 1. Install dependencies
From the `backend/` folder:

pip install fastapi uvicorn

If using a requirements file:

pip install -r requirements.txt

### Seed curriculum data
From the `backend/` folder, with `MONGODB_URI` configured in `.env`, run:

```powershell
python -m scripts.seed_curriculum
```

The script upserts courses, degree programs, and categorized requirements from
`app/services/mock_data.py`. It does not create a user or seed any student's
completed courses.

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

For a deployed backend, set `REACT_APP_API_URL` to its base URL before building
the frontend. It defaults to `http://127.0.0.1:8000` for local development.

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
8. Password reset requests send a single-use link that expires after 30 minutes

---

## 📊 API Endpoints

### Auth

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/login` | Log in and receive a JWT |
| GET | `/auth/me` | Get the current authenticated user |
| POST | `/auth/password-reset/request` | Email a password reset link |
| POST | `/auth/password-reset/confirm` | Set a new password with a valid reset token |

### Progress

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/progress` | Get the authenticated student's progress report |

---

## ⚠️ Notes

### Database
Authentication users are stored in the MongoDB Atlas `users` collection. The backend creates unique indexes for email and optional student ID when it starts.

Recommended future collections:

- students
- courses
- degrees
- degree_requirements
- student_completed_courses

The dashboard currently still uses mock academic progress data. A future improvement is to connect `/progress` to real student/course records in MongoDB Atlas.

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
- Existing PostgreSQL user records are not copied automatically; migrate them to the Atlas `users` collection before switching production traffic.
- Password reset email delivery requires the SMTP settings described above.

---

## 🧠 Future Improvements

- Replace mock data with MongoDB-backed student records
- Add role-based access for students, advisors, and admins
- Add registration page in the frontend
- Add email verification
- Add tests for auth and protected routes
- Deploy backend and frontend

---

## 👨‍💻 Author
Built as a degree progress tracking system for academic planning and visualization.
