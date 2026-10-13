# Security Requirements

## Input Validation

- Treat user input, external URLs, metadata, and filenames as untrusted.
- Allow only explicitly supported URL schemes and sources.
- Prevent server-side request forgery (SSRF), local-file access, path traversal, and command injection.
- Consider redirects, DNS rebinding, and internal network targets.
- Keep TLS certificate verification enabled.

## Media Processing

- Never build shell commands from user-controlled strings.
- Use safe subprocess APIs with execution timeouts.
- Enforce file-size, duration, concurrency, and resource limits.
- Isolate temporary files and clean them up reliably.
- Do not expose internal filesystem paths to clients.

## API Security

- Validate request data.
- Return safe, consistent error responses.
- Add rate limiting and job ownership controls before public deployment.
- Keep credentials out of source control.
- Configure production CORS explicitly.

## Media Rights

Only support operations permitted by applicable laws, platform terms, and the user's rights. Do not bypass DRM, paywalls, or access controls.

This document is a baseline, not a completed security audit.
