general = cd jetCDNparse && uv run main.py

ruff = uvx ruff

all: format run

check:
	${ruff} check
	${ruff} format --check
format:
	${ruff} check --fix
	${ruff} format

run:
	${general}
run_force:
	${general} --force

server_test:
	cd dist && uv run python -m http.server
