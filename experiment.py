from datetime import datetime

from StratSupp.measurements import stability, heterogeneity, overall_trinary_monopoly, names_dict
from run import run
from CONFIG import *
import pickle
from StratSupp.plotting import heatmap


f_measures = [overall_trinary_monopoly]



if __name__ == '__main__':
    load = True

    n_measures = len(f_measures)

    if load:
        exp_dict = pickle.load(open('1000_steps_2023-02-28_13-54-25.pkl', "rb"))

    else:  # get dataframes
        n_promotions = len(promotion_range)  # New
        n_affinities = len(affinity_range)  # New
        measure_tables = [] # New
        for f_measure in f_measures: # New
            measure_tables.append([[0] * affinity_range for i in range(promotion_range)])   # New

        exp_dict = {"promotion_factor": [], "affinity_change": [], "rec_df": [], "pay_df": []}
        for promotion_idx in range(n_promotions):
            promotion = promotion_range[promotion_idx]  # New
            for affinity_idx in range(n_affinities):
                affinity = affinity_range[affinity_idx]  #New

                print(promotion, affinity)
                rec_df, pay_df = run(promotion, affinity)
                exp_dict["promotion_factor"].append(promotion)
                exp_dict["affinity_change"].append(affinity)
                exp_dict["rec_df"].append(rec_df)
                exp_dict["pay_df"].append(pay_df)

                for i in range(n_measures):     # New
                    measure_tables[i][promotion_idx][affinity_idx] = f_measures[i](rec_df)   # New

        # save
        exp_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(' ', '_').replace(':', '-')
        with open(exp_name + '.pkl', 'wb') as file:
            pickle.dump(exp_dict, file)

        for measure_table in measure_tables:                    # New
            heatmap(measure_table, names_dict(measure_table))   # New

    # measurements
    print(f'Measurements from the {lookback_steps} last timestamps')
    for i in range(len(exp_dict['rec_df'])):
        stability_values = stability(exp_dict['rec_df'][i])
        significances = []
        for v in stability_values:
            significances.append("--## High Value ##--" if v >= significance_stability_bound else "")
        print(f'Promotion: {exp_dict["promotion_factor"][i]:3.3}, '
              f'Affinity: {exp_dict["affinity_change"][i]:4.3}, '
              f'Stability:\n'
              f'\t\t\t\t\t\t\t\tMarketShare:      {stability_values[0]:5.3}\t\t{significances[0]}\n'
              f'\t\t\t\t\t\t\t\tMajoritySupplier: {stability_values[1]:5.3}\t\t{significances[1]}\n'
              f'\t\t\t\t\t\t\t\tNonZero:          {stability_values[2]:5.3}\t\t{significances[2]}\n'
              f'\t\t\t\t\t\t\t\tUserTopic:        {stability_values[3]:5.3}\t\t{significances[3]}\n')
        print(50 * '-')


