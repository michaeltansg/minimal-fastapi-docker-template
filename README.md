# minimal-fastapi-docker-template
A template for FastAPI with Docker and Dev Containers.

## Getting started
1. Create a `.env` file.
2. Rename the service `app` and modify the container_name value (`fastapi-server`) in docker-compose.yml file as appropriate.
3. Start the container using: `docker compose up -d`
4. Check the service is running. The following are expected behaviour:

```bash
$ curl http://localhost:8000/api/v1/health/
{"now":xxxxxx}
```

### OpenAPI documentation endpoints:
http://localhost:8000/api/v1/docs
http://localhost:8000/api/v1/redoc

The project is being watched for changes and any saved modifications will cause the app to be reloaded.

### Building and distribution
Firstly, modify Makefile with the appropriate image name.
```
docker login
docker buildx create --use
```
To create an image for distribution, modify the `Dockerfile` (if required) and then execute: `make push`

Other examples of use of Makefile:
```
make build IMAGE_NAME=mycustomimage TAG=v1.0
make push IMAGE_NAME=mycustomimage TAG=v1.0 PLATFORM=linux/arm64
```

---

To install python packages on host:
```bash
python -m venv venv;. venv/bin/activate; pip install -U pip
pip install -r requirements.txt
```

If more packages are added to requirements.txt, execute the following: `docker compose up --build -d` to rebuild the docker image and start a new container.

To start debugging:
1. Add port 5678:5678 to docker compose file.
2. place the following in the code where you wish to begin debugging:
```
import debugpy

debugpy.listen(("0.0.0.0", 5678))
print("Waiting for client to attach...")
debugpy.wait_for_client()
```