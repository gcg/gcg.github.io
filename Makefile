.PHONY: all build serve test clean

all: build serve

build:
	python3 scripts/build_posts.py

serve: build
	@echo "Serving gcg.me locally at http://localhost:8000..."
	python3 -m http.server 8000

test: build
	python3 -m unittest discover -s tests -v

clean:
	rm -rf .DS_Store
