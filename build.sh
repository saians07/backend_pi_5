#!/bin/sh
echo "Starting deployment to server ..."
echo "Utilize blue green deployment ..."

# ensure we are on the correct directory
cd ~/bakcend_pi_5
cp ~/very_private_repo/.env .env

# Determine current and next environment
if docker ps --format "table {{.Names}}" | grep -q "backend_pi_5_blue"; then
    CURRENT="blue"
    NEXT="green"
    CURRENT_PORT=8082
    NEXT_PORT=8083
    echo "Deploying to: $NEXT environment (port: $NEXT)"
    docker compose --file docker_compose_$NEXT.yml down
    docker compose --file docker_compose_$NEXT.yml up
else
    CURRENT="green"
    NEXT="blue"
    CURRENT_PORT=8083
    NEXT_PORT=8082
    echo "Deploying to: $CURRENT environment (port: $CURRENT_PORT)"
    docker compose -f docker_compose_$NEXT.yml down
    docker compose -f docker_compose_$NEXT.yml up
fi

# wait for container to start
sleep 10

# Health Check
if curl -f httpl://localhost:$NEXT_PORT/health; then
    echo "✅ Health chek Passed"

    # if health check passed, we will stop old docker
    docker compose --file docker_compose_$CURRENT.yml down

    echo "✅ Deployment successful to $NEXT environment"
else
    echo "❌ Health check failed on $NEXT environment"
    docker docker compose --file docker_compose_$NEXT.yml down
    exit 1
fi




