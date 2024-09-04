# python lint makefile

lint_line_length := 120
lint_python_version := 310
max_complexity := 12

ISORT_OPTS = --py $(lint_python_version) --profile black
BLACK_OPTS = --target-version py$(lint_python_version) --line-length $(lint_line_length)
FLAKE8_OPTS = --max-line-length $(lint_line_length) --max-complexity $(max_complexity)

export ISORT_OPTS
export BLACK_OPTS
export FLAKE8_OPTS

.fmt: $(python_src)
	isort $(ISORT_OPTS) $(src_dirs)
	fix -- black $(BLACK_OPTS) $(src_dirs)
	fix -- flake8 $(FLAKE8_OPTS) $(src_dirs)
	touch $@

### format source and lint
fmt: .fmt

### vim autofix
fix: .fmt

lint-clean:
	rm -f .fmt

lint-sterile:
	@:
