# Handy Commands for Working with AWS Lambda

Test locally.
```
docker run --rm -p 9000:8080 eyf-tools
curl --location --request POST 'http://localhost:9000/2015-03-31/functions/function/invocations' \
--header 'Content-Type: application/json' \
--data-raw '{
    "body": {
        "InitialLiquidBalance": 200000,
        "OriginalLoanAmount": 189600,
        "CurrentMortgageRate": 0.0475,
        "NumMonths": 360,
        "RemainingNumberOfMonthsOnCurrentLoan": 287,
        "NewLoanAmount": 169455.74,
        "NewInterestRate": 0.038,
        "NumMonthsNewLoan": 360,
        "ReFiCost": 4345,
        "MarketReturnRate": 0.07,
        "ShowCashOutRefi": true,
        "NewLoanAmountV2": 280000,
        "Show15yearRefi": true,
        "New15yearInterestRate": 0.032,
        "NumMonthsNewLoan15year": 180
    }
}'
```

Test remote endpoint using curl.
```
curl "https://pcqu45672xh4vva7orjff5rqly0epqhl.lambda-url.us-east-2.on.aws/"
```
