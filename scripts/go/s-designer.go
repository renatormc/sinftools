package main

import (
	"fmt"
	"os"
	"os/exec"
)

func main() {

	args := os.Args[1:]
	sinftools_dir := os.Getenv("SINFTOOLS")
	cmd := exec.Command(fmt.Sprintf("%s\\extras\\Python\\Lib\\site-packages\\pyqt5_tools\\Qt\\bin\\designer.exe", sinftools_dir), args...)
	err := cmd.Start()

	if err != nil {
		println(err.Error())
		return
	}

}
