package main

import (
	"time"

	"github.com/dgrijalva/jwt-go"
)

// User represents a registered user.
type User struct {
	ID        int       `json:"id"`
	Username  string    `json:"username"`
	Email     string    `json:"email"`
	Password  string    `json:"password,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

// File represents an uploaded file.
type File struct {
	ID          int       `json:"id"`
	UserID      int       `json:"user_id"`
	Name        string    `json:"name"`
	Path        string    `json:"path"`
	Size        int64     `json:"size"`
	ContentType string    `json:"content_type"`
	UploadedAt  time.Time `json:"uploaded_at"`
	IsPublic    bool      `json:"is_public"`
}

// FileShare represents a record showing a file shared with another user.
type FileShare struct {
	FileID     int `json:"file_id"`
	SharedWith int `json:"shared_with"`
}

// Credentials represents user login credentials.
type Credentials struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

// Claims embeds JWT standard claims with custom user info.
type Claims struct {
	Username string `json:"username"`
	UserID   int    `json:"user_id"`
	jwt.StandardClaims
}
