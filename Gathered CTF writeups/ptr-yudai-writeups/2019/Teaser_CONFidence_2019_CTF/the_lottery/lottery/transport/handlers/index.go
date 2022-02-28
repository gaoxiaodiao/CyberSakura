package handlers

import (
	"net/http";
	"fmt"
)

func (h *Handlers) IndexGet(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "200 API OK")
}
