package main

import (
	"fmt"
	"os"
	"os/exec"
)

func main() {
	sinftools_dir := os.Getenv("SINFTOOLS")
	script := fmt.Sprintf("%s\\tools\\liga\\logon_confirm.py", sinftools_dir)
	args := []string{script}
	args = append(args, "manual")
	for _, item := range os.Args[1:] {
		args = append(args, item)
	}

	cmd := exec.Command(fmt.Sprintf("%s\\extras\\Python\\pythonw.exe", sinftools_dir), args...)
	err := cmd.Start()

	if err != nil {
		println(err.Error())
		return
	}
}
