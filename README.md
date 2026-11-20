# Flask Application Containerization with Docker

## Project Overview

This project demonstrates the containerization of a Python Flask web application using Docker.

The objective of the project is to package a Flask application and all of its dependencies into a portable Docker image, run the application inside a Docker container, expose the application to the host machine through port mapping, manage the container lifecycle, monitor application logs, and optimize the Docker build process.

The project demonstrates the following Docker concepts:

- Preparing a Flask application for containerization
- Creating and configuring a Dockerfile
- Building Docker images
- Running Docker containers
- Docker port mapping
- Container lifecycle management
- Container log monitoring
- Docker image optimization
- Docker layer caching
- Using `.dockerignore`
- Testing a containerized Flask application

---

## Project Structure

The project repository contains the following files:

```text
flask-docker-project/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
└── screenshots/
    └── flask-app-running.png
```

### File Descriptions

| File | Description |
|---|---|
| `app.py` | Contains the Python Flask web application |
| `requirements.txt` | Contains the Python packages required by the application |
| `Dockerfile` | Defines the instructions used to build the Docker image |
| `.dockerignore` | Prevents unnecessary files from being included in the Docker build context |
| `.gitignore` | Prevents local development files such as virtual environments from being committed to Git |
| `README.md` | Documents the project, commands, configuration, and testing process |
| `screenshots/` | Contains evidence of the Flask application successfully running |

---

# 1. Flask Application

The Flask application is defined in `app.py`.

The application has two routes:

- `/` - Displays a message confirming that the Flask Docker application is running.
- `/health` - Provides a simple JSON health-check endpoint.

Example application configuration:

```python
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Flask Docker Application</h1>
    <p>The application is running successfully inside a Docker container.</p>
    """


@app.route("/health")
def health():
    return jsonify(
        status="healthy",
        message="Flask application is running"
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

The Flask server listens on:

`0.0.0.0:5000`

Using `0.0.0.0` is important in a containerized environment because it allows the application to accept connections coming from outside the container.

---

# 2. Application Dependencies

Python dependencies are stored in the `requirements.txt` file.

Example:

```text
Flask==3.1.2
gunicorn==23.0.0
```

Flask provides the web application framework, while Gunicorn is used to serve the Flask application inside the Docker container.

The dependencies can be installed locally using:

```bash
pip install -r requirements.txt
```

---

# 3. Local Application Testing

Before building the Docker image, the Flask application was tested locally.

A Python virtual environment was created:

```bash
python3 -m venv venv
```

The environment was activated using:

```bash
source venv/bin/activate
```

The application dependencies were installed using:

```bash
pip install -r requirements.txt
```

The application was then started:

```bash
python app.py
```

The health endpoint was tested using:

```bash
curl http://localhost:5000/health
```

A successful response confirms that the Flask application is functioning correctly before containerization.

Example response:

```json
{
  "message": "Flask application is running",
  "status": "healthy"
}
```

---

# 4. Dockerfile

The Dockerfile defines the steps required to package the Flask application into a Docker image.

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

## Dockerfile Explanation

### Base Image

```dockerfile
FROM python:3.13-slim
```

The application uses the lightweight Python slim image rather than the full Python image. This helps reduce the final Docker image size.

### Environment Configuration

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```

`PYTHONDONTWRITEBYTECODE=1` prevents Python from creating unnecessary `.pyc` bytecode files.

`PYTHONUNBUFFERED=1` ensures that application output is immediately sent to container logs.

### Working Directory

```dockerfile
WORKDIR /app
```

This creates and sets `/app` as the working directory inside the Docker image.

### Dependency Installation

```dockerfile
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
```

The dependency file is copied separately and the required Python packages are installed.

Copying `requirements.txt` before the source code also improves Docker layer caching.

### Copy Application Source Code

```dockerfile
COPY app.py .
```

The Flask application is copied into the container.

### Expose Flask Port

```dockerfile
EXPOSE 5000
```

This documents that the application listens on TCP port `5000` inside the container.

### Application Startup

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

Gunicorn starts the Flask application and listens on port `5000`.

---

# 5. Docker Ignore Configuration

A `.dockerignore` file is included to prevent unnecessary files from being sent to the Docker daemon during the image build.

Example `.dockerignore`:

```text
.git
.gitignore
__pycache__
*.pyc
*.pyo
*.pyd
.env
venv
.venv
README.md
Dockerfile*
docker-compose*.yml
```

This helps reduce the Docker build context and prevents unnecessary development files from being added to the image.

---

# 6. Building the Docker Image

The Docker image is built from the Dockerfile using:

```bash
docker build -t flask-docker-app:1.0 .
```

The command performs the following actions:

- Reads the Dockerfile
- Downloads the required Python base image if necessary
- Sets the container working directory
- Installs the Python dependencies
- Copies the application source code
- Creates the final Docker image
- Tags the image as `flask-docker-app:1.0`

The image can be verified using:

```bash
docker image ls
```

