# Use official Node image
FROM node:18

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install

# Copy all other frontend files
COPY . .

# Start the app
CMD ["npm", "start"]
