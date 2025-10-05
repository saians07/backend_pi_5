<h1 align="center">
    Triple S
</h1>

Official python backend for my raspberry pi-5.

Previously I have created a Go language based backend. But the development is very slow since I am not yet really fluent with GO language. Hence, here i tried to switch the language to Python for easier and faster prototyping.

## Structure of The Project

```
triple-s/
├── .github/
│   ├── master/
|   |   └── master-ci-cd.yml
│   ├── release_candidate/
|   |   └── rc-ci-cd.yml
├── core/ # what your app will do?
│   ├── database/
│   ├── logger/
│   └── main.py
├── api/ # how can you send a command to your app to use their core function?
│   ├── database/ 
│   |   ├── read 
│   |   └── write
│   └── config/
├── service/
│   └── database/ # list of model of the database
│       ├── users
|       └── transactions
├── deployment/
│   └── deploy.sh
├── scripts/
│   └── docker/
│       └── Dockerfile
├── __init__.py
├── docker_compose_blue.yml
├── docker_compose_green.yml
├── main.py
└── requirements.txt
```

The entry point will be `main.py`. It will read the function from `api` folder. The `api` folder is a bridge to the `core` functions. `core` functions might need the help from specific service, like database helps core function to map the model of the database.

## Features

### Backend Service API

The main function of this service is to provide backend technology service.

The main function of this backend is to provide "bridge" to acess to the database. There is only 1 way to access the database, through this backend.

### AI capability 