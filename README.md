# Task Tracker

A full-stack Task Management Web Application built using FastAPI and React.

This project demonstrates authentication, protected routes, database integration, and deployment.

--------------------------------------------------

Tech Stack

Backend
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Passlib (bcrypt)

Frontend
- React
- Vite
- Fetch API
- LocalStorage

Deployment
- Render (Backend)
- Vercel (Frontend)

--------------------------------------------------

Features

- User Registration
- User Login (JWT)
- Protected Routes
- User-specific tasks
- Create task
- Update task
- Delete task
- Filter tasks by status
- CORS enabled
- Production ready

--------------------------------------------------

Project Structure

task-tracker
  api/
    main.py
    core/
    storage/
  task-ui/
    src/
  requirements.txt
  README.md

--------------------------------------------------

Backend Setup

Install dependencies

pip install -r requirements.txt

Run server

uvicorn main:app --reload

Server URL

http://127.0.0.1:8000

Swagger Docs

http://127.0.0.1:8000/docs

--------------------------------------------------

Frontend Setup

Install

npm install

Run

npm run dev

--------------------------------------------------

Environment Variable

Create .env file inside frontend

VITE_API_URL=http://127.0.0.1:8000

For production

VITE_API_URL=https://your-render-url

--------------------------------------------------

Authentication Flow

1. Register user
2. Login
3. Receive JWT token
4. Save token in localStorage
5. Send header

Authorization: Bearer <token>

6. Backend validates token
7. Returns only that user's tasks

--------------------------------------------------

API Endpoints

POST /register
POST /login

GET /tasks
POST /tasks
PUT /tasks/{id}
DELETE /tasks/{id}

--------------------------------------------------

Learning Outcomes

- REST API design
- JWT authentication
- Protected routes
- SQLAlchemy ORM
- React hooks
- Deployment
- CORS
- Full stack integration

--------------------------------------------------

Author

Sabari Gireeswaran
