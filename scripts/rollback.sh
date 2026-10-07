#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="docker-compose.blue-green.yml"
NGINX_CONF="nginx/default.conf"

compose_exec() {
    if docker compose version >/dev/null 2>&1; then
        docker compose "$@"
    elif command -v docker-compose >/dev/null 2>&1; then
        docker-compose "$@"
    elif [ -x "$HOME/.docker/cli-plugins/docker-compose" ]; then
        "$HOME/.docker/cli-plugins/docker-compose" "$@"
    elif [ -x "/usr/local/bin/docker-compose" ]; then
        "/usr/local/bin/docker-compose" "$@"
    else
        echo "Error: Neither 'docker compose' nor 'docker-compose' is available." >&2
        exit 1
    fi
}

if grep -q "app-green:8000" "$NGINX_CONF" 2>/dev/null; then
    ROLLBACK_TO="blue"
else
    ROLLBACK_TO="green"
fi

echo "Rolling back traffic to: $ROLLBACK_TO"

compose_exec -f "$COMPOSE_FILE" start "app-$ROLLBACK_TO" || \
compose_exec -f "$COMPOSE_FILE" up -d "app-$ROLLBACK_TO"

cat <<EOF > "$NGINX_CONF"
upstream app_backend {
    server app-$ROLLBACK_TO:8000;
}

server {
    listen 80;
    server_name huynn69.fuji.io.vn huyn69.fuji.io.vn fuji.io.vn www.fuji.io.vn localhost;

    location / {
        proxy_pass http://app_backend;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

docker exec bg_nginx_proxy nginx -s reload || true
echo "Rollback completed. Live traffic routed to [$ROLLBACK_TO]"
