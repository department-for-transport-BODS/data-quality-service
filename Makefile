ifneq (,$(wildcard ./config/.env))
    include ./config/.env
    export
endif

ENV?=local
DIRNAME=`basename ${PWD}`
PG_EXEC=psql "host=$(POSTGRES_HOST) port=$(POSTGRES_PORT) user=$(POSTGRES_USER) password=$(POSTGRES_PASSWORD) gssencmode='disable'

cmd-exists-%:
	@hash $(*) > /dev/null 2>&1 || \
		(echo "ERROR: '$(*)' must be installed and available on your PATH."; exit 1)

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/[:].*[##]/:/'

start-services: ## Start the Docker container services
	docker-compose --env-file ./config/.env up -d

stop-services: ## Stop the Docker container services
	docker-compose down

build-scaffold: ## Build a terraform scaffold to mimic an existing environment
	cd ./local_scaffold; tflocal init; tflocal apply -auto-approve

destroy-scaffold: ## Destroy terraform scaffold
	cd ./local_scaffold; tflocal init; tflocal destroy -auto-approve

test: ## Run the tests
	pytest --continue-on-collection-errors -rPp --cov=. --cov-report term-missing

rebuild-local: ## Rebuild the Docker container services and SAM application
	rm -Rf .aws-sam 
	# pip install -q -r utils/requirements.txt
	docker-compose down
	docker-compose up -d
	samlocal build
	python utils/bootstrap_layers.py
	samlocal deploy \
            --stack-name local \
            --no-fail-on-empty-changeset \
            --no-confirm-changeset \
            --resolve-s3 \
            --capabilities CAPABILITY_IAM \
						--region eu-west-2

make local-run: ## Run lambdas locally
	export PYTHONPATH=./src/boilerplate && \
	export POSTGRES_HOST=localhost && \
	export POSTGRES_PASSWORD=postgres && \
	export POSTGRES_PORT=5432 && \
	export POSTGRES_USER=postgres && \
	export POSTGRES_DB=bodds && \
	echo "${POSTGRES_USER}" && \
	python -c 'from src.template.app import lambda_handler; from json import dumps; lambda_handler({"Records":[{"body": dumps({"file_id": 1,"check_id": 1,"result_id": 1})}]},None)'

