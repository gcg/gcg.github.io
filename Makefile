.PHONY: all build serve clean

all: build serve

build:
	python3 scripts/build_posts.py

serve: build
	@echo "Starting local Solo Leveling Webtoon preview server at http://localhost:8000..."
	python3 -m http.server 8000

clean:
	rm -rf .DS_Store
