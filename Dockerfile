# Build stage
FROM golang:1.24-alpine AS builder
WORKDIR /app
COPY . . 
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Final stage
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/main . 
COPY --from=builder /app/migrations ./migrations
COPY --from=builder /app/uploads ./uploads

EXPOSE 8080
CMD ["./main"]
