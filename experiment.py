from datetime import datetime

from StratSupp.measurements import stability, heterogeneity
from run import run
from CONFIG import *

import pickle

if __name__ == '__main__':
    promotion_range = list(np.linspace(0, 5, 11))
    affinity_range = [round(x, 1) for x in np.linspace(-2, 2, 11)]

    load = True

    if load:
        exp_dict = pickle.load(open('1000_steps_2023-02-28_13-54-25.pkl', "rb"))

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
    significance_bound = 1.0  # TODO define significance bound
    print(f'Measurements from the {lookback_steps} last timestamps')
    for i in range(len(exp_dict['rec_df'])):
        stability_values = stability(exp_dict['rec_df'][i])
        significances = []
        for v in stability_values:
            significances.append("--## High Value ##--" if v >= significance_bound else "")
        print(f'Promotion: {exp_dict["promotion_factor"][i]:3.3}, '
              f'Affinity: {exp_dict["affinity_change"][i]:4.3}, '
              f'Stability:\n'
              f'\t\t\t\t\t\t\t\tMarketShare:      {stability_values[0]:5.3}\t\t{significances[0]}\n'
              f'\t\t\t\t\t\t\t\tMajoritySupplier: {stability_values[1]:5.3}\t\t{significances[1]}\n'
              f'\t\t\t\t\t\t\t\tNonZero:          {stability_values[2]:5.3}\t\t{significances[2]}\n'
              f'\t\t\t\t\t\t\t\tUserTopic:        {stability_values[3]:5.3}\t\t{significances[3]}\n')
        print(50 * '-')
