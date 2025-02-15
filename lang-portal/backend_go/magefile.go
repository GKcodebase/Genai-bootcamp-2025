//go:build mage
package main

import (
	"database/sql"
	"fmt"
	"os"

	_ "modernc.org/sqlite"
	"github.com/magefile/mage/sh"
)

// Migrate applies database migrations
func Migrate() error {
	db, err := sql.Open("sqlite", "words.db")
	if err != nil {
		return err
	}
	defer db.Close()

	migrationFiles, err := os.ReadDir("db/migrations")
	if err != nil {
		return err
	}

	for _, file := range migrationFiles {
		if !file.IsDir() {
			content, err := os.ReadFile(fmt.Sprintf("db/migrations/%s", file.Name()))
			if err != nil {
				return err
			}

			_, err = db.Exec(string(content))
			if err != nil {
				return fmt.Errorf("error executing migration %s: %v", file.Name(), err)
			}
			fmt.Printf("Applied migration: %s\n", file.Name())
		}
	}
	return nil
}

// Run starts the server
func Run() error {
	return sh.Run("go", "run", "cmd/server/main.go")
}

// Build builds the server binary
func Build() error {
	return sh.Run("go", "build", "-o", "server", "cmd/server/main.go")
}
