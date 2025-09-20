package repository

import (
	"backend_pi_5/internal/model"
	"database/sql"
	"fmt"
)

type userRepository struct {
	db *sql.DB
}

func InitUserRepository(db *sql.DB) UserRepository {
	return &userRepository{db: db}
}

func (r *userRepository) GetUserByID(id int) (*model.User, error) {
	query := `
		SELECT id, name
		FROM users
		WHERE id = $1
	`
	var user model.User
	err := r.db.QueryRow(query, id).Scan(
		&user.ID,
		&user.Name,
	)

	if err != nil {
		if err == sql.ErrNoRows {
			return nil, fmt.Errorf("user with id %d not found", id)
		}
		return nil, fmt.Errorf("failed to get user: %w", err)
	}
	return &user, nil
}
