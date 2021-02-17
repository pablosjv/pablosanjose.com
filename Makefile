.DEFAULT_GOAL := run
.SILENT: # silence!!

export PATH := ./bin:$(PATH)

clean:
	rm -rf ./public || true
	rm -rf content/posts/* static/public/images/* || true

.venv:
	python3 -m virtualenv .venv

setup: .venv
	.venv/bin/pip install -r requirements.txt

run:
	hugo server --watch --buildFuture --cleanDestinationDir

ci: refresh
	hugo

avatar:
	wget -O static/avatar.jpg https://github.com/pablosjv.png
	convert static/avatar.jpg \
		-bordercolor white -border 0 \
		\( -clone 0 -resize 16x16 \) \
		\( -clone 0 -resize 32x32 \) \
		\( -clone 0 -resize 48x48 \) \
		\( -clone 0 -resize 64x64 \) \
		-delete 0 -alpha off -colors 256 static/favicon.ico
	convert -resize x120 static/avatar.jpg static/apple-touch-icon.png

og:
	wget -O static/og-image.png "https://og.caarlos0.dev/Pablo%20San%20Jose%20%7C%20**pablosjv**.png?theme=light&md=1&fontSize=100px&images=https://github.com/pablosjv.png"

# go run cmd/notion/main.go
refresh: clean
	.venv/bin/python refresh.py
