import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from io import BytesIO
import base64


# Compute and plot liquid account balance over time for different mortgage refinance / non-refinance options
# Include investment return opportunity costs (especially for closing costs) in all options

# Formula for computing monthly payments for given interest and loan amount:
# From https://www.thebalance.com/loan-payment-calculations-315564 and http://www.oxfordmathcenter.com/drupal7/node/434:
# P = L * ( r*(1+r)^n ) / ( (1+r)^n - 1)
# P = monthly payment
# L = Loan amount
# r = monthly interest rate = annual interest rate / 12 (not actually correct, but every source I find says this)
# n = number of payments = number of years * 12 (360 for 30 year mortgage)


#############################################################################################################
# Inputs

# * Total closing cost
# * Mortgage rate
# * Size of the loan (at most 80% of the value of the house, so that can have tradition mortgage with 20% equity)
# * Assumed annual return for the market

# # The initial liquid cash balance doesn't impact the difference in balances, so just use a reasonable number
# # that is larger than the new loan amount (otherwise it turns negative)
# InitialLiquidBalance = 400000
# # Original loan amount
# OriginalLoanAmount = 310400
# # Current mortgage rate
# CurrentMortgageRate = 0.03625
# # Number of months of current mortgage
# NumMonths = 360 # 30 year mortgage
# # Loan Origination Date 1/27/20. Original Maturity Date 2/1/50.
# # Current month: Jun 2020
# # So 7 months, plus 2021 to 2050
# RemainingNumberOfMonthsOnCurrentLoan = 6+(2050-2021)*12

# NewLoanAmount = 307593
# NewInterestRate = 0.02625 # Annual, for 30 year mortgage
# ReFiCost = 6707 # https://www.valuepenguin.com/mortgages/average-cost-of-refinance
# Possibly more accurate: 235+480+0.01*NewLoanAmount+255+275+750+733+138+58
# NumMonthsNewLoan = 360 # 30 year mortgage

# # Assumed rate of return for investments in index funds
# MarketReturnRate = 0.055 #0.04 #0.00 # annual

# # Evaluating cash-out refinance, using the additional funds to invest in the market:
# ShowCashOutRefi = False
# # If house is worth ~350k, and you get a mortgage for 80% of that: 280k
# NewLoanAmountV2 = 0.8*350000
# NewLoanV2minusCurrentBalance = NewLoanAmountV2-NewLoanAmount

# # Evaluating 15 year mortgage
# Show15yearRefi = False
# # NewLoanAmount same as 30 year refi
# New15yearInterestRate = 0.02625
# # ReFiCost same as 30 year refi
# NumMonthsNewLoan15year = 180 # 15 year mortgage
# # MarketReturnRate as 30 year refi

