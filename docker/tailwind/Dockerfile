FROM alpine

RUN apk add --update nodejs-current npm yarn

WORKDIR /usr/src/app

COPY theme/ .

RUN npm install -D tailwindcss@latest postcss@latest autoprefixer@latest 

