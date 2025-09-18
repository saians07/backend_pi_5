# BACKEND FOR PI 5

In order to protect my pi 5 from unwanted access. I decided to write a GO based backend.

# STRUCTURE OF THE PROJECT

```
backend_pi_5/
├── cmd/
│   └── api/
│       └── main.go
├── internal/
│   ├── handler/
│   ├── service/
│   ├── repository/
│   ├── model/
│   └── config/
├── pkg/
│   ├── logger/
│   ├── database/
│   └── utils/
├── configs/
│   ├── config.yaml
│   └── config.dev.yaml
├── scripts/
│   ├── build.sh
│   └── deploy.sh
├── deployments/
│   ├── docker/
│   │   └── Dockerfile
│   └── kubernetes/
├── test/
├── go.mod
├── go.sum
├── Makefile
├── README.md
├── .gitignore
└── .env.example
```

# THE USAGE

## ACCESS INTERNAL DATABASE