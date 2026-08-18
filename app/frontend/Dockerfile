# Estágio 1: Compilação de Assets Estáticos via Node LTS Recente
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build


# Estágio 2: Distribuição Estática via Nginx Estável Ultra Leve
FROM nginx:stable-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
