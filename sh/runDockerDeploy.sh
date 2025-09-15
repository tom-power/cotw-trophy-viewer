cd ./docker &&
docker compose -f docker-compose-deploy.yml build cotw_trophy_viewer &&
docker compose -f docker-compose-deploy.yml up --detach --force-recreate --remove-orphans cotw_trophy_viewer