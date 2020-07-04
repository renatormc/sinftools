package main

import (
	"os"
	"os/exec"
	"fmt"
)

func main() {
	os.Setenv("exec_mode", "sinf")
	sinftools_dir := os.Getenv("SINFTOOLS")
	cmd := exec.Command(fmt.Sprintf("%s\\Miniconda3\\pythonw.exe", sinftools_dir), fmt.Sprintf("%s\\tools\\report4\\reader\\gui_server.py", sinftools_dir))
	err := cmd.Start()

	if err != nil {
		println(err.Error())
		return
	}

}
