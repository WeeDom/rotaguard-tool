# Deployment Guide: rotaguard-tool

This guide describes how to deploy the Flask API and React frontend as separate services, suitable for modern CI/CD pipelines and scalable production environments.

---

## 1. Overview
- **Backend:** Flask REST API (Dockerized)
- **Frontend:** React (Vite) static build (Dockerized or hosted on CDN/static host)
- **Recommended:** Deploy each as its own service/container. Use a reverse proxy (e.g., Nginx) to route traffic.

---

## 2. Backend (Flask API)

### Build Docker Image
```bash
docker build -t rotaguard-backend .
```

### Run Container
```bash
docker run -d --name rotaguard-backend -p 5000:5000 \
  --env-file .env \
  rotaguard-backend
```
- Exposes API at `http://<host>:5000/api/`
- Use environment variables for secrets/configuration.

### Example CI/CD Steps
- Lint, test, and build Docker image.
- Push to registry (e.g., Docker Hub, GHCR).
- Deploy to server/VM/container service.

---

## 3. Frontend (React/Vite)

### Build Static Files
```bash
cd frontend
npm install
npm run build
```
- Output is in `frontend/dist/`

### Deploy Static Files
- **Option 1:** Upload `dist/` to a CDN/static host (Netlify, Vercel, S3+CloudFront, Azure Static Web Apps, etc.)
- **Option 2:** Serve with Nginx or Caddy on your own server.

#### Example Nginx Config
```
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/html; # where you put frontend/dist
    location / {
        try_files $uri /index.html;
    }
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Example CI/CD Steps
- Lint, test, and build React app.
- Deploy `dist/` to static host or server.

---

## 4. Environment Variables
- Use `.env` files for secrets and config (never commit secrets to git).
- Set API base URL in React using Vite env vars (e.g., `VITE_API_URL`).

---

## 5. Production Checklist
- [ ] Use HTTPS (TLS certs via Let's Encrypt, etc.)
- [ ] Set secure, unique secrets for Flask
- [ ] Use a production-ready WSGI server (e.g., Gunicorn) for Flask
- [ ] Enable CORS as needed
- [ ] Monitor logs and errors
- [ ] Automate with CI/CD (GitHub Actions, GitLab CI, etc.)

---

## 6. Example Directory Structure
```
rotaguard-tool/
  app/           # Flask backend
  frontend/      # React frontend
  Dockerfile     # For backend
  docker-compose.yml (dev only)
  ...
```

---

## 7. Resources
- [Docker Docs](https://docs.docker.com/)
- [Vite Docs](https://vitejs.dev/)
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)
- [Nginx Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Netlify](https://www.netlify.com/), [Vercel](https://vercel.com/), [AWS S3](https://aws.amazon.com/s3/)

---

**Tip:**
- Use Docker Compose for local development only. For production, deploy each stack as its own service/container.
- Keep secrets out of git. Use CI/CD secrets or environment variables.
