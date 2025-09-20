package repository

import "backend_pi_5/internal/model"

type UserRepository interface {
	GetUserByID(id int) (*model.User, error)
}
