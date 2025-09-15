cd ./docker &&
docker compose -f docker-compose-deploy.yml build cotw_trophy_viewer &&
docker compose up  -f docker-compose-deploy.yml --detach --force-recreate --remove-orphans cotw_trophy_viewer