package main

import (
	"os"

	"github.com/google/logger"
)

func main() {
	lf, err := os.OpenFile("hash.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0660)
	if err != nil {
		logger.Fatalf("Failed to open log file: %v", err)
	}
	defer lf.Close()

	defer logger.Init("LoggerExample", false, true, lf).Close()

	hasher := Hasher{root: ".", hashFile: ".\\hash.txt", nWorkers: 4}
	hasher.run()
}
