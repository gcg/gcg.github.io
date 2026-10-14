.PHONY: all serve clean

all: serve

serve:
	@echo "Starting local Solo Leveling Webtoon preview server at http://localhost:8000..."
	python3 -m http.server 8000

clean:
	rm -rf .DS_Store
