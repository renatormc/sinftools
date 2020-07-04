package main

import (
	"fmt"
	"os"
	"os/exec"
)

func main() {
	sinftools_dir := os.Getenv("SINFTOOLS")
	script := fmt.Sprintf("%s\\\\extras\\Python\\\Scripts\\idlex.pyw", sinftools_dir)
	args := []string{script}
	for _, item := range os.Args[1:] {
		args = append(args, item)
	}

	cmd := exec.Command(fmt.Sprintf("%s\\\\extras\\Python\\\pythonw.exe", sinftools_dir), args...)
	err := cmd.Start()

	if err != nil {
		println(err.Error())
		return
	}
}
