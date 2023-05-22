PROJECT_NAME = $(notdir ${PWD})
PROJECT_NAME := $(shell echo ${PROJECT_NAME} | tr A-Z a-z)

ENV ?= dev
export ENV

TARGET_TEST=$(if ${TEST},${TEST},tests/)
COV=$(if ${TEST},,--cov=load.py --cov-report=term)

COV=$(if ${TEST},,--cov=load)

help:
	@echo
	@echo "help"
	@echo "       Print this help"
	@echo

	@echo "init"
	@echo "       Initialise dependencies to test and run the application."
	@echo

	@echo "check"
	@echo "       Run static analysis"
	@echo

	@echo "test"
	@echo "       Run unit tests with coverage. \
Use TEST=/path/to/test to run a specific test."
	@echo

	@echo "commit"
	@echo "       Write commit message according to the Conventional Commits specification. \
Use \"|\" as the newline character in multiline commit comments."
	@echo

	@echo "show_current_version":
	@echo "       Show current version."
	@echo

	@echo "bump_prerelease_preview"
	@echo "       Bump to a prerelease or bump an existing prerelease preview (current prerelease \
tag can be changed in file pyproject.toml)."
	@echo

	@echo "bump_prerelease"
	@echo "       Bump to a prerelease or bump an existing prerelease (current prerelease \
tag can be changed in file pyproject.toml)."
	@echo

	@echo "bump_release_preview"
	@echo "       Bump to a release or bump an existing release preview."
	@echo

	@echo "bump_release"
	@echo "       Bump to a release or bump an existing release."
	@echo

	@echo "changelog"
	@echo "       Create/recreate CHANGELOG.md file (without commiting)."
	@echo

	@echo "run"
	@echo "       Run the application."
	@echo

	@echo "build"
	@echo "       Build docker image."
	@echo

commitizen:
	@source .venv/bin/activate && cz check --allow-abort --commit-msg-file .git/COMMIT_EDITMSG && deactivate

commit:
	@source .venv/bin/activate && cz commit && deactivate

show_current_version:
	@source .venv/bin/activate && semantic-release --current print-version && deactivate
	@echo

bump_prerelease_preview:
	@source .venv/bin/activate && semantic-release --noop --prerelease version && deactivate
	@echo

bump_prerelease:
	@source .venv/bin/activate && semantic-release --prerelease version && deactivate
	@echo

bump_release_preview:
	@source .venv/bin/activate && semantic-release --noop version && deactivate
	@echo

bump_release:
	@source .venv/bin/activate && semantic-release version && deactivate
	@echo

changelog:
	@source .venv/bin/activate && cz changelog && deactivate

# When running in an Jenkins environment git hooks will not be installed.
# Variable RUN_BY_JENKINS is set at the begining of each pipeline to
# signal that we are running in a Jenkins environment.
init:
	@python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -r requirements_dev.txt && deactivate
ifndef RUN_BY_JENKINS
	@source .venv/bin/activate && pre-commit install --hook-type commit-msg && deactivate
else
ifneq (${RUN_BY_JENKINS},TRUE)
	@source .venv/bin/activate && pre-commit install --hook-type commit-msg && deactivate
endif
endif

check:
	@source .venv/bin/activate && python3 -m flake8 load.py tests/ && deactivate

build:
	@docker build . -t ${PROJECT_NAME}-${ENV} ${DOCKER_BUILD_ARGS}

test:
	@source .venv/bin/activate && pytest ${COV} ${TARGET_TEST} && deactivate

run:
	@source .venv/bin/activate && python3 -m app && deactivate

.PHONY: help init check build test functional_test run
