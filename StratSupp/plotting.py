import matplotlib.pyplot as plt
import seaborn
from CONFIG import *


def plot_supplier_over_time(df, subject):
    df.pivot('timestamp', 'supplier', subject).plot.line(
        title=f'Supplier {subject} over time ',
        xlabel='Time ($t$)',
        ylabel=f'{subject}',
        figsize=(12, 6),
        )
    plt.show()


def _heatmap(values, measurement_name):
    plt.ylabel('promotion')
    plt.xlabel('affinity change')
    _ = plt.title(measurement_name)
    seaborn.heatmap(values, yticklabels=promotion_range, xticklabels=affinity_range)
    plt.show()


def heatmap(values, measurement_name):
    if values is tuple:
        for i in range(len(values)):
            new_measurement_name = measurement_name+" "+str(i)
            _heatmap(values, new_measurement_name)
    else:
        _heatmap(values, measurement_name)