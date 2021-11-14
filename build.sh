#! /usr/bin/env bash
docker build -t geekzone/tailwindcss -f docker/tailwindcss/Dockerfile .

# docker push geekzone/tailwindcss

# sudo docker run -v theme:$TAILWIND -ti geekzone/tailwindcss \
docker run -ti geekzone/tailwindcss
yarn tailwind build /usr/src/app/theme/static_src/src/styles.css -c /usr/src/app/theme/static_src/tailwind.config.js -o /usr/src/app/theme/static/css/dist/styles.css

