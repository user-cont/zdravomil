.PHONY: image-build build-test test-in-container test

IMAGE_NAME = docker.io/usercont/zdravomil
TEST_IMAGE_NAME = zdravomil-test

build:
	docker-compose build

bot-start:
	docker-compose up zdravomil

bot-start-with-redis: build
	docker-compose up

stop:
	docker-compose stop

build-test: build
	docker build . --tag=${TEST_IMAGE_NAME} -f Dockerfile.test

test-in-container: build-test
	docker run ${TEST_IMAGE_NAME}

test:
	DEPLOYMENT=test pytest --color=yes --verbose --showlocals
