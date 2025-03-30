package main

import (
	"log"
	"net/http"
	"os"
)

// main is the application entry point.
func main() {
	// Make sure the JWT secret is set
	if os.Getenv("JWT_SECRET") == "" {
		log.Fatal("JWT_SECRET environment variable not set")
	}

	// Initialize DB and Redis
	initDB()
	defer db.Close()
	defer redisClient.Close()

	// Start background workers (upload and job workers)
	StartWorkers()

	// Define all routes
	http.HandleFunc("/register", registerHandler)
	http.HandleFunc("/login", loginHandler)
	http.HandleFunc("/protected", protectedHandler)
	http.HandleFunc("/upload", uploadHandler)
	http.HandleFunc("/download", downloadHandler)
	http.HandleFunc("/files", listFilesHandler)
	http.HandleFunc("/search", searchHandler)
	http.HandleFunc("/share", shareHandler)
	http.HandleFunc("/delete", deleteFileHandler)

	log.Println("Server running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
