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
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/[:].*[##]/:\n\t/'

install: cmd-exists-brew ## Install dependencies
	pip install ruff pytest cfn-lint
	brew install watchman

start-services: ## Start the Docker container services
	docker-compose --env-file ./config/.env up -d

stop-services: ## Stop the Docker container services
	docker-compose down

build-scaffold: ## Build a terraform scaffold to mimic an existing environment
	cd ./local_scaffold; tflocal init; tflocal apply -auto-approve

destroy-scaffold: ## Destroy terraform scaffold
	# cd ./local_scaffold; tflocal init; tfloc.al destroy -auto-approve

test: ## Run the tests
	pytest --continue-on-collection-errors -rPp --cov=. --cov-report term-missing

rebuild: ## Rebuild the Docker container services and SAM application
	rm -Rf .aws-sam
	docker compose down
	docker compose up -d
	# samlocal validate --lint
	cfn-lint template.yaml --ignore-checks W1001 W8001 W2001
	samlocal build
	python utils/bootstrap_layers.py	
	samlocal deploy \
            --config-env local \
            --no-fail-on-empty-changeset \
            --no-confirm-changeset \
            --resolve-s3 \
            --region eu-west-2

redeploy: ## Rebuild the Docker container services and SAM application
	samlocal deploy \
            --config-env local \
            --no-fail-on-empty-changeset \
            --no-confirm-changeset \
            --resolve-s3 \
            --region eu-west-2

make run: ## Run lambdas locally
	export PYTHONPATH=./src/boilerplate && \
	python -m run_lambda

watch: ## Rebuild or redeploy when files changes along with running lambda
	watchman-make -p "**/template/*.py" -t redeploy run -p "**/boilerplate/*.py" -t rebuild run

clean: ## format python file and does flake8 fixes
	ruff check . --fix
