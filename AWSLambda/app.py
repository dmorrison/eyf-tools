from MortgageRefinanceDecisionTemplate import MortgageRefinanceDecision
from output_mode import OutputMode

def handler(event, context):
    print("event: ", event)
    print('POST body:', event['body'])

    params = event['body']
    calculator = MortgageRefinanceDecision(params, OutputMode.JSON)
    results = calculator.calculate()

    return {
        'statusCode': 200,
        # 'body': {
        #     # 'msgFromHandler': 'Trying to send POST params.',
        #     # 'event': event,
        #     'endingLiquidBalanceOverTime': calculator.ending_liquid_balance_over_time,
        #     # 'balancePlotBase64Img': calculator.get_balances_plot_base64()
        # },
        'body': results,
    }
