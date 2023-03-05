package main

import (
	"fmt"
	"net"
	"net/http"
	"io/ioutil"
	"os/exec"
	"bytes"
	"strings"
)

func main() {
	fmt.Println("Server is running on http://0.0.0.0:5000")
	http.HandleFunc("/",DemoServer)
	http.ListenAndServe(":5000",nil)
	
}

// getIP returns the ip address from the http request
func getIP(r *http.Request) (string, error) {
	ips := r.Header.Get("X-Forwarded-For")
	splitIps := strings.Split(ips, ",")

	if len(splitIps) > 0 {
		// get last IP in list since ELB prepends other user defined IPs, meaning the last one is the actual client IP.
		netIP := net.ParseIP(splitIps[len(splitIps)-1])
		if netIP != nil {
			return netIP.String(), nil
		}
	}

	ip, _, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil {
		return "", err
	}

	netIP := net.ParseIP(ip)
	if netIP != nil {
		ip := netIP.String()
		if ip == "::1" {
			return "127.0.0.1", nil
		}
		return ip, nil
	}

	return "", nil
}

func GetMetadata(url string) (string) {
        resp, err := http.Get(url)
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	//fmt.Println(string(body))
	if(err != nil) {
		return ""
	}
	return string(body)
}

func DemoServer(w http.ResponseWriter, r *http.Request) {
	//get golang version
	cmd := exec.Command("go","version")
	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Run()
	runtimever := out.String()

	//get client IP
	ip, _ := getIP(r)
	//output 
	fmt.Fprintf(w,"<html><body>")
	fmt.Fprintf(w, "<h1>Graviton University Golang Demo</h1>")
	fmt.Fprintf(w, "<p>Instance Type is : %s</p>",GetMetadata("http://169.254.169.254/latest/meta-data/instance-type"))
	fmt.Fprintf(w, "<p>Instance ID is : %s</p>",GetMetadata("http://169.254.169.254/latest/meta-data/instance-id"))
	fmt.Fprintf(w, "<p>Server Public IP is : %s</p>",GetMetadata("http://169.254.169.254/latest/meta-data/public-ipv4"))
	fmt.Fprintf(w, "<p>Runtime is : %s</p>",runtimever)
	fmt.Fprintf(w, "<p>Request From : %s</p>",ip)
	fmt.Fprintf(w,"</body></html>")
}
