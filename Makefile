# Quality gates — mirror of .github/workflows/quality.yml. Run `make grade` before every PR.
# `test` inherits pyproject addopts (-m 'not live and not arena'); the heavy
# strategy-measurement evals are `make test-arena` (ADR-0018 — mandatory before
# merging any strategy change; CI twin is the on-demand arena.yml workflow).

.PHONY: lint format-check type test test-arena sizes patterns hardcoded sync-verify submission grade

lint:
	uv run ruff check .

format-check:
	uv run ruff format --check .

type:
	uv run mypy src/

test:
	uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=85

test-arena:
	uv run pytest -n auto --dist loadscope -m "arena and not live" -v

sizes:
	uv run python scripts/check_file_sizes.py

patterns:
	uv run python scripts/check_anti_patterns.py

hardcoded:
	uv run python scripts/check_no_hardcoded.py

sync-verify:
	uv run python scripts/sync_core.py --verify

submission:
	uv run python scripts/check_submission.py

grade: lint format-check type sizes patterns hardcoded sync-verify test submission
	uv run python scripts/self_grade.py --validate
	@echo "ALL GATES GREEN"
