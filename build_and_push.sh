#!/bin/zsh
aws ecr get-login-password | docker login --username AWS --password-stdin 878978020374.dkr.ecr.us-east-2.amazonaws.com/eyf-tools
docker build -t eyf-tools .
docker tag eyf-tools:latest 878978020374.dkr.ecr.us-east-2.amazonaws.com/eyf-tools:latest
docker push 878978020374.dkr.ecr.us-east-2.amazonaws.com/eyf-tools:latest

# curl "https://pcqu45672xh4vva7orjff5rqly0epqhl.lambda-url.us-east-2.on.aws/"
