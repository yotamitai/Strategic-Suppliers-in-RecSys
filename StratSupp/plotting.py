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
    _ = plt.title(measurement_name)

    seaborn.heatmap(values, yticklabels=promotion_range, xticklabels=affinity_range, annot=True)
    plt.ylabel('promotion')
    plt.xlabel('affinity change')
    plt.show()


def heatmap(values, measurement_name):
    if isinstance(values[0][0], tuple):
        for i in range(len(values[0][0])):
            new_values = [[item[i] for item in row] for row in values]
            _heatmap(new_values, measurement_name[i])
    else:
        _heatmap(values, measurement_name)