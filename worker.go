package main

import (
	"fmt"
	"io"
	"log"
	"mime/multipart"
	"os"
	"path/filepath"
	"sync"
	"time"
)

// Global concurrency variables
var (
	uploadQueue   = make(chan UploadTask, 10)    // Buffer for file upload tasks
	jobQueue      = make(chan BackgroundJob, 20) // Buffer for background jobs
	uploadPath    = "./uploads"                  // Directory for file storage
	uploadWorkers = 3                            // Number of concurrent upload workers
)

// UploadTask holds the file info and channels to handle results/progress.
type UploadTask struct {
	File     multipart.File
	Handler  *multipart.FileHeader
	Claims   *Claims
	Response chan UploadResult
	Progress chan int
	IsPublic bool
}

// UploadResult is used to communicate back the result (file ID or error).
type UploadResult struct {
	FileID int
	Error  error
}

// BackgroundJob can be used for any post-upload or cleanup tasks.
type BackgroundJob struct {
	Type string
	Data interface{}
}

// StartWorkers spins up the worker goroutines and creates the uploads directory if needed.
func StartWorkers() {
	// Ensure upload directory exists
	if err := os.MkdirAll(uploadPath, os.ModePerm); err != nil {
		log.Fatal("Failed to create upload directory:", err)
	}

	// Start upload workers
	for i := 0; i < uploadWorkers; i++ {
		go uploadWorker(i)
	}

	// Start background job worker
	go backgroundJobWorker()
}

// uploadWorker continuously listens on uploadQueue for new tasks.
func uploadWorker(id int) {
	for task := range uploadQueue {
		processUpload(task, id)
	}
}

// processUpload handles the actual file copying to disk and the DB insert.
func processUpload(task UploadTask, workerID int) {
	defer close(task.Progress)
	defer close(task.Response)
	defer task.File.Close()

	filePath := filepath.Join(
		uploadPath,
		fmt.Sprintf("%d_%d_%s", task.Claims.UserID, time.Now().UnixNano(), task.Handler.Filename),
	)

	// Create the destination file
	dst, err := os.Create(filePath)
	if err != nil {
		task.Response <- UploadResult{Error: err}
		return
	}
	defer dst.Close()

	var wg sync.WaitGroup
	wg.Add(2)

	var fileID int
	var dbErr error

	// 1) Copy file to disk, track progress
	go func() {
		defer wg.Done()
		reader := io.TeeReader(task.File, dst)
		buf := make([]byte, 32*1024)
		totalRead := 0
		fileSize := task.Handler.Size

		for {
			n, errRead := reader.Read(buf)
			if n > 0 {
				totalRead += n
				progress := int(float64(totalRead) / float64(fileSize) * 100)
				task.Progress <- progress
			}
			if errRead != nil {
				break
			}
		}
	}()

	// 2) Insert DB record
	go func() {
		defer wg.Done()
		contentType := task.Handler.Header.Get("Content-Type")
		if contentType == "" {
			contentType = "application/octet-stream"
		}

		dbErr = db.QueryRow(
			`INSERT INTO files (user_id, name, path, size, content_type, is_public) 
			 VALUES ($1, $2, $3, $4, $5, $6) RETURNING id`,
			task.Claims.UserID,
			task.Handler.Filename,
			filePath,
			task.Handler.Size,
			contentType,
			task.IsPublic,
		).Scan(&fileID)
	}()

	wg.Wait()

	// If DB insert failed, remove the partial file and return error
	if dbErr != nil {
		_ = os.Remove(filePath)
		task.Response <- UploadResult{Error: dbErr}
		return
	}

	// Enqueue a post-upload job
	jobQueue <- BackgroundJob{
		Type: "post_upload",
		Data: fileID,
	}

	// Return success with the newly created file ID
	task.Response <- UploadResult{FileID: fileID}
}

// backgroundJobWorker handles any background jobs from jobQueue (e.g., cleanup or post-processing).
func backgroundJobWorker() {
	for job := range jobQueue {
		switch job.Type {
		case "post_upload":
			fileID := job.Data.(int)
			log.Printf("Processing post-upload for file %d", fileID)
			// Add any logic needed after upload here (e.g. indexing, etc.)

		case "cleanup":
			filePath := job.Data.(string)
			if err := os.Remove(filePath); err != nil {
				log.Printf("Error deleting file %s: %v", filePath, err)
			} else {
				log.Printf("File %s successfully deleted.", filePath)
			}
		}
	}
}
