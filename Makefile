PYTHON ?= python3
SOURCE_VERSION := $(shell dpkg-parsechangelog -S Version | sed 's/-[^-]*$$//')
PREPARED_SOURCE ?= build/fonts-nerd-symbols-$(SOURCE_VERSION)/upstream-src

.PHONY: test test-prepared-source prepare-test-source test-integration test-repro

test:
	$(PYTHON) tests/test_repo.py

prepare-test-source:
	./debian/scripts/prepare-upstream "$(SOURCE_VERSION)" dfsg

test-prepared-source:
	$(PYTHON) tests/test_repo.py --prepared-source "$(PREPARED_SOURCE)"

test-integration:
	docker run --rm --privileged -v "$${PWD}:/src:ro" debian:unstable bash /src/tests/integration-debian.sh /src

test-repro:
	docker run --rm --device /dev/fuse --cap-add SYS_ADMIN --security-opt apparmor=unconfined -v "$${PWD}:/src:ro" debian:unstable bash /src/tests/reprotest-debian.sh /src
