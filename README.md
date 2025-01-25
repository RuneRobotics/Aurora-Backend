# Aurora Setup Instructions


This guide will help you set up and run the Aurora app in a Docker container.


## Prerequisites:
- Docker
- Docker Compose


## Steps to Set Up and Run:


1. **Clone the Repository**:
   - Clone this repository to your local machine:
     ```bash
     git clone https://github.com/your-repo/aurora.git
     cd aurora
     ```


2. **Build and Start the Docker Container**:
   - Build the Docker image and start the container:
     ```bash
     docker-compose up --build
     ```


   This will:
   - Build the image using the `Dockerfile`.
   - Start the container in an idle state (it won’t run the app automatically).


3. **Enter the Running Container**:
   - After the container is running, enter the container's terminal:
     ```bash
     docker exec -it aurora_aurora_1 bash
     ```
   - The name `aurora_aurora_1` comes from the combination of your project name and service name in the `docker-compose.yml` file.


4. **Run the App Manually**:
   - Inside the container, manually run your Python script:
     ```bash
     python filename.py
     ```


5. **Access the App**:
   - Your app should now be running at `http://localhost:5900` (or the port you've configured).
   - Open your browser and visit `http://localhost:5900` to see the app in action.


6. **Stop the Container**:
   - Once you’re done, you can stop the container:
     ```bash
     docker-compose down
     ```


---


## Notes:
- The `docker-compose.yml` file mounts your local `aurora` directory into the container, so any changes you make locally will immediately be reflected in the container.
- You can view logs or access the container at any time using `docker exec`.
- For debugging, you can run commands like:
  ```bash
  docker-compose logs
