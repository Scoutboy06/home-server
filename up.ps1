docker compose `
 -f compose.yml `
 -f infra/docker-compose.yml `
 -f media/docker-compose.yml `
 -f cloud/docker-compose.yml `
 -f automation/docker-compose.yml `
 -f games/docker-compose.yml `
 -f productivity/docker-compose.yml `
 up -d
