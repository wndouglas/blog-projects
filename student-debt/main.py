from debtRateCalculator import DebtRateCalculator
from wealthCalculator import WealthCalculator
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def rate_vs_salary_plots():
    min_salary = 25000
    max_salary = 65000
    num_salaries = 100
    salaries = [min_salary + x * (max_salary - min_salary) / num_salaries for x in range(num_salaries)]

    num_repayment_rates = 4
    min_repayment_rate = 0
    max_repayment_rate = 0.2
    repayment_rates = [min_repayment_rate + x*(max_repayment_rate - min_repayment_rate)/num_repayment_rates for x in range(num_repayment_rates + 1)]
    effective_rates_mat = []
    years_to_repayment_mat = []

    rate_plot_legend_data = []
    for repayment_rate in repayment_rates:
        rate_plot_legend_data.append("repayment rate = " + "{:.2f}".format(repayment_rate))
        effective_rates = []
        years_to_repayment = []
        for salary in salaries:
            debt_calculator = DebtRateCalculator(salary)
            (R, N, total_spent) = debt_calculator.calculate(repayment_rate)
            effective_rates.append(R * 100)
            years_to_repayment.append(N / 360)
        effective_rates_mat.append(effective_rates)
        years_to_repayment_mat.append(years_to_repayment)

    sf = 0.75
    fig, axs = plt.subplots(2, sharex=True, figsize=(16*sf, 12*sf))
    fig.suptitle('Effective Annual Rate and Years to Finish Repaying vs Initial Salary')


    for i in range(len(repayment_rates)):
        axs[0].plot(salaries, effective_rates_mat[i])
        axs[1].plot(salaries, years_to_repayment_mat[i])

    axs[0].set_ylabel("Effective rate of interest (%)")
    axs[1].set_ylabel("Time to full repayment (years)")

    for ax in axs:
        ax.set_xlabel("Yearly salary (£)")
        ax.legend(rate_plot_legend_data)

    plt.show()

def rate_vs_repayment_rate_plots():
    min_salary = 50000
    max_salary = 80000
    num_salaries = 1
    salaries = [min_salary + x * (max_salary - min_salary) / num_salaries for x in range(num_salaries)]

    num_repayment_rates = 100
    min_repayment_rate = 0
    max_repayment_rate = 0.5
    repayment_rates = [(min_repayment_rate + x*(max_repayment_rate - min_repayment_rate)/num_repayment_rates)*100 for x in range(num_repayment_rates + 1)]
    effective_rates_mat = []
    total_spends_mat = []

    rate_plot_legend_data = []
    for salary in salaries:
        rate_plot_legend_data.append("initial salary = " + "{:.0f}".format(salary))
        effective_rates = []
        total_spends = []
        debt_calculator = DebtRateCalculator(salary)
        for repayment_rate in repayment_rates:
            (R, _, total_spent) = debt_calculator.calculate(repayment_rate/100)
            effective_rates.append(R * 100)
            total_spends.append(total_spent)
        effective_rates_mat.append(effective_rates)
        total_spends_mat.append(total_spends)

    sf = 0.75
    fig, axs = plt.subplots(2, sharex=True, figsize=(16*sf, 9*sf))
    fig.suptitle('Effective Annual Rate and Total Spent on Repayment vs Repayment Rate')

    for i in range(len(salaries)):
        axs[0].plot(repayment_rates, effective_rates_mat[i])
        axs[1].plot(repayment_rates, total_spends_mat[i])

    axs[0].set_ylabel("Effective rate of interest (%)")
    axs[1].set_ylabel("Total spent on repayment (£)")

    axs[0].set_xlabel("Repayment Rate (%)")
    axs[1].set_xlabel("Repayment Rate (%)")

    for ax in axs:
        ax.legend(rate_plot_legend_data)

    plt.show()


def wealth_vs_prepayment_proportion_plots():
    min_salary = 10000
    max_salary = 40000
    num_salaries = 3
    salaries = [max_salary - x * (max_salary - min_salary) / num_salaries for x in range(num_salaries)]

    num_repayment_proportions = 1000
    min_repayment_rate = 0
    max_repayment_rate = 1
    repayment_proportions = [min_repayment_rate + x * (max_repayment_rate - min_repayment_rate) / num_repayment_proportions for x in
                       range(num_repayment_proportions + 1)]
    terminal_wealths_mat = []
    time_to_repays_mat = []

    rate_plot_legend_data = []
    for salary in salaries:
        rate_plot_legend_data.append("Salary = " + "{:.2f}".format(salary))
        terminal_wealths = []
        time_to_repays = []
        for repayment_proportion in repayment_proportions:
            wealth_calculator = WealthCalculator(salary)
            (terminal_wealth, time_to_repay) = wealth_calculator.calculate(repayment_proportion)
            terminal_wealths.append(terminal_wealth/1e6)
            time_to_repays.append(time_to_repay/12)

        terminal_wealths_mat.append(terminal_wealths)
        time_to_repays_mat.append(time_to_repays)

    sf = 0.75
    fig, axs = plt.subplots(3, sharex=True, figsize=(16 * sf, 12 * sf))

    for i in range(len(salaries)):
        axs[0].plot(repayment_proportions, terminal_wealths_mat[i])
        axs[2].plot(repayment_proportions, time_to_repays_mat[i])

    axs[1].plot(repayment_proportions, terminal_wealths_mat[0])

    axs[0].set_ylabel("Terminal wealth (Millions £)")
    axs[0].set_xlabel("Repayment proportion")
    axs[0].set_title("Terminal wealth vs repayment proportion")
    axs[0].legend(rate_plot_legend_data)

    axs[2].set_ylabel("Time to repay (Years)")
    axs[2].set_xlabel("Repayment proportion")
    axs[2].set_title("Time to repayment vs repayment proportion, Salary = £40,000")
    axs[2].legend(rate_plot_legend_data)

    axs[1].set_ylabel("Terminal wealth (Millions £)")
    axs[1].set_title("Terminal wealth vs repayment proportion, Salary = £40,000")
    axs[1].set_xlabel("Repayment proportion")

    fig.tight_layout()
    plt.savefig('wealth.png', bbox_inches='tight', quality=100)
    plt.show()


if __name__ == '__main__':
    wealth_vs_prepayment_proportion_plots()



