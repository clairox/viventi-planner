# Pull official base image
FROM node:16.17.1

# Set working directory
WORKDIR /frontend

# Copy project into container
COPY . /frontend

# Install packages
RUN npm install

# Expose port
EXPOSE 5173

# Run app when container launches
CMD ["npm", "run", "dev", "--host"]