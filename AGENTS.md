# Agent Instructions

## 1. Project Overview

MP3 Downloader is a web application built with React, TypeScript,
FastAPI, yt-dlp, and FFmpeg.

The goal is to provide a maintainable, secure, testable application
for media downloading and conversion where legally and technically
permitted.

## 2. Repository Structure

- `frontend/`: React, TypeScript, Vite application.
- `backend/`: FastAPI application and media-processing services.
- `docs/`: Architecture, requirements, security, and design decisions.
- `specs/features/`: Feature specifications and acceptance criteria.
- `tasks/`: Development backlog and implementation plans.
- `scripts/`: Repeatable development and maintenance scripts.

Keep frontend and backend responsibilities separate.

## 3. Mandatory Workflow

Before implementing a task:

1. Read this file and relevant documentation.
2. Inspect the existing implementation and Git status.
3. Identify the task requirements and acceptance criteria.
4. Write a short plan for non-trivial changes.
5. Identify affected files, dependencies, risks, and tests.

During implementation:

1. Make the smallest coherent change that satisfies the task.
2. Follow existing conventions unless a documented reason
   justifies changing them.
3. Avoid unrelated refactoring and unnecessary dependencies.
4. Do not overwrite or delete existing work without authorization.
5. Never modify files outside the project unless explicitly asked.
6. Do not silently change public API contracts.

After implementation:

1. Run relevant tests and available quality checks.
2. Inspect the Git diff for unintended changes.
3. Report files changed, commands run, results, and limitations.
4. Never claim a test passed unless it was actually run.
5. Identify any remaining risks or manual verification steps.

Ask before proceeding when requirements are ambiguous and the
decision could materially affect architecture, security, or data.

## 4. Architecture Rules

### Frontend

- Use TypeScript and React.
- Keep reusable UI components separate from feature-specific logic.
- Put API communication behind a service layer.
- Represent loading, success, empty, and error states explicitly.
- Avoid duplicating API types and business logic unnecessarily.
- Do not place secrets in frontend code or Vite environment variables.

### Backend

- Use FastAPI for HTTP routes and request handling.
- Keep routes thin; put business logic in services.
- Validate requests and responses with explicit schemas.
- Separate configuration, domain logic, and infrastructure concerns.
- Use asynchronous/background processing for long-running work
  when appropriate.
- Return consistent, safe error responses.
- Keep temporary files isolated and clean them up reliably.
- Never expose server paths, stack traces, or secrets to clients.

Do not create abstractions or directories without a current need.

## 5. Security Requirements

- Treat all user input and external URLs as untrusted.
- Never disable TLS certificate verification to bypass errors.
- Protect against SSRF, local-file access, path traversal,
  command injection, and unsafe file handling.
- Do not execute user-provided shell commands.
- Use subprocess argument lists rather than shell command strings.
- Restrict media processing to explicitly supported inputs.
- Apply sensible request, file-size, duration, and resource limits.
- Keep secrets in environment variables, never in source control.
- Never log passwords, tokens, or sensitive user data.
- Only support media operations consistent with applicable
  laws, platform terms, and the user's rights.
- Do not bypass DRM, paywalls, or access controls.

Any public-facing download endpoint requires a security review
before deployment.

## 6. Code Quality

- Prefer clear, readable, maintainable code over clever shortcuts.
- Use descriptive names and small, cohesive functions.
- Handle expected errors explicitly.
- Avoid broad exception handling that hides failures.
- Add tests for business logic, validation, error cases,
  and security-sensitive behavior.
- Keep dependencies minimal and justified.
- Do not introduce credentials, generated artifacts, or local
  virtual environments into Git.

## 7. Testing and Verification

Frontend:
- Run `npm run build`.
- Run `npm run lint`.
- Add appropriate automated tests as the test setup evolves.

Backend:
- Use pytest for automated tests.
- Test services independently from HTTP routes.
- Test request validation and failure scenarios.
- Use mocks for external downloads and media tools in unit tests.
- Do not require real downloads or network access in unit tests.

Run relevant checks after each meaningful change. Report skipped
checks and explain why they could not run.

## 8. Dependencies and Environment

- Inspect installed versions before changing dependencies.
- Do not recreate or replace virtual environments unnecessarily.
- Keep frontend lockfiles committed.
- Document backend dependencies and keep them reproducible.
- Update dependency manifests when adding or removing packages.
- Never commit `.env` files or machine-specific configuration.

## 9. Git Rules

- Inspect `git status` before editing.
- Never discard, reset, or overwrite user changes.
- Do not use destructive Git commands without explicit approval.
- Keep changes focused and review the final diff.
- Do not commit or push unless explicitly requested.
- Never claim a change is committed or deployed unless verified.

## 10. Definition of Done

A task is complete only when:

- Its acceptance criteria are satisfied.
- Relevant quality checks have been run.
- New behavior has appropriate tests where practical.
- Documentation is updated when necessary.
- The final diff contains no unrelated changes.
- Results, limitations, and remaining work are reported.
