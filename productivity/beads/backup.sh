#!/bin/sh
# Online, full Dolt backup: includes history, branches and the working set.
set -eu
cd "$(dirname "$0")"
for database in eden inet_server; do
docker compose exec -T dolt sh -c '
  database="$1"
  exec dolt --no-tls --host 127.0.0.1 --port 3306 \
    --user root --password "$DOLT_ROOT_PASSWORD" --use-db "$database" \
    sql -q "CALL DOLT_BACKUP('\''sync-url'\'', '\''file:///backups/$database'\'');"
' sh "$database"
done
