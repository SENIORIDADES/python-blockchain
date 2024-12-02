#!/bin/bash
chown  -R 1000:1000 /app/database
source venv/bin/activate
exec "$@"
