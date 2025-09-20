package config

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v2"
)

type Config struct {
	Database DatabaseConfig `yaml:"database"`
	Server   ServerConfig   `yaml:"server"`
	App      AppConfig      `yaml:"app"`
}

type DatabaseConfig struct {
	Host         string
	Port         string
	User         string
	Password     string
	DBName       string
	MaxOpenConns int `yaml:"max_open_conns"`
	MaxIdleConns int `yaml:"max_idle_conns"`
}

type ServerConfig struct {
	Port         string `yaml:"port"`
	ReadTimeout  int    `yaml:"read_timeout"`
	WriteTimeout int    `yaml:"write_timeout"`
}

type AppConfig struct {
	Name    string `yaml:"name"`
	Version string `yaml:"version"`
	Env     string `yaml:"env"`
}

func getConfigPath() string {
	env := os.Getenv("PI5_GO_BACKEND_ENV")
	if env == "production" {
		return "configs/config.yaml"
	}
	return "configs/config.dev.yaml"
}

func Load() (*Config, error) {
	configPath := getConfigPath()

	data, err := os.ReadFile(configPath)
	if err != nil {
		return nil, fmt.Errorf("failed to read config file: %w", err)
	}

	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("failed to parse config file: %w", err)
	}
	// Override with environment variables if they exist
	overrideWithEnv(&cfg)

	return &cfg, nil
}

func overrideWithEnv(cfg *Config) {
	if val := os.Getenv("PI5_POSTGRES_DB_HOST"); val != "" {
		cfg.Database.Host = val
	}

	if val := os.Getenv("PI5_POSTGRES_DB_PORT"); val != "" {
		cfg.Database.Port = val
	}

	if val := os.Getenv("PI5_POSTGRES_DB_USER"); val != "" {
		cfg.Database.User = val
	}

	if val := os.Getenv("PI5_POSTGRES_DB_PWD"); val != "" {
		cfg.Database.Password = val
	}

	if val := os.Getenv("PI5_POSTGRES_DB_NAME"); val != "" {
		cfg.Database.Password = val
	}
}
