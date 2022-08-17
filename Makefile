.PHONY: watch build optimize serve 


build: build-theme build-server

watch: 
	@$(MAKE) -j2 watch-theme watch-server

build-server:
	hugo --minify

install-theme:
	@cd themes/main; npm i 

build-theme:
	@cd themes/main; npm i; npm run build

watch-theme:
	@cd themes/main; npm run watch 

watch-server:
	hugo server -D --watch 


