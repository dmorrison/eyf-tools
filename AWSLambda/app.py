import json
from MortgageRefinanceDecisionTemplate import MortgageRefinanceDecision

def handler(event, context):
    print("In Lambda handler. event: ", event)

    # The body for a post comes in as a JSON string. This converts it
    # to a dict.
    params = json.loads(event['body'])

    calculator = MortgageRefinanceDecision(params)
    results = calculator.calculate()

    return {
        'statusCode': 200,
        'body': results,
    }
