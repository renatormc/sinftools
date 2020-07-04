package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/hello/{name}", HelloHandler)
	http.Handle("/", r)
	log.Fatal(http.ListenAndServe(":8000", r))
}

func HelloHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, "<h1>Título</h1>")
	fmt.Fprintf(w, "Nome: %v\n", vars["name"])

}
