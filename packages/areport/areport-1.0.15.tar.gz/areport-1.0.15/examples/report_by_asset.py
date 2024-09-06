import pandas as pd
from areport import Report

# Create a report
pf_values = pd.read_csv('pf_values.csv', index_col=0)
exposures = pd.read_csv('exposure.csv', index_col=0)

pf_values.index = pd.to_datetime(pf_values.index)
pf_values.index = [x.timestamp() for x in pf_values.index]

report = Report(pf_values.squeeze())
monthly_returns = report.annual_return_by_asset(exposures.shift(1))
monthly_returns.to_csv("monthly_returns.csv")

# report.print_metrics()
# report.metrics_to_csv(file_name='report_metrics.csv')