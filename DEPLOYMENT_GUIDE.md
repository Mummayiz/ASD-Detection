# ASD Detection Application - Deployment Guide

## Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- MongoDB (local or remote)
- 2GB RAM minimum

## Environment Files

### Backend `.env` file (already included)
Location: `/app/backend/.env`
```
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"
CORS_ORIGINS="*"
```

### Frontend `.env` file (already included)
Location: `/app/frontend/.env`
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

## Deployment Steps

### 1. Backend Deployment

```bash
cd backend/
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001
```

### 2. Frontend Deployment

```bash
cd frontend/
yarn install
yarn build
# Serve the build folder using nginx or any static file server
```

### 3. Using Supervisor (Recommended for Production)

The application is configured with supervisor for process management:

```bash
sudo supervisorctl start backend
sudo supervisorctl start frontend
```

### 4. Docker Deployment (Optional)

Create `Dockerfile` for backend:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

### 5. Environment Variables for Production

Update the `.env` files for your production environment:

**Backend `.env`:**
```
MONGO_URL="mongodb://your-mongo-host:27017"
DB_NAME="asd_detection_prod"
CORS_ORIGINS="https://your-frontend-domain.com"
```

**Frontend `.env`:**
```
REACT_APP_BACKEND_URL=https://your-backend-domain.com
```

## Required Files Structure
```
/app/
├── backend/
│   ├── .env                 ← Environment variables
│   ├── requirements.txt     ← Python dependencies  
│   ├── server.py           ← FastAPI application
│   └── models/             ← ML model files
├── frontend/
│   ├── .env                ← Environment variables
│   ├── package.json        ← Node dependencies
│   └── src/                ← React source code
└── models/                 ← Trained ML models
```

## Health Checks

- Backend: `GET http://localhost:8001/health`
- Frontend: `GET http://localhost:3000`

## Database Setup

MongoDB will be automatically configured. The application creates collections as needed:
- `assessments` - Store assessment results
- Database name from `DB_NAME` environment variable

## Security Considerations

1. Update CORS_ORIGINS to specific domains in production
2. Use HTTPS in production
3. Set up proper MongoDB authentication
4. Consider rate limiting for API endpoints

## Troubleshooting

- Check logs: `/var/log/supervisor/backend.*.log`
- Verify MongoDB connection: Check MONGO_URL in .env
- Test API: `curl http://localhost:8001/health`