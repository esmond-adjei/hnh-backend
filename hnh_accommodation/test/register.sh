#!/usr/bin/env bash

# Check if all three arguments are provided
if [ $# -ne 3 ]; then
    echo "Usage: ./register.sh <username> <password> <email>"
    exit 1
fi

# Read the command-line arguments
username=$1
password=$2
email=$3

# Build the JSON payload
json_payload="{\"username\":\"$username\",\"password\":\"$password\",\"email\":\"$email\"}"

# Make the POST request using curl
curl -X POST -H "Content-Type: application/json" -d "$json_payload" http://127.0.0.1:8000/api/register/
