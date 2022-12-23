#!/bin/zsh
docker build -t eyf-tools .
docker run --rm -p 9000:8080 eyf-tools
