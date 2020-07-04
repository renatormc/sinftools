package main

import (
	"os"
	"os/exec"
)

func main() {

	os.Setenv("exec_mode", "portable")
	cmd := exec.Command(".report\\gui_server\\gui_server.exe")
	err := cmd.Start()

	if err != nil {
		println(err.Error())
		return
	}

}