or:

```bash
docker images
```

The image can also be inspected with:

```bash
docker image inspect flask-docker-app:1.0
```

---

# 7. Running the Docker Container

The application container is started using:

```bash
docker run -d --name flask-container -p 8080:5000 flask-docker-app:1.0
```

### Command Explanation

`docker run` creates and starts a new container.

`-d` runs the container in detached mode.

`--name flask-container` assigns the name `flask-container` to the container.

`-p 8080:5000` maps TCP port `8080` on the host machine to TCP port `5000` inside the container.

`flask-docker-app:1.0` specifies the Docker image used to create the container.

The port mapping can therefore be represented as:

```text
Host Port 8080 → Container Port 5000
```

---

# 8. Verifying the Running Container

Running containers can be viewed using:

```bash
docker ps
```

All containers, including stopped containers, can be displayed using:

```bash
docker ps -a
```

The configured port mapping can also be checked using:

```bash
docker port flask-container
```

---

# 9. Accessing the Flask Application

After the container starts successfully, the application can be accessed using a web browser.

Navigate to:

```text
http://localhost:8080
```

The browser should display:

> Flask Docker Application  
> The application is running successfully inside a Docker container.

The health endpoint can be accessed at:

```text
http://localhost:8080/health
```

It can also be tested from the command line:

```bash
curl http://localhost:8080/health
```

A successful response should be similar to:

```json
{
  "message": "Flask application is running",
  "status": "healthy"
}
```

This confirms that Docker port mapping is working and the Flask application running inside the container is accessible from the host machine.

---

# 10. Container Lifecycle Management

Docker commands were used to practice managing the complete lifecycle of the container.

## Stop the Container

```bash
docker stop flask-container
```

## Start the Container Again

```bash
docker start flask-container
```

## Restart the Container

```bash
docker restart flask-container
```

## Check Container Status

```bash
docker ps -a
```

## Remove the Container

The container must be stopped before normal removal:

```bash
docker stop flask-container
docker rm flask-container
```

Alternatively, it can be forcefully stopped and removed using:

```bash
docker rm -f flask-container
```

---

# 11. Monitoring Container Logs

Application logs can be viewed with:

```bash
docker logs flask-container
```

Logs can be monitored continuously using:

```bash
docker logs -f flask-container
```

The most recent log entries can be displayed with:

```bash
docker logs --tail 20 flask-container
```

Logs with timestamps can be displayed using:

```bash
docker logs --timestamps flask-container
```

Container logs are useful when troubleshooting application startup errors, web requests, crashes, or configuration problems.

---

# 12. Container Inspection and Monitoring

Detailed container configuration can be viewed using:

```bash
docker inspect flask-container
```

Live CPU, memory, network, and container resource utilization can be viewed with:

```bash
docker stats flask-container
```

A shell can also be opened inside the running container:

```bash
docker exec -it flask-container sh
```

Once inside the container, commands such as the following can be used:

```bash
pwd
ls -la
```

The container shell can be closed using:

```bash
exit
```

---

# 13. Docker Image Optimization

Several techniques are used to reduce image size and improve build efficiency.

## Lightweight Base Image

The Dockerfile uses:

```dockerfile
FROM python:3.13-slim
```

The slim variant contains fewer unnecessary operating-system packages than the full Python image.

## Docker Layer Caching

The dependency file is copied before the application source:

```dockerfile
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
```

Docker can therefore reuse the dependency installation layer when `app.py` changes but `requirements.txt` remains unchanged.

This can significantly improve rebuild times during development.

## Pip Cache Reduction

Dependencies are installed using:

```bash
pip install --no-cache-dir -r requirements.txt
```

The `--no-cache-dir` option prevents pip's download cache from being stored in the Docker image.

## Docker Ignore

The `.dockerignore` file reduces the build context by preventing unnecessary files, such as virtual environments and Git metadata, from being transferred during the Docker build.

---

# 14. Testing Docker Layer Caching

The first image is built using:

```bash
docker build -t flask-docker-app:1.0 .
```

The image can then be rebuilt:

```bash
docker build -t flask-docker-app:1.1 .
```

If the dependencies have not changed, Docker can reuse previously cached layers.

After changing only `app.py`, another version can be built:

```bash
docker build -t flask-docker-app:1.2 .
```

Docker should continue to reuse the dependency-installation layer because `requirements.txt` has not changed.

A completely fresh build can be performed using:

```bash
docker build --no-cache -t flask-docker-app:clean .
```

---

# 15. Viewing Docker Image Layers

The image history can be viewed using:

```bash
docker history flask-docker-app:1.0
```

This displays the layers that were used to construct the final Docker image.

The image size can be checked using:

```bash
docker image ls flask-docker-app:1.0
```

---

# 16. Git Configuration

Local development files should not be stored in the Git repository.

The `.gitignore` file contains entries such as:

```text
venv/
.venv/
__pycache__/
*.pyc
.env
```

