package handler

import (
	"backend_pi_5/internal/service"
	"backend_pi_5/pkg/logger"
	"backend_pi_5/pkg/utils"
	"net/http"
	"strconv"
	"strings"

	"github.com/gorilla/mux"
)

type UserHandler struct {
	userService service.UserService
	logger      logger.Logger
}

func InitUserHandler(userService service.UserService, logger logger.Logger) *UserHandler {
	return &UserHandler{
		userService: userService,
		logger:      logger,
	}
}

func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	idStr := vars["id"]

	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.logger.Error("Invalid user ID format", err)
		utils.WriteErrorResponse(w, http.StatusBadRequest, "Invalid user ID format")
		return
	}

	user, err := h.userService.GetUserbyID(id)
	if err != nil {
		if strings.Contains(err.Error(), "not found") {
			utils.WriteErrorResponse(w, http.StatusNotFound, "User not found")
			return
		}

		h.logger.Error("Failed to get user", err)
		utils.WriteErrorResponse(w, http.StatusInternalServerError, "Internal server error")
		return
	}

	utils.WriteSuccessResponse(w, user)
}
