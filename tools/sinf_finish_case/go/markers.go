package main

import (
	"encoding/json"
	"io/ioutil"
	"os"
	"path/filepath"
)

//Marker stores a marker info
type Marker struct {
	Type    string `json:"type"`
	Name    string `json:"name"`
	Subtype string `json:"subtype"`
	Role    string `json:"role"`
}

func getMarkers(folder string) []Marker {
	path := filepath.Join(folder, ".sinf_mark.json")
	jsonFile, err := os.Open(path)
	if os.IsNotExist(err) {
		return nil
	}
	defer jsonFile.Close()
	byteValue, _ := ioutil.ReadAll(jsonFile)
	var markers []Marker
	json.Unmarshal([]byte(byteValue), &markers)
	return markers
}

func isHashPartial(path string) (bool, *Marker) {
	markers := getMarkers(path)
	for _, marker := range markers {
		if marker.Type == "hash_partial" {
			return true, &marker
		}
	}
	return false, nil
}
