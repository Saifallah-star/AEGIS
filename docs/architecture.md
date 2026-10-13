# Architecture

## Technology Stack

- React and TypeScript for the browser interface
- Vite for frontend development and builds
- FastAPI for HTTP endpoints
- yt-dlp for supported media retrieval where permitted
- FFmpeg for supported media processing

## Intended Request Flow

Browser → frontend API service → FastAPI route → input validation → application service → media-processing worker → controlled result delivery.

This describes the intended architecture; not every component is implemented yet.

## Design Principles

- Keep HTTP routes thin and business logic in services.
- Isolate long-running jobs from request handling.
- Validate untrusted input and enforce resource limits.
- Keep temporary files private and clean them up.
- Do not expose stack traces or sensitive server details.

## Decisions Still Needed

- Background job and progress-reporting mechanism
- Temporary-file lifecycle and download delivery
- Rate limits and concurrent job limits
- Persistence requirements
- Deployment configuration
