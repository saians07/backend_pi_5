package logger

import (
	"log"
	"os"
)

type Logger interface {
	Info(msg string)
	Error(msg string, err error)
	Fatal(msg string, err error)
}

type logger struct {
	infoLogger  *log.Logger
	errorLogger *log.Logger
}

func InitLog() Logger {
	return &logger{
		infoLogger:  log.New(os.Stdout, "INFO: ", log.Ldate|log.Ltime|log.Lshortfile),
		errorLogger: log.New(os.Stderr, "ERROR: ", log.Ldate|log.Ltime|log.Lshortfile),
	}
}

func (l *logger) Info(msg string) {
	l.infoLogger.Println(msg)
}

func (l *logger) Error(msg string, err error) {
	if err != nil {
		l.errorLogger.Printf("%s: %v", msg, err)
	} else {
		l.errorLogger.Println(msg)
	}
}

func (l *logger) Fatal(msg string, err error) {
	if err != nil {
		l.errorLogger.Fatalf("%s: %v", msg, err)
	} else {
		l.errorLogger.Fatal(msg)
	}
}
