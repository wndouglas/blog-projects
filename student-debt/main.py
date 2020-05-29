from debtRateCalculator import DebtRateCalculator
import matplotlib.pyplot as plt

if __name__ == '__main__':
    yearly_salary = 40000
    effective_rates = []
    months = []
    num_rates = 100
    voluntary_repayment_rates = [0.2*x/num_rates for x in range(num_rates)]

    debt_calculator = DebtRateCalculator(yearly_salary)
    for voluntary_repayment_rate in voluntary_repayment_rates:
        (R, N) = debt_calculator.calculate(voluntary_repayment_rate)
        effective_rates.append(R)
        months.append(N)

    plt.plot(voluntary_repayment_rates, effective_rates)
    plt.show()

    # Now we plot the effective rate vs salary for a range of salaries if we
    # don't make any repayments
    min_salary = 30000
    max_salary = 60000
    num_salaries = 100
    effective_rates = []
    years_to_repayment = []
    salaries = [min_salary + x*(max_salary-min_salary)/num_salaries for x in range(num_salaries)]
    for salary in salaries:
        debt_calculator = DebtRateCalculator(salary)
        (R, N) = debt_calculator.calculate(0.5)
        effective_rates.append(R)
        years_to_repayment.append(N/365)

    plt.plot(salaries, effective_rates)
    plt.show()
    plt.plot(salaries, years_to_repayment)
    plt.show()



