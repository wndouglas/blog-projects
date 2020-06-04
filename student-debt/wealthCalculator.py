class WealthCalculator:
    """ WealthCalculator calculates the total accrued wealth across the 30 year
        period of investment.

        Methods
        -------
        calculate(x)
            Does the computation.
    """

    def __init__(self,
                 initial_yearly_salary,
                 initial_debt=36000,
                 yearly_raise_rate=0.036,
                 yearly_return=0.05,
                 disposable_income_fraction=0.4,
                 interest_yearly_salary_floor=26575,
                 interest_yearly_salary_ceiling=47835,
                 max_adjustable_rate=0.03,
                 inflation_linked_rate=0.03,
                 repayment_yearly_salary_floor=26575,
                 compounding_period=12):
        """ Set-up all the problem parameters"""
        self.current_monthly_salary = initial_yearly_salary/compounding_period
        self.current_asset_price = 1
        self.monthly_raise_rate = compounding_period*((1 + yearly_raise_rate)**(1/compounding_period) - 1)
        self.compounding_period = compounding_period
        self.quantity_invested = 0
        self.disposable_income_fraction = disposable_income_fraction
        self.current_month = 0
        self.is_repaid = False
        self.available_investment_income = disposable_income_fraction*initial_yearly_salary/compounding_period
        self.monthly_return = compounding_period*((1 + yearly_return)**(1/compounding_period) - 1)
        self.current_debt = initial_debt
        self.time_to_repay = 30*compounding_period
        self.inflation_linked_rate = inflation_linked_rate
        self.interest_monthly_salary_floor = interest_yearly_salary_floor/compounding_period
        self.interest_monthly_salary_ceiling = interest_yearly_salary_ceiling/compounding_period
        self.max_adjustable_rate = max_adjustable_rate
        self.repayment_monthly_salary_floor = repayment_yearly_salary_floor/compounding_period

    def __update_salary(self):
        """ Called every month to update current salary using the monthly
            rate. """
        self.current_monthly_salary *= (1 + self.monthly_raise_rate/self.compounding_period)

    def __update_quantity_invested(self):
        """ Update the current quantity invested in the risky asset. """
        self.quantity_invested += self.available_investment_income/self.current_asset_price

    def __update_asset_price(self):
        """ Called every month to update current asset price using the monthly
            rate. """
        self.current_asset_price *= (1 + self.monthly_return/self.compounding_period)

    def __calculate_repayment(self, x, compounded_debt):
        """ Called every month to calculate the months total repayment. """
        self.available_investment_income = self.current_monthly_salary*self.disposable_income_fraction

        if self.is_repaid:
            return 0

        automatic_contribution = 0.09*max(0, self.current_monthly_salary
                                          - self.repayment_monthly_salary_floor)

        remaining_income = self.available_investment_income - automatic_contribution
        voluntary_contribution = x*remaining_income

        if compounded_debt <= 0:
            self.is_repaid = True
            self.time_to_repay = self.current_month
            automatic_contribution = 0
            voluntary_contribution = 0

        if compounded_debt - automatic_contribution < 0:
            automatic_contribution = compounded_debt
            voluntary_contribution = 0

        if compounded_debt - automatic_contribution < voluntary_contribution:
            voluntary_contribution = compounded_debt - automatic_contribution

        total_loan_contribution = automatic_contribution + voluntary_contribution
        self.available_investment_income -= total_loan_contribution

        return automatic_contribution + voluntary_contribution

    def __calculate_debt_interest(self):
        """ Calculate the current interest paid on the loan based on current
            salary. """
        fixed_rate = self.inflation_linked_rate
        floating_rate = 0

        s = self.current_monthly_salary
        l = self.interest_monthly_salary_floor
        u = self.interest_monthly_salary_ceiling

        if l <= s <= u:
            floating_rate = self.max_adjustable_rate*(s - l)/(u - l)
        elif s > u:
            floating_rate = self.max_adjustable_rate

        return fixed_rate + floating_rate

    def __next_month(self, x):
        """ This function takes us to the next month and updates all the
            relevant quantities. """
        rate = self.__calculate_debt_interest()
        compounded_debt = (1 + rate/self.compounding_period)*self.current_debt
        payment = self.__calculate_repayment(x, compounded_debt)
        self.current_debt = compounded_debt - payment

        self.__update_asset_price()
        self.__update_quantity_invested()

        self.__update_salary()
        self.current_month += 1

    def calculate(self, x=0):
        """ This function does the bulk of the work, calculating the final wealth
         and total number of months. """
        while self.current_month < 30*self.compounding_period:
            self.__next_month(x)

        terminal_wealth = self.current_asset_price*self.quantity_invested

        return terminal_wealth, self.time_to_repay

