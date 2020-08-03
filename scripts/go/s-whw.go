package main

import (
	"fmt"
	"os"
	"os/exec"
)

func main() {
	sinftools_dir := os.Getenv("SINFTOOLS")
	script := fmt.Sprintf("%s\\tools\\word_helper\\cmd.py", sinftools_dir)
	args := []string{script}
	for _, item := range os.Args[1:] {
		args = append(args, item)
	}

	cmd := exec.Command(fmt.Sprintf("%s\\extras\\Python\\python.exe", sinftools_dir), args...)
	err := cmd.Start()

	if err != nil {
		println(err.Error())
		return
	}
}
