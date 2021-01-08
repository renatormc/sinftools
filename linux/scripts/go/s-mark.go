package main

import (
	"fmt"
	"os"
	"os/exec"
)

func main() {
	sinftools_dir := os.Getenv("SINFTOOLS")
	os.Setenv("PYTHONPATH", fmt.Sprintf("%s/tools/libs", sinftools_dir))
	script := fmt.Sprintf("%s/tools/sinf_mark_gui/main_window.py", sinftools_dir)
	args := []string{script}
	for _, item := range os.Args[1:] {
		args = append(args, item)
	}

	// cmd := exec.Command(fmt.Sprintf("%s/venv/bin/python3.8", sinftools_dir), args...)
	cmd := exec.Command(fmt.Sprintf("%s/venv/bin/python", sinftools_dir), args...)
	err := cmd.Start()

	if err != nil {
		println(err.Error())
		return
	}
}
