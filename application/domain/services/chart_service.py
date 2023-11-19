from application.domain.services.analysis_service import AnalysisService
from application.use_cases.chart_usecase import ChartUseCase
import matplotlib
import matplotlib.pyplot as plt

plt.close("all")
matplotlib.use('agg')
analysis_service = AnalysisService()


class ChartService(ChartUseCase):

    def generate_expense_chart(self, year: int):
        df = analysis_service.create_aggregated_expense_dataframe()

        # Pivot the DataFrame for plotting
        pivot_df = df.pivot(index='month', columns='description', values='amount')

        # Plot the stacked bar chart
        ax = pivot_df.plot(kind='bar', stacked=True, colormap='viridis')

        # Set labels and title
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount')
        ax.set_title('Stacked Bar Chart of Amounts by Description')

        plt.savefig('foo.png', dpi=600)
