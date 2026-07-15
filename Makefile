general = cd jetCDNparse && uv run main.py

ruff = uv run --dev -m ruff

all: format run

check:
	${ruff} check
	${ruff} format --check
format:
	${ruff} format
	${ruff} check --fix

run:
	${general}
run_force:
	${general} -f

server_test:
	cd dist && uv run -m http.server
