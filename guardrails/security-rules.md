# Security Rules

- Never commit licenses, secrets, `.secrets/`, `license/`, `*.lic`, or `*.lic_base64`.
- Do not print secret contents into logs, patches, or generated reports.
- Treat production input files as sensitive unless the task explicitly says otherwise.
- Avoid adding commands that upload run data or secrets anywhere outside the local environment.
- When using Docker, mount only the paths required for the task.
- If a change depends on private runtime paths or credentials, document the dependency without embedding the secret itself.
