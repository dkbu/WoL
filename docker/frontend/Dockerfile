FROM node:22-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage: serve static files with nginx
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# Replace default nginx config to proxy /api to the backend
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
