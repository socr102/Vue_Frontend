# build stage
FROM node:lts-alpine as build-stage
RUN apk add g++ make python2
WORKDIR /app
COPY package*.json ./

RUN npm install

RUN npm install sass-loader -D

RUN npm install node-sass -D

COPY . .


RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
RUN rm /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]