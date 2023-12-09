
# Use the official Node.js 14 image as the base image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package.json /app

# Install the app dependencies
RUN npm install

# Copy the rest of the app files to the working directory
COPY . /app

EXPOSE 5173

# Start the app
CMD ["npm", "run", "dev", "--", "--host"]
