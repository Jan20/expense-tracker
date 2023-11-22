from application.domain.services.expense_analysis_service import ExpenseExpenseAnalysisService
from application.use_cases.chart_usecase import ChartUseCase
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
from matplotlib import cm

plt.close("all")
matplotlib.use('agg')
analysis_service = ExpenseExpenseAnalysisService()


class ChartService(ChartUseCase):

    def generate_monthly_expenses_chart(self) -> None:
        df = analysis_service.create_monthly_expenses_dataframe()
        plt.rcParams.update({'font.size': 4})

        # Pivot the DataFrame for plotting
        pivot_df = df.pivot(index='month', columns='description', values='amount')

        # Order the index
        pivot_df = pivot_df.sort_index()

        # Plot the stacked bar chart
        ax = pivot_df.plot(kind='bar', stacked=True, colormap='viridis')

        # Set labels and title
        ax.set(xlabel='Month', ylabel='Amount', title='Stacked Bar Chart of Amounts by Description')

        plt.savefig('foo.png', dpi=600)

    def generate_yearly_expenses_chart(self) -> None:
        df = analysis_service.create_yearly_expenses_dataframe()
        plt.rcParams.update({'font.size': 4})

        # Pivot the DataFrame for plotting
        # df = df.pivot(index='description', columns='amount', values='amount')
        df = df.sort_values(by='amount')

        colors = cm.viridis(np.linspace(0, 1, 10))
        plt.gca().set_prop_cycle(cycler('color', colors))

        ax = df.plot(kind='bar', x='description', y='amount', legend=False, rot=45, color=colors, figsize=(10, 6))
        # Annotate each bar with its corresponding amount value
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points')

        # Set labels and title
        ax.set(xlabel='Description', ylabel='Amount', title='Stacked Bar Chart of Amounts by Description')

        plt.savefig('foo.png', dpi=600)
