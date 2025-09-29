#!/bin/sh
echo "Starting deployment to server ..."
echo "Utilize blue green deployment ..."

# ensure we are on the correct directory
cd ~/backend_pi_5
cp ~/very_private_repo/.env .env
docker pull ghcr.io/saians07/backend_pi_5:latest

# Determine current and next environment
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

# install jq
apt install jq

TOKEN=$(curl -X POST http://nginx.triple-s.web.id/api/users/login -H "Content-Type: application/json" -d '{"username":"saians07","password":"GT-b5330"}' | jq -r '.token')
RAW_DATA="{\"enabled\":true,\"defaultServer\":false,\
    \"useGlobalBindings\":false,\"domainNames\":[\"api.triple-s.web.id\"],\
    \"routes\":[{\"priority\":0,\"enabled\":true,\"type\":\"PROXY\",\"sourcePath\":\"/\",\"settings\":{\"includeForwardHeaders\":true,\"proxySslServerName\":true,\"keepOriginalDomainName\":true,\"directoryListingEnabled\":false,\"custom\":null},\"targetUri\":\"http://192.168.1.10:$NEXT_PORT\",\"redirectCode\":null,\"response\":null,\"integration\":null,\"accessListId\":null,\"sourceCode\":null}],\
    \"bindings\":[{\"type\":\"HTTP\",\"ip\":\"0.0.0.0\",\"port\":80,\"certificateId\":null}],\
    \"featureSet\":{\"websocketsSupport\":true,\"http2Support\":true,\"redirectHttpToHttps\":false},\
    \"accessListId\":null}"


curl -X PUT http://nginx.triple-s.web.id/api/hosts/ed2557da-24bf-4fa1-8f8a-4a0761a1d8b5 \
    -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
    --data-raw "$RAW_DATA"


echo "Deploying to: $NEXT environment (port: $NEXT)"
docker compose --file docker_compose_$NEXT.yml down
docker compose --file docker_compose_$NEXT.yml up -d

# wait for container to start
sleep 10

# Health Check
if curl -f -s --max-time 30 http://localhost:$NEXT_PORT/health; then
    echo "✅ Health check Passed"

    # if health check passed, we will stop old docker
    if docker ps --format "table {{.Names}}" | grep -q "backend_pi_5_$CURRENT"; then
        echo "Removing $CURRENT environment"
        docker compose --file docker_compose_$CURRENT.yml down
    fi

    echo "✅ Deployment successful to $NEXT environment"
else
    echo "❌ Health check failed on $NEXT environment"
    docker compose --file docker_compose_$NEXT.yml down
    exit 1
fi
