LINT_PATHS = telegram_handler/ tests/


lint:
	isort $(LINT_PATHS) --diff --check-only
	ruff $(LINT_PATHS)

format:
	isort $(LINT_PATHS)
	ruff $(LINT_PATHS) --fix
	black $(LINT_PATHS)