This prevents the Python virtual environment, Python cache files, and local environment variables from being committed.

---

# 17. Git Workflow

The repository can be initialized using:

```bash
git init
git branch -M main
```

Project files are staged using:

```bash
git add .
```

Changes are committed using:

```bash
git commit -m "Complete Flask Docker containerization project"
```

The repository can then be connected to GitHub:

```bash
git remote add origin YOUR_GITHUB_REPOSITORY_URL
```

The configured remote can be verified using:

```bash
git remote -v
```

The project is pushed to GitHub using:

```bash
git push -u origin main
```

After the initial push, future changes can normally be uploaded with:

```bash
git add .
git commit -m "Update Flask Docker project"
git push
```

---

# 18. Troubleshooting

## Flask Module Not Found

During local testing, the following error can occur:

```text
ModuleNotFoundError: No module named 'flask'
```

This means Flask is not installed in the Python environment being used.

The issue can be resolved by activating the virtual environment:

```bash
source venv/bin/activate
```

Then installing the dependencies:

```bash
pip install -r requirements.txt
```

Flask installation can be verified using:

```bash
pip show Flask
```

The application can then be started again:

```bash
python app.py
```

---

## Container Name Already Exists

If Docker reports that `flask-container` already exists, check existing containers:

```bash
docker ps -a
```

Remove the old container:

```bash
docker rm -f flask-container
```

Then run the new container:

```bash
docker run -d --name flask-container -p 8080:5000 flask-docker-app:1.0
```

---

## Unable to Access localhost:8080

Check whether the container is running:

```bash
docker ps
```

Check the logs:

```bash
docker logs flask-container
```

Check the configured port mapping:

```bash
docker port flask-container
```

Test the endpoint:

```bash
curl http://localhost:8080
```

---

# 19. Screenshot Evidence

The `screenshots` directory contains evidence that the Flask application is successfully running inside the Docker container and is accessible through the mapped host port.

The main screenshot should show the Flask application running in a web browser at:

```text
http://localhost:8080
```

Screenshot location:

```text
screenshots/flask-app-running.png
```

The screenshot demonstrates that:

- The Docker container started successfully.
- The Flask application is running inside the container.
- Container port `5000` has been successfully mapped to host port `8080`.
- The application can be accessed from a web browser on the host machine.

If the screenshot has been committed to the repository, it can also be displayed directly in this README using:

![Flask Application Running](screenshots/flask-app-running.png)

---

# 20. Useful Docker Commands

| Task | Command |
|---|---|
| Build image | `docker build -t flask-docker-app:1.0 .` |
| List images | `docker image ls` |
| Run container | `docker run -d --name flask-container -p 8080:5000 flask-docker-app:1.0` |
| List running containers | `docker ps` |
| List all containers | `docker ps -a` |
| View logs | `docker logs flask-container` |
| Follow logs | `docker logs -f flask-container` |
| Stop container | `docker stop flask-container` |
| Start container | `docker start flask-container` |
| Restart container | `docker restart flask-container` |
| Remove container | `docker rm -f flask-container` |
| Inspect container | `docker inspect flask-container` |
| Check port mapping | `docker port flask-container` |
| Monitor resources | `docker stats flask-container` |
| Open container shell | `docker exec -it flask-container sh` |
| View image layers | `docker history flask-docker-app:1.0` |
| Remove image | `docker image rm flask-docker-app:1.0` |

---

# 21. Project Requirements Completed

The project demonstrates the following required tasks:

- [x] Prepared a Flask web application for containerization
- [x] Created a `requirements.txt` file
- [x] Created a Dockerfile
- [x] Used a lightweight Python base image
- [x] Installed Python dependencies inside the Docker image
- [x] Built a Docker image
- [x] Verified the Docker image
- [x] Created and started a Docker container
- [x] Mapped host port `8080` to container port `5000`
- [x] Accessed the Flask application through the mapped host port
- [x] Practiced stopping and starting containers
- [x] Practiced restarting and removing containers
- [x] Monitored application output using Docker logs
- [x] Used `.dockerignore` to reduce the Docker build context
- [x] Optimized the Dockerfile for Docker layer caching
- [x] Used a slim Python base image to reduce image size
- [x] Included screenshot evidence of the running Flask application
- [x] Documented the build and run commands

---

# Conclusion

This project demonstrates the complete process of containerizing a Python Flask web application using Docker.

The Flask application was first prepared and tested locally before being packaged into a Docker image. A Dockerfile was created to configure the Python environment, install application dependencies, copy the application source code, expose the Flask port, and launch the application using Gunicorn.

The Docker image was then built and used to create a container. Port mapping was configured so that the Flask application running on port `5000` inside the container could be accessed through port `8080` on the host machine.

The project also demonstrates Docker container lifecycle management, log monitoring, container inspection, image versioning, Docker layer caching, `.dockerignore` usage, and image optimization with a lightweight Python base image.

The completed project provides a repeatable and portable method for running the Flask application in a containerized environment.
