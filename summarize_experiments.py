import pickle
from os import listdir
from os.path import join
from CONFIG import *
from StratSupp.measurements import overall_trinary_monopoly
from StratSupp.plotting import final_heatmap


def summarize_experiments(path):
    exp_dicts = []
    for file in listdir(path):
        exp_dicts.append(pickle.load(open(join(path,file), "rb")))

    values_matrices_list = []
    for exp_dict in exp_dicts:
        values = [[0] * len(affinity_range) for i in promotion_range]
        for i in range(len(exp_dict['rec_df'])):
            df = exp_dict['rec_df'][i]
            p_index = promotion_range.index(exp_dict["promotion_factor"][i])
            a_index = affinity_range.index(exp_dict["affinity_change"][i])

            values[p_index][a_index] = overall_trinary_monopoly(df)
        values_matrices_list.append(values)

    final_heatmap(values_matrices_list)


if __name__ == '__main__':
    summarize_experiments('experiments')