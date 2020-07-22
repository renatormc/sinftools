package main

import (
	"crypto/sha512"
	"encoding/hex"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"path/filepath"
	"sync"

	"github.com/cheggaaa/pb/v3"
	"github.com/google/logger"
)

//Hasher df
type Hasher struct {
	// f         *os.File
	onlyCount bool
	nFiles    int64
	root      string
	hashFile  string
	// pBar      *pb.ProgressBar
	nWorkers int
	jobs     chan string
	results  chan Result
	wg       sync.WaitGroup
}

//Result is
type Result struct {
	Path     string
	HashText string
	Error    error
}

func calculateSha512(path string) (string, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer f.Close()

	h := sha512.New()
	if _, err := io.Copy(h, f); err != nil {
		return "", err
	}

	hasher := sha512.New()
	s, err := ioutil.ReadFile(path)
	hasher.Write(s)
	if err != nil {
		return "", err
	}
	return hex.EncodeToString(hasher.Sum(nil)), nil
}

func (hasher *Hasher) calcHashFile(path string) {
	if filepath.Base(path) == ".sinf_mark.json" {
		return
	}
	if hasher.onlyCount {
		hasher.nFiles++
		return
	}
	hasher.jobs <- path

}

func (hasher *Hasher) hashNormalFolder(path string) {
	items, _ := ioutil.ReadDir(path)
	for _, item := range items {
		if item.IsDir() {
			hasher.hashFolder(filepath.Join(path, item.Name()))
		} else {

			hasher.calcHashFile(filepath.Join(path, item.Name()))
		}
	}
}

func (hasher *Hasher) hashFolderIpedImages(path string) {
	items, _ := ioutil.ReadDir(path)
	for _, item := range items {
		if item.IsDir() {
			hasher.hashFolder(filepath.Join(path, item.Name()))
		} else {
			switch filepath.Ext(item.Name()) {
			case ".log", ".txt":
				hasher.calcHashFile(filepath.Join(path, item.Name()))
			}
		}
	}
}

func (hasher *Hasher) hashFolderIpedResults(path string) {
	item := filepath.Join(path, "FileList.csv")
	if !fileExists(item) {
		item = filepath.Join(path, "Lista de Arquivos.csv")
	}
	if fileExists(item) {
		hasher.calcHashFile(item)
	}
	putPortable(path)

}

func (hasher *Hasher) hashFolder(path string) {
	ok, marker := isHashPartial(path)
	if ok {
		switch marker.Subtype {
		case "iped_results":
			hasher.hashFolderIpedResults(path)
		case "iped_images":
			hasher.hashFolderIpedImages(path)
		}
	} else {
		hasher.hashNormalFolder(path)
	}
}

func (hasher *Hasher) countFiles() {
	fmt.Println("Contando arquivos. Aguarde, isso pode demorar.")
	hasher.onlyCount = true
	hasher.hashFolder(hasher.root)
	hasher.onlyCount = false
	fmt.Printf("%d arquivos encontrados\n", hasher.nFiles)
}

func (hasher *Hasher) workerHash() {
	defer func() {
		hasher.results <- Result{HashText: "finish"}
	}()

	for path := range hasher.jobs {
		// if path == "finish" {
		// 	return
		// }
		result := Result{}
		text, err := calculateSha512(path)
		if err != nil {
			result.Path, _ = filepath.Rel(hasher.root, path)
			result.HashText = ""
			result.Error = err
		} else {
			relPath, _ := filepath.Rel(hasher.root, path)
			result.Path = relPath
			result.HashText = text
		}
		hasher.results <- result
	}
	fmt.Println("Finalizou worker")
}

func (hasher *Hasher) run() {
	// var wg sync.WaitGroup
	hasher.jobs = make(chan string)
	hasher.results = make(chan Result)
	hasher.countFiles()
	logger.Info("Iniciando.")
	f, err := os.OpenFile(hasher.hashFile, os.O_CREATE|os.O_WRONLY, 0660)
	if err != nil {
		logger.Fatalf("Failed to open hash file: %v", err)
	}
	defer f.Close()
	pBar := pb.Full.Start64(hasher.nFiles)

	// hasher.wg.Add(hasher.nWorkers)
	for i := 0; i < hasher.nWorkers; i++ {
		go hasher.workerHash()
	}

	go func() {
		hasher.hashFolder(hasher.root)
		close(hasher.jobs)
	}()

	nRunning := hasher.nWorkers
	for result := range hasher.results {
		if result.Error != nil {
			logger.Errorf("Não foi possível calcular hash do arquivo \"%s\"", result.Path)
		} else if result.HashText == "finish" {
			nRunning--
			if nRunning == 0 {
				break
			}
			continue
		} else {
			fmt.Fprintf(f, "%s	%s\n", result.HashText, result.Path)
		}
		pBar.Increment()
	}

	// hasher.wg.Wait()
	pBar.Finish()
	res, err := calculateSha512(hasher.hashFile)
	if err != nil {
		logger.Fatalf("Failed to open hash file: %v", err)
	}
	fmt.Printf("Hash do hash: \n%s", res)
	logger.Infof("Finalizado")
	logger.Infof("Hash do hash: %s", res)
}
