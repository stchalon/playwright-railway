#!/bin/bash
playwright install --with-deps chromium
uvicorn app.main:app --host 0.0.0.0 --port $PORT
