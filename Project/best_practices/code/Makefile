# Need to specify bash in order for conda activate to work.
SHELL=/bin/bash

# LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_TAG:=2022-09-10-23-25
LOCAL_IMAGE_NAME:=batch-model-energy-usage:${LOCAL_TAG}

test:
	pytest tests/

integration_test: test
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash integration-test/run.sh

quality_checks: integration_test
	isort .
	black .
	pylint --recursive=y .

build: quality_checks
	docker build -t ${LOCAL_IMAGE_NAME} .

#integration_test: build
#	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash integration-test/run.sh

publish: build integration_test
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash scripts/publish.sh

setup:
	pipenv install --dev
	pre-commit install
