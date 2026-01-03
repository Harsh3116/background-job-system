# Background Job Processing System

A full-stack background job processing system built with:

- **FastAPI** – REST API
- **Redis** – job queue
- **PostgreSQL** – persistent job storage
- **Python Worker** – background execution
- **React** – admin dashboard for job tracking

## Features

- Create background jobs via API or UI
- Asynchronous job execution
- Redis-backed queue
- Persistent job state
- Retry and failure handling
- Real-time job status tracking
- React dashboard with job history

## Architecture

Client → FastAPI → Redis Queue → Worker → PostgreSQL  
Frontend polls API for job status updates.

## How to Run

### Backend
pip install -r requirements.txt
uvicorn main:app

### WORKER
python worker.py

### FRONTEND
cd frontend/job-ui
npm install
npm run dev

Why This Project

This project demonstrates real-world backend system design, including
producer–consumer architecture, background processing, and frontend–backend integration.


Commit and push:

git add README.md
git commit -m "Add project README"
git push
