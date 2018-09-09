FROM abiosoft/caddy:no-stats

# Agree with Let's Encrypt Subscriber Agreement.
ENV ACME_AGREE true

COPY Caddyfile /etc/Caddyfile

# caddy image already exposes 80 and 443
# It also already has an entry point, so nothing to do here!