﻿#!/usr/bin/env bash
exec python -m uvicorn backend.server:app --host 0.0.0.0 --port ${PORT:-8001}