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


def summarize_values(list_of_values):
    non_negatives = [x for x in list_of_values if x>=0]
    if len(non_negatives) / len(list_of_values) < stability_percentage_bound:
        return -1
    return sum(non_negatives) / len(non_negatives)


def final_heatmap(list_of_matrices):
    summary = []

    for line_idx in range(len(list_of_matrices[0])):
        new_line = []
        for value_idx in range(len(list_of_matrices[0][0])):
            values_list = [matrix[line_idx][value_idx] for matrix in list_of_matrices]
            new_value = summarize_values(values_list)
            new_line.append(new_value)
        summary.append(new_line)

    _heatmap(summary, "Market State: Stability And Heterogeneity")