Recommended Deployment

This repository contains a Vite React frontend (in `frontend/`) and a FastAPI backend (in `backend/app`). They are currently arranged as two separate apps. Vercel supports static sites and serverless functions but packaging a full FastAPI app into Vercel's Python serverless environment can be fragile.

Recommended approach

- Deploy frontend to Vercel (static build):
  1. Point Vercel to this repository and set the root to the project root.
  2. In `vercel.json` we build the frontend. Ensure `frontend/package.json` has `build` script (it does: `vite build`).
  3. Set an environment variable `VITE_API_URL` in Vercel to your backend URL (e.g. `https://api.example.com/api/v1`).

- Deploy backend to a dedicated Python host (Render, Fly.io, Heroku, Railway):
  1. Create a service that runs `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
  2. Make sure `requirements.txt` is installed and environment variables for any secrets are set.
  3. Configure CORS in `backend/app/main.py` to include your Vercel frontend origin (e.g. `https://your-site.vercel.app`).

Why split? Full FastAPI apps often need persistent files, DBs (SQLite isn't suitable for multi-instance), and background workers. A host like Render makes this simpler to configure.

Quick local build

- Frontend (from repo root):

  cd frontend
  npm install
  npm run build

- Backend (from `backend`):

  python -m venv venv
  .\venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  uvicorn app.main:app --host 0.0.0.0 --port 8000

Notes

- If you still prefer to deploy both to Vercel, consider packaging the backend as separate serverless functions and removing SQLite (use an external DB). This is more advanced and I can help with it if you want.
