# Variables
PROJECT_NAME = cloudydad-data-center
PYTHON = python3
ROOT_DIR := $(CURDIR)
SHELL := /bin/bash

GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
CYAN   := $(shell tput -Txterm setaf 6)
RESET  := $(shell tput -Txterm sgr0)

.PHONY: all
all: help

## Init:
.PHONY: init
init: direnv ## initialize Python environment

.PHONY: direnv
direnv: ## setup direnv
	cp .envrc.sample .envrc && direnv allow .

.PHONY: install-uv
install-uv: ## install uv as a dependency for compile and install operations
	pip install uv

.PHONY: bw-auth
bw-auth: # Authenticate to Bitwarden
	NODE_OPTIONS="--no-deprecation" bw logout > /dev/null 2>&1
	NODE_OPTIONS="--no-deprecation" bw login --apikey > /dev/null 2>&1
	@CMD_OUTPUT=$$(NODE_OPTIONS="--no-deprecation" bw unlock --passwordenv BW_PASSWORD | grep --color=none 'export BW_SESSION' | awk -FBW_SESSION= '{print $$2}' | tr -d '"'); \
	if grep -q "BW_SESSION=" .env; then \
		awk -v var="export BW_SESSION" -v val="$$CMD_OUTPUT" 'BEGIN {FS=OFS="="} $$1==var {$$2=val} 1' .env > .env.tmp && mv .env.tmp .env; \
	else \
		echo "export BW_SESSION=$$CMD_OUTPUT" >> .env; \
	fi

## Compile:
.PHONY: compile
compile: compile-docs-reqs ## pip-compile requirements

.PHONY: compile-docs-reqs
compile-docs-reqs: requirements-docs.in ## pip-compile dev requirements
	uv pip compile --output-file=requirements-docs.txt requirements-docs.in

## Install:
.PHONY: install ## install dependencies
install: install-pip install-galaxy

.PHONY: install-pip
install-pip: ## pip-sync requirements
	uv pip sync requirements.txt

.PHONY: install-galaxy
install-galaxy: ## Install Ansible Galaxy roles
	uvx --from ansible-core ansible-galaxy install -r ./collections/requirements.yml
	uvx --from ansible-core ansible-galaxy collection install -r ./collections/requirements.yml

.PHONY: install-docs
install-docs: ## pip-sync requirements
	uv pip sync requirements-docs.txt

## Lint:
.PHONY: lint
lint: pre-commit ## Run all available linters

.PHONY: pre-commit
pre-commit:
	pre-commit run -a

## Test:
.PHONY: test
test: ## Run tests

## Docs:
.PHONY: docs
docs: install-docs ## Spin up docs site
	npx @techdocs/cli generate --no-docker && npx @techdocs/cli serve --no-docker

## Playbooks:
.PHONY: site
site: ## Deploy cloudydad-data-center
	uvx --from ansible-core ansible-playbook playbooks/site.yml

.PHONY: reset
reset: ## Reset Kubernetes cluster
	uvx --from ansible-core ansible-playbook playbooks/reset.yml

.PHONY: show-facts
show-facts: ## Show facts for cloudydad-data-center
	uvx --from ansible-core ansible-playbook playbooks/show-facts.yml

.PHONY: reboot
reboot: ## Reboot cloudydad-data-center
	uvx --from ansible-core ansible-playbook playbooks/reboot.yml

## Help:
.PHONY: help
help: ## Show this help.
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} { \
		if (/^[a-zA-Z_-]+:.*?##.*$$/) {printf "    ${YELLOW}%-20s${GREEN}%s${RESET}\n", $$1, $$2} \
		else if (/^## .*$$/) {printf "  ${CYAN}%s${RESET}\n", substr($$1,4)} \
		}' $(MAKEFILE_LIST)
