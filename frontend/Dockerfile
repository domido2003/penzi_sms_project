# Use Node.js for development
FROM node:18

# Set working directory inside container
WORKDIR /app

# Install dependencies first (cache layer)
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the app
COPY . .

# Expose React development port
EXPOSE 3000

# Run development server
CMD ["npm", "start"]
