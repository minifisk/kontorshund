FROM jwilder/nginx-proxy:0.9
COPY vhost.d/default /etc/nginx/vhost.d/default
COPY custom.conf /etc/nginx/conf.d/custom.conf


# # Inspiration: https://www.rockyourcode.com/run-docker-nginx-as-non-root-user/

# FROM nginx:1.21

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends python3

# RUN rm /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/conf.d

# WORKDIR /app

# ## add permissions for nginx user
# RUN chown -R nginx:nginx /app && chmod -R 755 /app && \
#         chown -R nginx:nginx /var/cache/nginx && \
#         chown -R nginx:nginx /var/log/nginx && \
#         chown -R nginx:nginx /etc/nginx/conf.d
# RUN touch /var/run/nginx.pid && \
#         chown -R nginx:nginx /var/run/nginx.pid

# USER nginx