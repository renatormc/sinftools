package main

import (
	"fmt"
	"os"
	"os/exec"
)

func main() {

	args := os.Args[1:]
	sinftools_dir := os.Getenv("SINFTOOLS")
	cmd := exec.Command(, args...)
	err := cmd.Start()

	if err != nil {
		println(err.Error())
		return
	}

}
