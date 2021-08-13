#!/usr/bin/env bash
cd /usr/src/app
alembic upgrade head
uvicorn --host 0.0.0.0 --reload --log-level debug --app-dir . app.main:app