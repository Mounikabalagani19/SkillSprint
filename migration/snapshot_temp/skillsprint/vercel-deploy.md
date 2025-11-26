Deploying the Frontend to Vercel

1. In Vercel, create a new Project and point it to this repository.
2. Set the Root Directory to `frontend`.
3. Set Environment Variables (in Project Settings):
   - `VITE_API_URL` -> the base URL of your backend, e.g. `https://api.example.com/api/v1`
4. Vercel will run:
   - `npm install`
   - `npm run build`
   and serve the `dist` folder.

Notes

- The backend (FastAPI) should be deployed separately (Render, Heroku, Railway, etc.).
- Ensure CORS in `backend/app/main.py` includes your Vercel URL.
- If you want a single-repo deploy, additional work is required to convert the backend to serverless functions and use an external DB (SQLite is not suitable for serverless). I can help with that if needed.
