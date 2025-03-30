package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
)

// uploadHandler handles the file upload logic, sending tasks to the uploadQueue.
func uploadHandler(w http.ResponseWriter, r *http.Request) {
	claims, err := validateRequest(r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}

	err = r.ParseMultipartForm(32 << 20) // 32 MB
	if err != nil {
		http.Error(w, "Error parsing form", http.StatusBadRequest)
		return
	}

	file, handler, err := r.FormFile("file")
	if err != nil {
		http.Error(w, "Error retrieving the file", http.StatusBadRequest)
		return
	}
	// Do not close `file` here; it will be closed in the worker after copying.

	isPublic, _ := strconv.ParseBool(r.FormValue("is_public"))

	responseChan := make(chan UploadResult)
	progressChan := make(chan int)

	// Enqueue the upload task
	uploadQueue <- UploadTask{
		File:     file,
		Handler:  handler,
		Claims:   claims,
		Response: responseChan,
		Progress: progressChan,
		IsPublic: isPublic,
	}

	// Optionally listen for progress updates (async logging)
	go func() {
		for p := range progressChan {
			log.Printf("Upload progress: %d%%", p)
		}
	}()

	// Wait for the upload result
	result := <-responseChan
	if result.Error != nil {
		http.Error(w, result.Error.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"id":        result.FileID,
		"filename":  handler.Filename,
		"status":    "uploaded",
		"is_public": isPublic,
	})
}

// downloadHandler handles file download requests, checking if the user can access the file.
func downloadHandler(w http.ResponseWriter, r *http.Request) {
	claims, err := validateRequest(r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}

	fileID := r.URL.Query().Get("id")
	if fileID == "" {
		http.Error(w, "File ID required", http.StatusBadRequest)
		return
	}

	var file File
	err = db.QueryRow(`
		SELECT f.id, f.user_id, f.name, f.path, f.size, f.content_type, f.is_public
		FROM files f
		LEFT JOIN file_shares fs ON f.id = fs.file_id AND fs.user_id = $2
		WHERE f.id = $1 
		  AND (f.user_id = $2 OR fs.user_id = $2 OR f.is_public = true)
	`, fileID, claims.UserID).Scan(
		&file.ID, &file.UserID, &file.Name, &file.Path, &file.Size, &file.ContentType, &file.IsPublic,
	)
	if err != nil {
		http.Error(w, "File not found or access denied", http.StatusNotFound)
		return
	}

	// Set appropriate headers and serve the file
	w.Header().Set("Content-Disposition", fmt.Sprintf("attachment; filename=%s", file.Name))
	w.Header().Set("Content-Type", file.ContentType)
	w.Header().Set("Content-Length", strconv.FormatInt(file.Size, 10))

	http.ServeFile(w, r, file.Path)
}

