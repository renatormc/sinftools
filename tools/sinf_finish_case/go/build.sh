#!/bin/bash
env GOOS=windows GOARCH=amd64 go build -a -o "sinf_finish_case.exe"
env GOOS=linux GOARCH=amd64 go build -a -o "sinf_finish_case"