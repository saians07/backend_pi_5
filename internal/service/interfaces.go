package service

import "backend_pi_5/internal/model"

type UserService interface {
	GetUserbyID(id int) (*model.User, error)
}
