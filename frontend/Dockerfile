# Use official Node.js image
FROM node:20

# Set working directory
WORKDIR /usr/src/app

# Install dependencies first (for better Docker cache)
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the app
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start Vite dev server
CMD ["npm", "run", "dev", "--", "--host"]
