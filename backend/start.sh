#!/usr/bin/env bash
exec uvicorn backend.server:app --host 0.0.0.0 --port 
