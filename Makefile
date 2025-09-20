include .env

.PHONY: run build test clean deps create-db docker-build docker-run

# for development
run:
	go run cmd/api/main.go

build:
	chmod +x scripts/build.sh
	./scripts/build.sh

test:
	go test -v ./...

clean:
	rm -rf bin/

# Dependencies
deps:
	go mod download
	go mod tidy

# Database initialization
create-db:
	docker exec -it postgresql psql -h $(PI5_POSTGRES_DB_HOST) -U $(PI5_POSTGRES_DB_USER) -d $(PI5_POSTGRES_DB_NAME) -f scripts/create_table.sql

# Docker
docker-build:
	docker build -t backend-service deployments/docker/Dockerfile .

docker-run:
	docker run -p 8010:8080 backend-service

# Environment
dev:
	PI5_GO_BACKEND_ENV=development go run cmd/api/main.go

prod:
	PI5_GO_BACKEND_ENV=production go run cmd/api/main.go
