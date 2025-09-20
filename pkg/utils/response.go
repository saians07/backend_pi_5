package utils

import (
	"backend_pi_5/internal/model"
	"encoding/json"
	"net/http"
)

func WriteJSONResponse(w http.ResponseWriter, statusCode int, response model.APIResponse) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	json.NewEncoder(w).Encode(response)
}

func WriteErrorResponse(w http.ResponseWriter, statusCode int, message string) {
	response := model.APIResponse{
		Success: false,
		Error:   message,
	}
	WriteJSONResponse(w, statusCode, response)
}

func WriteSuccessResponse(w http.ResponseWriter, data any) {
	response := model.APIResponse{
		Success: true,
		Data:    data,
	}
	WriteJSONResponse(w, http.StatusOK, response)
}
