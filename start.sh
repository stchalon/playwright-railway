#!/bin/bash
playwright install-deps
uvicorn app.main:app --host 0.0.0.0 --port $PORT