#!/usr/bin/bash

curl -X POST -H "Content-Type: application/json" -d '{"username":"hnh-admin","password":"whoistheadmin","email":"xmon@hnh.com"}' http://127.0.0.1:8000/api/register/
