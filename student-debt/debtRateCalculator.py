

class DebtRateCalculator:
    """ debt_rate_calculator calculates the effective rate of interest and
        the total number of months taken to pay off ones student loan.

        Attributes
        ----------
        initial_monthly_salary : float
            the starting initial salary per month
        current_monthly_salary: float
            the monthly salary in month n
        monthly_raise_rate: float
        compounding_period: float
            In the post, we used monthly compounding. This leads to 'choppy'
            results. Increasing this value up to 100+ smooths out our results
            while still maintaining the relative performance of different strategies.
        compounding_period: float
        current_month: int
            the month we currently reside in, month n
        initial_debt: float
        current_debt: float
        current_total_paid: float
            running count of the total paid towards loan
        inflation_linked_rate: float
        interest_monthly_salary_floor : float
        interest_monthly_salary_ceiling: float
        max_adjustable_rate: float
        repayment_monthly_salary_floor: float

        Methods
        -------
        calculate(x)
            Does the computation.
    """

    def __init__(self,
                 initial_yearly_salary,
                 initial_debt=40000,
                 yearly_raise_rate=0.05,
                 interest_yearly_salary_floor=26575,
                 interest_yearly_salary_ceiling=47835,
                 max_adjustable_rate=0.03,
                 inflation_linked_rate=0.03,
                 repayment_yearly_salary_floor=26575,
                 compounding_period=365,
                 ):
        """ Set-up all the problem parameters"""
        self.initial_monthly_salary = initial_yearly_salary/compounding_period
        self.current_monthly_salary = initial_yearly_salary/compounding_period
        self.monthly_raise_rate = compounding_period*((1 + yearly_raise_rate)**(1/compounding_period) - 1)
        self.compounding_period = compounding_period
        self.current_month = 0
        self.initial_debt = initial_debt
        self.current_debt = initial_debt
        self.current_total_paid = 0
        self.inflation_linked_rate = inflation_linked_rate
        self.interest_monthly_salary_floor = interest_yearly_salary_floor/compounding_period
        self.interest_monthly_salary_ceiling = interest_yearly_salary_ceiling/compounding_period
        self.max_adjustable_rate = max_adjustable_rate
        self.repayment_monthly_salary_floor = repayment_yearly_salary_floor/compounding_period

    def __update_salary(self):
        """ Called every month to update current salary using the monthly
            rate. """
        self.current_monthly_salary *= (1 + self.monthly_raise_rate/self.compounding_period)

    def __calculate_repayment(self, x, compounded_debt):
        """ Called every month to calculate the months total repayment. """
        automatic_contribution = 0.09*max(0, self.current_monthly_salary
                                          - self.repayment_monthly_salary_floor)
        voluntary_contribution = x*self.current_monthly_salary
        payment = automatic_contribution + voluntary_contribution

        if compounded_debt - payment < 0:
            return compounded_debt

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
        self.current_total_paid += payment
        self.__update_salary()
        self.current_month += 1

    def __calculate_effective_rate(self):
        """ After the debt has been paid off, calculate the effective rate
            over the lifetime of the loan."""
        P = self.current_total_paid
        D = self.initial_debt
        N = self.current_month
        return (P/D)**(self.compounding_period/N) - 1

    def calculate(self, x=0):
        """ This function does the bulk of the work, calculating the effective
            rate and total number of months. """
        while self.current_month < 30*self.compounding_period and self.current_debt > 0:
            self.__next_month(x)

        R = self.__calculate_effective_rate()
        N = self.current_month

        # Finally we reset all member variables to their initial states
        self.current_debt = self.initial_debt
        self.current_monthly_salary = self.initial_monthly_salary
        self.current_month = 0
        self.current_total_paid = 0

        return R, N

