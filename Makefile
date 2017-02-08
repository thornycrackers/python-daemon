.PHONY: build

IMAGENAME=thornycrackers/python_daemon
CONTAINERNAME=python_daemon

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build the Docker image
	docker build -t $(IMAGENAME) ./build

up: build  ## Bring the Docker container up
	docker run -dP -v $(CURDIR):/app --name $(CONTAINERNAME) $(IMAGENAME) /bin/bash -c '/opt/entry.sh'

down: ## Stop the Docker container
	docker stop $(CONTAINERNAME) || echo 'No container to stop'

enter: ## Enter the running Docker container
	docker exec -it $(CONTAINERNAME) /bin/bash

clean: down ## Remove the Docker image and any stopped containers
	docker rm $(CONTAINERNAME) || echo 'No container to remove'
