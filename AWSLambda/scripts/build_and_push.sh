#!/bin/zsh
aws ecr get-login-password | docker login --username AWS --password-stdin 878978020374.dkr.ecr.us-east-2.amazonaws.com/eyf-tools
docker build -t eyf-tools -f AWSLambda/Dockerfile .
docker tag eyf-tools:latest 878978020374.dkr.ecr.us-east-2.amazonaws.com/eyf-tools:latest
docker push 878978020374.dkr.ecr.us-east-2.amazonaws.com/eyf-tools:latest
