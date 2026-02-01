# 🧪 Task Tracker – Full Stack Task Management App

A clean, beginner-friendly full-stack task management application built using FastAPI (backend) and React (frontend).

This project demonstrates real-world software architecture including:
- Backend APIs
- Database integration
- Authentication
- Frontend UI
- Full-stack communication
- Deployment ready structure

---

## 🚀 Features

### ✅ Backend (FastAPI)
- Create tasks
- List all tasks
- Filter by status (todo / in-progress / done)
- Update tasks
- Delete tasks
- Get task by ID
- User registration
- Login authentication
- Password hashing using bcrypt
- SQLite database storage
- Clean layered architecture

### ✅ Frontend (React + Vite)
- View all tasks
- Add new tasks
- Delete tasks
- Mark tasks as done
- Filter tasks by status
- API integration with FastAPI
- Simple responsive UI

---

## 🧠 Tech Stack

### Backend
- Python
- FastAPI
- SQLite
- SQLAlchemy
- Passlib (bcrypt)

### Frontend
- React
- Vite
- JavaScript
- Fetch API

### Tools
- Git
- GitHub
- Node.js
- npm

---

###📂 Project Structure

task-tracker/
api/               
core/              
storage/           
task-ui/           
requirements.txt 
README.md  
.gitignore

---

## 🧠 Architecture

Frontend (React)
      ↓ HTTP/JSON
Backend (FastAPI)
      ↓
Service Layer (TaskManager)
      ↓
Database (SQLite)

This layered architecture keeps:
- UI separate
- Logic separate
- Storage separate

Making the app scalable and maintainable.

---

# ⚙️ Backend Setup

## 1. Clone repository
git clone https://github.com/SabariGireeswaran/task-tracker.git
cd task-tracker

## 2. Create virtual environment
python -m venv venv
source venv/bin/activate

## 3. Install dependencies
pip install -r requirements.txt

## 4. Run backend server
uvicorn api.main:app --reload

Open:
http://127.0.0.1:8000/docs

---

# ⚛️ Frontend Setup

## 1. Go to frontend folder
cd task-ui

## 2. Install packages
npm install

## 3. Start React app
npm run dev

Open:
http://localhost:5173

---

# 🔐 Authentication Flow

1. Register user
2. Login user
3. Password stored securely (hashed)
4. JWT authentication (planned/next step)

---

# 📌 Future Improvements

- JWT authentication
- Protected routes
- User-specific tasks
- Better UI styling (Tailwind/Bootstrap)
- Deploy frontend (Render/Vercel)
- Docker support
- Unit testing

---

# 🎯 Learning Outcomes

This project helped practice:

- REST API design
- CRUD operations
- Database modeling
- Authentication systems
- React frontend development
- Full-stack integration
- Git workflow
- Deployment concepts

---

# 🙌 Author

Sabari Gireeswaran  
B.Sc Mathematics  
Aspiring Full Stack Developer  
Learning FastAPI | React | Full Stack Development

---

⭐ If you like this project, give it a star on GitHub!
