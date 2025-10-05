echo "Start deploying to server"

source .env

cd ~/Desktop/projects/triple-s
cp ~/Desktop/very_private_repo/.env .env
# docker pull ghcr.io/saians07/triple_s:latest

# Determine current and next environment
if docker ps --format "table {{.Names}}" | grep -q "triple_s_green"; then
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

echo "$NEXT"

apt install jq

TOKEN=$(curl -X POST http://nginx.triple-s.web.id/api/users/login -H "Content-Type: application/json" -d "{\"username\":\"$NGINX_IGNITION_USER\",\"password\":\"$NGINX_IGNITION_PWD\"}" | jq -r '.token')

RAW_DATA="{\"enabled\":true,\"defaultServer\":false,\
    \"useGlobalBindings\":false,\"domainNames\":[\"api.triple-s.web.id\"],\
    \"routes\":[{\"priority\":0,\"enabled\":true,\"type\":\"PROXY\",\"sourcePath\":\"/\",\"settings\":{\"includeForwardHeaders\":true,\"proxySslServerName\":true,\"keepOriginalDomainName\":true,\"directoryListingEnabled\":false,\"custom\":null},\"targetUri\":\"http://192.168.1.10:$NEXT_PORT\",\"redirectCode\":null,\"response\":null,\"integration\":null,\"accessListId\":null,\"sourceCode\":null}],\
    \"bindings\":[{\"type\":\"HTTP\",\"ip\":\"0.0.0.0\",\"port\":80,\"certificateId\":null}],\
    \"featureSet\":{\"websocketsSupport\":true,\"http2Support\":true,\"redirectHttpToHttps\":false},\
    \"accessListId\":null}"

curl -X PUT http://nginx.triple-s.web.id/api/hosts/ed2557da-24bf-4fa1-8f8a-4a0761a1d8b5 \
    -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
    --data-raw "$RAW_DATA"