// listFilesHandler lists all files the user can see (owned, shared, or public).
func listFilesHandler(w http.ResponseWriter, r *http.Request) {
	claims, err := validateRequest(r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}

	rows, err := db.Query(`
		SELECT f.id, f.name, f.size, f.content_type, f.uploaded_at, f.is_public
		FROM files f
		LEFT JOIN file_shares fs ON f.id = fs.file_id AND fs.user_id = $1
		WHERE f.user_id = $1 OR fs.user_id = $1 OR f.is_public = true
	`, claims.UserID)
	if err != nil {
		http.Error(w, "Database error", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var files []File
	for rows.Next() {
		var f File
		if err := rows.Scan(&f.ID, &f.Name, &f.Size, &f.ContentType, &f.UploadedAt, &f.IsPublic); err != nil {
			continue
		}
		files = append(files, f)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(files)
}

// searchHandler allows searching files by name, type, or date, restricted to user access.
func searchHandler(w http.ResponseWriter, r *http.Request) {
	claims, err := validateRequest(r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}

	query := r.URL.Query()
	name := query.Get("name")
	fileType := query.Get("type")
	date := query.Get("date")

	sqlQuery := `
		SELECT f.id, f.name, f.size, f.content_type, f.uploaded_at, f.is_public
		FROM files f
		LEFT JOIN file_shares fs ON f.id = fs.file_id AND fs.user_id = $1
		WHERE (f.user_id = $1 OR fs.user_id = $1 OR f.is_public = true)`
	args := []interface{}{claims.UserID}
	paramCount := 2

	if name != "" {
		sqlQuery += fmt.Sprintf(" AND f.name ILIKE $%d", paramCount)
		args = append(args, "%"+name+"%")
		paramCount++
	}
	if fileType != "" {
		sqlQuery += fmt.Sprintf(" AND f.content_type LIKE $%d", paramCount)
		args = append(args, "%"+fileType+"%")
		paramCount++
	}
	if date != "" {
		sqlQuery += fmt.Sprintf(" AND DATE(f.uploaded_at) = $%d", paramCount)
		args = append(args, date)
		paramCount++
	}

	rows, err := db.Query(sqlQuery, args...)
	if err != nil {
		http.Error(w, "Database error", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var files []File
	for rows.Next() {
		var f File
		if err := rows.Scan(&f.ID, &f.Name, &f.Size, &f.ContentType, &f.UploadedAt, &f.IsPublic); err != nil {
			continue
		}
		files = append(files, f)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(files)
}

// shareHandler allows the owner of a file to share it with another user.
func shareHandler(w http.ResponseWriter, r *http.Request) {
	claims, err := validateRequest(r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}

	var share FileShare
	if err := json.NewDecoder(r.Body).Decode(&share); err != nil {
		http.Error(w, "Invalid request", http.StatusBadRequest)
		return
	}

	// Verify file belongs to user
	var ownerID int
	err = db.QueryRow(`SELECT user_id FROM files WHERE id = $1`, share.FileID).Scan(&ownerID)
	if err != nil || ownerID != claims.UserID {
		http.Error(w, "File not found or access denied", http.StatusForbidden)
		return
	}

	// Verify that the user to share with exists
	var userExists bool
	err = db.QueryRow(`SELECT EXISTS(SELECT 1 FROM users WHERE id = $1)`, share.SharedWith).Scan(&userExists)
	if err != nil || !userExists {
		http.Error(w, "User to share with not found", http.StatusBadRequest)
		return
	}

	_, err = db.Exec(
		`INSERT INTO file_shares (file_id, user_id) 
		 VALUES ($1, $2) ON CONFLICT DO NOTHING`,
		share.FileID, share.SharedWith,
	)
	if err != nil {
		http.Error(w, "Failed to share file", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
}

// deleteFileHandler deletes a file owned by the user, and queues up background cleanup.
func deleteFileHandler(w http.ResponseWriter, r *http.Request) {
	claims, err := validateRequest(r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}

	fileID := r.URL.Query().Get("id")
	if fileID == "" {
		http.Error(w, "File ID required", http.StatusBadRequest)
		return
	}

	// Verify file belongs to user, then remove it from DB
	var filePath string
	err = db.QueryRow(`
		DELETE FROM files 
		WHERE id = $1 AND user_id = $2
		RETURNING path
	`, fileID, claims.UserID).Scan(&filePath)
	if err != nil {
		if err == sql.ErrNoRows {
			http.Error(w, "File not found or access denied", http.StatusNotFound)
		} else {
			http.Error(w, "Database error", http.StatusInternalServerError)
		}
		return
	}

	// Queue file deletion as a background job
	jobQueue <- BackgroundJob{
		Type: "cleanup",
		Data: filePath,
	}

	// Also delete file_shares in the background
	go func() {
		_, delErr := db.Exec(`DELETE FROM file_shares WHERE file_id = $1`, fileID)
		if delErr != nil {
			log.Printf("Error deleting shares for file %s: %v", fileID, delErr)
		}
	}()

	w.WriteHeader(http.StatusNoContent)
}
