# Stage 1: build React frontend
FROM node:18 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .

# inject frontend env at build time
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL

RUN npm run build

# Stage 2: build Python app and include frontend build
FROM python:3.13-slim
WORKDIR /app

# # system deps for some Python packages (optional - add if you need build tools)
# RUN apt-get update && apt-get install -y build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*


# copy python requirements (assumes requirements.txt at repo root)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy backend code
COPY backend/ ./backend/

# copy frontend build produced in stage 1 into /app/frontend/build
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Expose default (Render will provide PORT env var)
EXPOSE 8000


# Start the uvicorn server. Use ${PORT:-8000} so Render's $PORT is used when available.
ENTRYPOINT ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2"]