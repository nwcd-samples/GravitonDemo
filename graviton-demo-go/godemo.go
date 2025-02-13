package main

import (
	"bytes"
	"context"
	"fmt"
	"io"
	"net"
	"net/http"
	"os/exec"
	"strings"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/feature/ec2/imds"
)

func main() {
	fmt.Println("Server is running on http://0.0.0.0:5000")
	http.HandleFunc("/", DemoServer)
	http.ListenAndServe(":5000", nil)
}

func getIP(r *http.Request) (string, error) {
	ips := r.Header.Get("X-Forwarded-For")
	splitIps := strings.Split(ips, ",")

	if len(splitIps) > 0 {
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
		if ip == "::1" {
			return "127.0.0.1", nil
		}
		return ip, nil
	}

	return "", nil
}

func DemoServer(w http.ResponseWriter, r *http.Request) {
	// Get Golang version
	cmd := exec.Command("go", "version")
	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Run()
	runtimever := out.String()

	// Get client IP
	ip, _ := getIP(r)

	// Fetch EC2 metadata using AWS SDK v2
	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		fmt.Fprintf(w, "Error loading AWS config: %v", err)
		return
	}

	client := imds.NewFromConfig(cfg)

	// Get instance ID
	instanceIDResp, err := client.GetMetadata(context.TODO(), &imds.GetMetadataInput{
		Path: "instance-id",
	})
	if err != nil {
		fmt.Fprintf(w, "Error getting instance ID: %v", err)
		return
	}
	defer instanceIDResp.Content.Close()
	instanceID, err := io.ReadAll(instanceIDResp.Content)

	// Get instance type
	instanceTypeResp, err := client.GetMetadata(context.TODO(), &imds.GetMetadataInput{
		Path: "instance-type",
	})
	if err != nil {
		fmt.Fprintf(w, "Error getting instance type: %v", err)
		return
	}
	defer instanceTypeResp.Content.Close()
	instanceType, err := io.ReadAll(instanceTypeResp.Content)

	// Get public IP
	publicIPResp, err := client.GetMetadata(context.TODO(), &imds.GetMetadataInput{
		Path: "public-ipv4",
	})
	if err != nil {
		fmt.Fprintf(w, "Error getting public IP: %v", err)
		return
	}

	defer publicIPResp.Content.Close()
	publicIP, err := io.ReadAll(publicIPResp.Content)
	// Output
	fmt.Fprintf(w, "<html><body>")
	fmt.Fprintf(w, "<h1>Graviton University Golang Demo</h1>")
	fmt.Fprintf(w, "<p>Instance Type is : %s</p>", instanceType)
	fmt.Fprintf(w, "<p>Instance ID is : %s</p>", instanceID)
	fmt.Fprintf(w, "<p>Server Public IP is : %s</p>", publicIP)
	fmt.Fprintf(w, "<p>Runtime is : %s</p>", runtimever)
	fmt.Fprintf(w, "<p>Request From : %s</p>", ip)
	fmt.Fprintf(w, "</body></html>")
}
