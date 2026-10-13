# MP3 Downloader

A web-based media downloading and conversion application built with React, TypeScript, FastAPI, yt-dlp, and FFmpeg.

## Status

Early development. The frontend scaffold exists. Backend application implementation and automated testing are still being established.

## Technology Stack

- Frontend: React, TypeScript, Vite
- Backend: Python, FastAPI
- Media processing: yt-dlp, FFmpeg

## Repository Structure

- `frontend/`: browser application
- `backend/`: API and media-processing services
- `docs/`: technical documentation and architecture decisions
- `specs/features/`: feature specifications
- `tasks/`: development backlog
- `scripts/`: development utilities

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Once `backend/app/main.py` exists, start the API with:

```bash
uvicorn app.main:app --reload --port 8000
```

## Quality Checks

Run from `frontend/`:

```bash
npm run build
npm run lint
```

## Development Workflow

Read `AGENTS.md` before making changes. Define acceptance criteria, implement one focused task at a time, run checks, and inspect the Git diff.

Only process media in ways permitted by applicable laws, platform terms, and the user's rights. Do not bypass DRM or access controls.
