#!/bin/zsh
docker build -t eyf-tools -f AWSLambda/Dockerfile .
docker run --rm -p 9000:8080 eyf-tools
