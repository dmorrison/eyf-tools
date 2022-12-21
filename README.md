# Handy Scripts for Working with AWS Lambda

Test locally.
```
docker run --rm -p 9000:8080 eyf-tools
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"eventKey":"foo"}'
```

Test remote endpoint using curl.
```
curl "https://pcqu45672xh4vva7orjff5rqly0epqhl.lambda-url.us-east-2.on.aws/"
```
