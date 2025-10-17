#!/bin/bash
echo "Start deploying process ..."

cd ~/very_private_repo
git pull

cd ~/backend_pi_5
cp ~/very_private_repo/.env .env
source .env
docker pull ghcr.io/saians07/backend_pi_5:latest

echo "Start configuring environment ..."
if docker ps --format "table {{.Names}}" | grep -q "backend_pi_5_blue"; then
    CURRENT="blue"
    NEXT="green"
    CURRENT_PORT=8082
    NEXT_PORT=8083
else
    CURRENT="green"
    NEXT="blue"
    CURRENT_PORT=8083
    NEXT_PORT=8082
fi

echo "Deploying to: $NEXT environment (port: $NEXT)"
docker compose --file docker_compose_$NEXT.yml down
docker compose --file docker_compose_$NEXT.yml up --pull always -d --build --remove-orphans

sleep 10

echo "🩺 Start health checking ..."
if curl -f -s --max-time 30 http://localhost:$NEXT_PORT/health; then
    echo "✅ Health check Passed"

    if docker ps --format "table {{.Names}}" | grep -q "backend_pi_5_$CURRENT"; then
        echo "Removing $CURRENT environment"
        docker compose --file docker_compose_$CURRENT.yml down
    fi

    # cleaning up docker iamges
    docker image prune -f
    docker container prune -f

    # run database migrations
    docker exec -it backend_pi_5_$NEXT alembic upgrade head

    # install jq to parse json
    sudo apt install jq

    # get the token from nginx json response
    TOKEN=$(curl -X POST "http://nginx.$BACKEND_URL/api/users/login" -H "Content-Type: application/json" -d "{\"username\":\"$NGINX_IGNITION_USER\",\"password\":\"$NGINX_IGNITION_PWD\"}" | jq -r '.token')

    RAW_DATA="{\"enabled\":true,\"defaultServer\":false,\
        \"useGlobalBindings\":false,\"domainNames\":[\"api.$BACKEND_URL\"],\
        \"routes\":[{\"priority\":0,\"enabled\":true,\"type\":\"PROXY\",\"sourcePath\":\"/\",\"settings\":{\"includeForwardHeaders\":true,\"proxySslServerName\":true,\"keepOriginalDomainName\":true,\"directoryListingEnabled\":false,\"custom\":null},\"targetUri\":\"http://192.168.1.10:$NEXT_PORT\",\"redirectCode\":null,\"response\":null,\"integration\":null,\"accessListId\":null,\"sourceCode\":null}],\
        \"bindings\":[{\"type\":\"HTTP\",\"ip\":\"0.0.0.0\",\"port\":80,\"certificateId\":null}],\
        \"featureSet\":{\"websocketsSupport\":true,\"http2Support\":true,\"redirectHttpToHttps\":false},\
        \"accessListId\":null}"

    curl -X PUT "http://nginx.$BACKEND_URL/api/hosts/ed2557da-24bf-4fa1-8f8a-4a0761a1d8b5" \
        -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
        --data-raw "$RAW_DATA"
    
    curl "https://nginx.$BACKEND_URL/api/nginx/reload" \
        -X 'POST' \
        -H 'accept: application/json' \
        -H "authorization: Bearer $TOKEN" \
        -H 'content-type: application/json' \
        -H "origin: http://nginx.$BACKEND_URL" \
        -H 'priority: u=1, i' \
        -H "referer: http://nginx.$BACKEND_URL/api/hosts/ed2557da-24bf-4fa1-8f8a-4a0761a1d8b5" \

    echo "✅ Deployment successful to $NEXT environment"
else
    echo "❌ Health check failed on $NEXT environment"
    docker compose --file docker_compose_$NEXT.yml down
    exit 1
fi
