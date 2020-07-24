package main

import (
	"database/sql"
	"fmt"
	"io/ioutil"
	"log"
	"path/filepath"
	"strings"

	"github.com/google/logger"
	_ "github.com/mattn/go-sqlite3"
)

func findImage(folder string, name string) string {
	items, _ := ioutil.ReadDir(folder)
	for _, item := range items {
		if item.IsDir() {
			res := findImage(filepath.Join(folder, item.Name()), name)
			if res != "" {
				return res
			}
		} else if strings.ToLower(item.Name()) == strings.ToLower(name) {
			return filepath.Join(folder, item.Name())
		}
	}
	return ""
}

func putPortable(path string) {
	sleuthPath := filepath.Join(path, "sleuth.db")
	if fileExists(sleuthPath) {
		fmt.Printf("\nTornando pasta \"%s\" portable\n", path)
		db, err := sql.Open("sqlite3", sleuthPath)
		db.Exec("PRAGMA journal_mode=WAL;")
		defer db.Close()
		if err != nil {
			log.Fatal(err)
		}
		rows, _ := db.Query("SELECT name, sequence FROM tsk_image_names;")
		defer rows.Close()
		var name string
		var sequence int
		for rows.Next() {
			rows.Scan(&name, &sequence)
			filename := filepath.Base(name)
			imagePath := findImage(filepath.Join(filepath.Dir(path), "extracao"), filename)
			if imagePath == "" {
				log.Fatalf("O arquivo \"%s\" não foi encontrado.", filename)
			}
			newPath, _ := filepath.Rel(path, imagePath)
			tx, err := db.Begin()
			stm, err := db.Prepare("UPDATE tsk_image_names SET name = ? WHERE sequence = ?")
			if err != nil {
				log.Fatal(err)
			}
			_, err = stm.Exec(newPath, sequence)
			if err != nil {
				logger.Errorf("Erro ao tentar tornar portable \"\": %v", path, err)
				return
			}
			tx.Commit()
		}

	}
}
