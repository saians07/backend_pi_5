package main

import (
	"backend_pi_5/internal/config"
	"backend_pi_5/internal/handler"
	"backend_pi_5/internal/repository"
	"backend_pi_5/internal/service"
	"backend_pi_5/pkg/database"
	"backend_pi_5/pkg/logger"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	// initialize logger
	log := logger.InitLog()

	cfg, err := config.Load()
	if err != nil {
		log.Fatal("Failed to load configuration:", err)
	}

	//initialize database
	db, err := database.ConnectDB(cfg.Database)
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}
	defer db.Close()

	// initialize user repository
	userRepo := repository.InitUserRepository(db)

	// initialize service
	userService := service.InitUserService(userRepo, log)

	// initialize handler
	userHandler := handler.InitUserHandler(userService, log)

	// setup routes
	router := setupRoutes(userHandler)

	// start server
	log.Info("Server starting on port " + cfg.Server.Port)
	if err := http.ListenAndServe(":"+cfg.Server.Port, router); err != nil {
		log.Fatal("Server failed to start: %v", err)
	}
}

func setupRoutes(userHandler *handler.UserHandler) *mux.Router {
	router := mux.NewRouter()

	return router
}
