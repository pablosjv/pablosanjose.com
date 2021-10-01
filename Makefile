.DEFAULT_GOAL := run
.SILENT: # silence!!

export PATH := ./bin:$(PATH)

help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

clean: ## clean artifacts
	rm -rf ./public || true
	rm -rf content/posts/* static/public/images/* || true

.venv:  ## create virtualenv
	python3 -m venv .venv

setup: .venv  ## setup project
	.venv/bin/pip install -r requirements.txt

run:  ## run the hugo server
	docker run --rm -it -v $(shell pwd):/src -p 1313:1313 klakegg/hugo:0.80.0 server --verbose --watch --buildFuture --cleanDestinationDir

ci: refresh  ## run CI steps
	docker run --rm -it -v $(shell pwd):/src klakegg/hugo:0.80.0

avatar:  ## get the avatar from github
	wget -O static/avatar.jpg https://github.com/pablosjv.png
	convert static/avatar.jpg \
		-bordercolor white -border 0 \
		\( -clone 0 -resize 16x16 \) \
		\( -clone 0 -resize 32x32 \) \
		\( -clone 0 -resize 48x48 \) \
		\( -clone 0 -resize 64x64 \) \
		-delete 0 -alpha off -colors 256 static/favicon.ico
	convert -resize x120 static/avatar.jpg static/apple-touch-icon.png

og:  ## get OG
	wget -O static/og-image.png "https://og.caarlos0.dev/Pablo%20San%20Jose%20%7C%20**pablosjv**.png?theme=light&md=1&fontSize=100px&images=https://github.com/pablosjv.png"

refresh: clean  ## refresh pages
	.venv/bin/python refresh.py
