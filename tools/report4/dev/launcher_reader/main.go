package main

import (
    "os/exec"
)

func main() {
	cmd := exec.Command(".\\.report\\sinf_reader\\sinf_reader-win32-x64\\sinf_reader.exe")
    err := cmd.Start()

    if err != nil {
        println(err.Error())
        return
    }
}
