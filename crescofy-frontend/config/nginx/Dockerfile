# build stage
FROM node:14.15.1-alpine as build-stage

RUN apk add g++ make python2

WORKDIR /app

COPY package*.json ./

# RUN npm install --save @popperjs/core

RUN npm install

#RUN npm i --unsafe-perm node-sass

#RUN npm install  --unsafe-perm -g sass-loader

#RUN npm install --unsafe-perm -g node-sass

#RUN npm install sass-loader sass webpack --save-dev

COPY . .

RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage

RUN rm /etc/nginx/conf.d/default.conf

COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
