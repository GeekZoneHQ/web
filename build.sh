#! /usr/bin/env bash
docker build -t geekzone/tailwindcss -f docker/tailwindcss/Dockerfile .

docker push geekzone/tailwindcss

TAILWIND=/usr/src/app/theme

docker run -v theme:$TAILWIND -ti geekzone/tailwindcss \
yarn tailwind build $TAILWIND/static_src/src/styles.css -c $TAILWIND/static_src/tailwind.config.js -o $TAILWIND/static/css/dist/styles.css

