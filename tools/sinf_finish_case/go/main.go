package main

import (
	"fmt"
	"os"

	"github.com/akamensky/argparse"
	"github.com/google/logger"
)

func main() {

	parser := argparse.NewParser("sinf-finish-case", "Calculates hash and other things")
	nWorkers := parser.Int("w", "workers", &argparse.Options{Default: 4, Help: "Number of workers"})
	err := parser.Parse(os.Args)
	if err != nil {
		fmt.Print(parser.Usage(err))
		return
	}

	lf, err := os.OpenFile("hash.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0660)
	if err != nil {
		logger.Fatalf("Failed to open log file: %v", err)
	}
	defer lf.Close()

	defer logger.Init("LoggerExample", false, true, lf).Close()

	hasher := Hasher{root: ".", hashFile: ".\\hash.txt", nWorkers: *nWorkers}
	hasher.run()
}
