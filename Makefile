default: build

run: build
	docker run --name idoven-challenge --rm -p 3000:80 idoven-challenge

tests: build
	docker run -e APP_CONFIG_FILE='test' --name idoven-challenge --rm idoven-challenge python -m pytest /idoven/app/tests

build:
	docker build -t idoven-challenge .
