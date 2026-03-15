# Stage 1: Build the React application
FROM node:20-alpine as build

WORKDIR /app

# The frontend code
COPY package.json .
# We will do an npm install directly
RUN npm install

# Because we manually copied files, copy src and pub
COPY . .
RUN npm run build

# Stage 2: Serve via Nginx
FROM nginx:alpine

# Copy built assets
COPY --from=build /app/dist /usr/share/nginx/html

# Replace default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