class RefiVsInvestCalculator:
    def __init__(self, params):
        self.params = params

        self.originalLoanAmount = int(params["originalLoanAmount"])
        self.currentMortgageRate = float(params["currentMortgageRate"]) / 100
        self.currentMortgageLengthInYears = int(params["currentMortgageLengthInYears"])
        self.remainingMonthsOnCurrentMortgage = int(params["remainingMonthsOnCurrentMortgage"])

        self.newLoanAmount = int(params["newLoanAmount"])
        self.newInterestRate = float(params["newInterestRate"]) / 100
        self.newMortgageLengthInYears = int(params["newMortgageLengthInYears"])
        self.closingCosts = int(params["closingCosts"])

        self.initialLiquidBalance = int(params["initialLiquidBalance"])
        self.rateOfReturn = int(params["rateOfReturn"]) / 100

    def calculate_balances_over_time(self):
        #############################################################################################################
        # Calculate different mortgage rates

        # Testing monthly payment calculation with our current mortgage:
        MonthlyMortgageRate = self.currentMortgageRate/12
        CurrentMonthlyPayment = self.originalLoanAmount * (MonthlyMortgageRate*(1+MonthlyMortgageRate)**(self.currentMortgageLengthInYears*12)) / \
            ((1+MonthlyMortgageRate)**(self.currentMortgageLengthInYears*12) - 1)
        print('Current monthly payment for 30-year mortgage = '+str(round(CurrentMonthlyPayment,2)))
        # TotalInterest = CurrentMonthlyPayment*NumMonths - OriginalLoanAmount

        # New loan payment for normal refi
        NewMonthlyMortgageRate = self.newInterestRate/12
        NewMonthlyPayment = self.newLoanAmount * (NewMonthlyMortgageRate*(1+NewMonthlyMortgageRate)**(self.currentMortgageLengthInYears*12)) / \
            ((1+NewMonthlyMortgageRate)**(self.currentMortgageLengthInYears*12) - 1)
        print('New monthly payment for 30-year refi = '+str(round(NewMonthlyPayment,2)))
        # TotalInterestNew = NewMonthlyPayment*NumMonths - OriginalLoanAmount

        # # New loan payment for cash-out refi (V2)
        # if ShowCashOutRefi:
        #     PnewV2 = NewLoanAmountV2 * (NewMonthlyMortgageRate*(1+NewMonthlyMortgageRate)**(self.currentMortgageLengthInYears*12)) / \
        #             ((1+NewMonthlyMortgageRate)**(self.currentMortgageLengthInYears*12) - 1)
        #     print('New monthly payment for cash-out refi = '+str(round(PnewV2,2)))

        # # new loan payment for 15 year refi
        # if Show15yearRefi:
        #     NewMonthly15yearInterestRate = New15yearInterestRate/12
        #     NewMonthlyPayment15Year = self.newLoanAmount * (NewMonthly15yearInterestRate*(1+NewMonthly15yearInterestRate)**NumMonthsNewLoan15year) / \
        #                 ((1+NewMonthly15yearInterestRate)**NumMonthsNewLoan15year - 1)
        #     print('New monthly payment for 15-year refi = '+str(round(NewMonthlyPayment15Year,2)))

        #############################################################################################################
        # Compute result of not refinancing, over the next 30 years (360 months)
        LiquidBalance = np.zeros(360+1)
        LiquidBalance[0] = self.initialLiquidBalance
        print(f'self.rateOfReturn: {self.rateOfReturn}')
        print(f'self.remainingMonthsOnCurrentMortgage: {self.remainingMonthsOnCurrentMortgage}')
        print(f'Initialized LiquidBalance[0] to {LiquidBalance[0]}')
        for ct in range(0,360):
            if ct < self.remainingMonthsOnCurrentMortgage:
                LiquidBalance[ct+1] = LiquidBalance[ct] - round(CurrentMonthlyPayment,2)
                LiquidBalance[ct+1] = LiquidBalance[ct+1] * (1+self.rateOfReturn/12) # simplification dividing by 12
            else:
                LiquidBalance[ct+1] = LiquidBalance[ct] * (1+self.rateOfReturn/12)  # simplification dividing by 12
            # print(f'LiquidBalance[{ct+1}]: {LiquidBalance[ct+1]}')


        #############################################################################################################
        # Result of refinancing, over the next 30 years (360 months)
        LiquidBalanceRefi = np.zeros(360+1)
        LiquidBalanceRefi[0] = self.initialLiquidBalance - self.closingCosts
        for ct in range(0,360):
            if ct < (self.newMortgageLengthInYears*12):
                LiquidBalanceRefi[ct+1] = LiquidBalanceRefi[ct] - round(NewMonthlyPayment,2)
                LiquidBalanceRefi[ct+1] = LiquidBalanceRefi[ct+1] * (1+self.rateOfReturn/12) # simplification dividing by 12
            else:
                LiquidBalanceRefi[ct+1] = LiquidBalanceRefi[ct] * (1+self.rateOfReturn/12)  # simplification dividing by 12

        # #############################################################################################################
        # # Result of refinancing at 80% current value, over the next 30 years (360 months)
        # if ShowCashOutRefi:
        #     LiquidBalanceRefiV2 = np.zeros(360+1)
        #     LiquidBalanceRefiV2[0] = self.initialLiquidBalance - self.closingCosts + NewLoanV2minusCurrentBalance
        #     for ct in range(0,360):
        #         if ct < (self.newMortgageLengthInYears*12):
        #             LiquidBalanceRefiV2[ct+1] = LiquidBalanceRefiV2[ct] - round(PnewV2,2)
        #             LiquidBalanceRefiV2[ct+1] = LiquidBalanceRefiV2[ct+1] * (1+self.rateOfReturn/12) # simplification dividing by 12
        #         else:
        #             LiquidBalanceRefiV2[ct+1] = LiquidBalanceRefiV2[ct] * (1+self.rateOfReturn/12)  # simplification dividing by 12

        # #############################################################################################################
        # # Result of refinancing, over the next 15 years (180 months)
        # if Show15yearRefi:
        #     LiquidBalanceRefi15yearRefi = np.zeros(360+1)
        #     LiquidBalanceRefi15yearRefi[0] = self.initialLiquidBalance - self.closingCosts
        #     for ct in range(0,360):
        #         if ct < NumMonthsNewLoan15year:
        #             LiquidBalanceRefi15yearRefi[ct+1] = LiquidBalanceRefi15yearRefi[ct] - round(NewMonthlyPayment15Year,2)
        #             LiquidBalanceRefi15yearRefi[ct+1] = LiquidBalanceRefi15yearRefi[ct+1] * (1+self.rateOfReturn/12) # simplification dividing by 12
        #         else:
        #             LiquidBalanceRefi15yearRefi[ct+1] = LiquidBalanceRefi15yearRefi[ct] * (1+self.rateOfReturn/12)  # simplification dividing by 12

        self.liquid_balance_over_time = LiquidBalance
        self.liquid_balance_over_time_with_refi = LiquidBalanceRefi

    @property
    def ending_liquid_balance_over_time(self):
        return self.liquid_balance_over_time[-1]

    @property
    def ending_liquid_balance_over_time_with_refi(self):
        return self.liquid_balance_over_time_with_refi[-1]
    
    def get_balances_plot_base64(self):
        MonthArray = np.arange(0,361)
        YearArray = MonthArray/12
        plt.plot(YearArray,self.liquid_balance_over_time/1000,'-b', label='No Refi') # markersize=5,
        plt.plot(YearArray,self.liquid_balance_over_time_with_refi/1000,'-r', label='Refi') # markersize=5,

        # if ShowCashOutRefi:
        #     plt.plot(YearArray,LiquidBalanceRefiV2/1000,'-g', label='Refi at 80%') #markersize=10,
        # if Show15yearRefi:
        #     plt.plot(YearArray,LiquidBalanceRefi15yearRefi/1000,'-c', label='15 year Refi') #markersize=10,

        # Add title
        plt.title('Balance With and Without Refinancing',fontsize=18)
        # x axis label
        plt.xlabel('Years',fontsize=15)
        # y axis label
        plt.ylabel('Balance ($k)',fontsize=15)
        plt.gca().tick_params(axis='both', which='major', labelsize=12)
        # add x-axis and y-axis limits if needed
        # Turn grid on
        plt.grid()
        # legend
        plt.legend(fontsize=15)
        # tight layout
        plt.tight_layout()

        # Generate base64-encoded iamge.
        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)
        balances_plot = base64.b64encode(figfile.getvalue())
        # Remove leading "b'" and trailing "'".
        balances_plot = str(balances_plot)[2:-1]

        plt.close()

        return balances_plot

