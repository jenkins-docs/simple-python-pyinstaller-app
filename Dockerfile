FROM nginx:1.10.1-alpine

COPY reverse-proxy.conf /etc/nginx/conf.d/default.conf
EXPOSE 9000

CMD ["nginx", "-g", "daemon off;"]