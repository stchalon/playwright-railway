#!/bin/bash
playwright install-deps
playwright install
uvicorn app.main:app --host 0.0.0.0 --port $PORT