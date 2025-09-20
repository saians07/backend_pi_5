package service

import (
	"backend_pi_5/internal/model"
	"backend_pi_5/internal/repository"
	"backend_pi_5/pkg/logger"
	"fmt"
)

type userService struct {
	userRepo repository.UserRepository
	logger   logger.Logger
}

func InitUserService(userRepo repository.UserRepository, logger logger.Logger) UserService {
	return &userService{
		userRepo: userRepo,
		logger:   logger,
	}
}

func (s *userService) GetUserbyID(id int) (*model.User, error) {
	if id <= 0 {
		return nil, fmt.Errorf("invalid user ID: %d", id)
	}

	s.logger.Info(fmt.Sprintf("Fetching user with ID: %d", id))

	user, err := s.userRepo.GetUserByID(id)
	if err != nil {
		s.logger.Error("Failed to fetch user from repository", err)
		return nil, err
	}

	s.logger.Info(fmt.Sprintf("Successfully fetched user: %s", user.Name))
	return user, nil
}
