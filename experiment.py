from datetime import datetime

from StratSupp.measurements import stability, heterogeneity, overall_trinary_monopoly, names_dict
from run import run
from CONFIG import *
import pickle
from StratSupp.plotting import heatmap, final_heatmap


f_measures = [overall_trinary_monopoly]
load = False



if __name__ == '__main__':

    n_measures = len(f_measures)

    exp_dicts = []
    if load:
        exp_dicts.append(pickle.load(open('1000_steps_2023-02-28_13-54-25.pkl', "rb")))

    else:  # get dataframes
        exp_dict = {"promotion_factor": [], "affinity_change": [], "rec_df": [], "pay_df": []}
        for promotion in promotion_range:
            for affinity in affinity_range:

                print(promotion, affinity)
                rec_df, pay_df = run(promotion, affinity)
                exp_dict["promotion_factor"].append(promotion)
                exp_dict["affinity_change"].append(affinity)
                exp_dict["rec_df"].append(rec_df)
                exp_dict["pay_df"].append(pay_df)

        # save
        exp_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(' ', '_').replace(':', '-')
        with open(exp_name + '.pkl', 'wb') as file:
            pickle.dump(exp_dict, file)

    # measurements
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


    # measurements
    # for f_measure in f_measures:
    #     values_matrices_list = []
    #     for exp_dict in exp_dicts:
    #         values = [[0] * len(affinity_range) for i in promotion_range]
    #         for i in range(len(exp_dict['rec_df'])):
    #             df = exp_dict['rec_df'][i]
    #             p_index = promotion_range.index(exp_dict["promotion_factor"][i])
    #             a_index = affinity_range.index(exp_dict["affinity_change"][i])
    #
    #             values[p_index][a_index] = f_measure(df)
    #         values_matrices_list.append(values)
    #
    #     heatmap(values, names_dict[f_measure])



    # print(f'Measurements from the {lookback_steps} last timestamps')
    # for i in range(len(exp_dict['rec_df'])):
    #     stability_values = stability(exp_dict['rec_df'][i])
    #     significances = []
    #     for v in stability_values:
    #         significances.append("--## High Value ##--" if v >= significance_stability_bound else "")
    #     print(f'Promotion: {exp_dict["promotion_factor"][i]:3.3}, '
    #           f'Affinity: {exp_dict["affinity_change"][i]:4.3}, '
    #           f'Stability:\n'
    #           f'\t\t\t\t\t\t\t\tMarketShare:      {stability_values[0]:5.3}\t\t{significances[0]}\n'
    #           f'\t\t\t\t\t\t\t\tMajoritySupplier: {stability_values[1]:5.3}\t\t{significances[1]}\n'
    #           f'\t\t\t\t\t\t\t\tNonZero:          {stability_values[2]:5.3}\t\t{significances[2]}\n'
    #           f'\t\t\t\t\t\t\t\tUserTopic:        {stability_values[3]:5.3}\t\t{significances[3]}\n')
    #     print(50 * '-')




