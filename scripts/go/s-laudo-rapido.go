package main

import (
	"fmt"
	"os"
	"os/exec"
)

func main() {
	sinftools_dir := os.Getenv("SINFTOOLS")
	cmd := exec.Command(fmt.Sprintf("%s\\Miniconda3\\pythonw.exe", sinftools_dir), fmt.Sprintf("%s\\tools\\laudo_editor\\laudo_rapido2\\main.py", sinftools_dir))
	err := cmd.Start()
	if err != nil {
		println(err.Error())
		return
	}
}
