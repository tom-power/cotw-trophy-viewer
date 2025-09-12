cd ./docker &&
docker compose build cotw_trophy_viewer &&
docker compose up --detach --force-recreate --remove-orphans cotw_trophy_viewer