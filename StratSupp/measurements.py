from collections import defaultdict

import numpy as np

from StratSupp.utils import topic_histogram
from CONFIG import *


def _shares_in_numbers(df_rec, time_step, return_indices=False):
    n_topics = topics_params["n_topics"]

    df_timestamp = df_rec[df_rec["timestamp"] == time_step]
    hist = topic_histogram(df_timestamp['latent_topic'].values, n_topics)
    market_shares = [round((x / df_timestamp.shape[0]), 3) for x in hist]

    major = -1
    for i, x in enumerate(market_shares):
        if x > 0.5:
            major = i

    non_zero_topics = df_timestamp['latent_topic'].unique().tolist()

    if return_indices:
        return major, non_zero_topics

    major_binary = min(1, major + 1)

    if len(non_zero_topics) == 1:
        monopoly_binary = 0
    else:
        monopoly_binary = 1

    monopoly_continuous = len(non_zero_topics) / n_topics

    return major_binary, monopoly_binary, monopoly_continuous


def heterogeneity(df_rec):
    last_timestamp = bidding_simulation_params["num_steps"]
    return _shares_in_numbers(df_rec, last_timestamp, return_indices=False)


def stability(df_rec):
    market_share = market_share_stability(df_rec)
    majority_supplier, non_zero_suppliers = supplier_stability(df_rec)
    users = user_stability(df_rec)

    return round(market_share,3), round(majority_supplier,3), round(non_zero_suppliers,3), round(users,3)


def market_share_stability(df_rec, verbose=False):
    n_topics = topics_params["n_topics"]
    last_timestamp = bidding_simulation_params["num_steps"]
    lookback_timestamps = range(last_timestamp - lookback_steps, last_timestamp)
    counts, market_shares, diff_shares = [], [], []
    # unique, diff_unique, diff_counts = [], [], []

    for timestamp in lookback_timestamps:
        df_timestamp = df_rec[df_rec["timestamp"] == timestamp]
        hist = topic_histogram(df_timestamp['latent_topic'].values, n_topics)
        counts.append(hist)
        market_shares.append(np.array([round((x / df_timestamp.shape[0]), 3) for x in hist]))
        # unique.append(df_timestamp['latent_topic'].nunique())

    # change
    for i in range(1, len(lookback_timestamps)):
        diff_shares.append(abs(market_shares[i] - market_shares[i - 1])/2) # divided by 2 as the change is symetric
        # diff_unique.append(abs(unique[i] - unique[i - 1]))
        # diff_counts.append(abs(counts[i] - counts[i - 1]))

    # for testing
    if verbose:
        print('Market shares:')
        for m in market_shares:
            print(f'\t{m}')
        print('Market share differences:')
        for d in diff_shares:
            print(f'\t{d}, Sum: {sum(d):.3}')

    # aggregation
    market_shares_average_change = round(np.average([sum(x) for x in diff_shares]), 3)
    # unique_heterogeneity = sum(diff_unique)/len(lookback_timestamps)
    # counts_heterogeneity = [sum(x)/len for i in diff_counts]

    market_shares_stability = 1 - market_shares_average_change
    assert 0.0 <= market_shares_stability <= 1.0, 'Stability measurement not in range'
    return market_shares_stability


def supplier_stability(df_rec):
    n_topics = topics_params["n_topics"]
    last_timestamp = bidding_simulation_params["num_steps"]

    majors_change = 0
    non_zeros_change = 0

    prev_major, prev_non_zero = _shares_in_numbers(df_rec, last_timestamp - lookback_steps,
                                                   return_indices=True)
    for time_step in range(last_timestamp - lookback_steps + 1, last_timestamp):
        new_major, new_non_zero = _shares_in_numbers(df_rec, time_step, return_indices=True)
        new_major_change = 0 if (new_major == prev_major or new_major==-1) else 1
        new_non_zero_change = len(
            set(prev_non_zero).symmetric_difference(set(new_non_zero))) / n_topics

        majors_change += new_major_change
        non_zeros_change += new_non_zero_change

        prev_major, prev_non_zero = new_major, new_non_zero

    majors_change /= (lookback_steps - 1)
    non_zeros_change /= (lookback_steps - 1)

    return 1 - majors_change, 1 - non_zeros_change


def user_stability(df_rec):
    last_timestamp = bidding_simulation_params["num_steps"]
    lookback_timestamps = range(last_timestamp - lookback_steps, last_timestamp)
    user_topics = defaultdict(lambda: set())
    for timestamp in lookback_timestamps:
        df_timestamp = df_rec[df_rec["timestamp"] == timestamp]
        df_timestamp = df_timestamp.reset_index()
        for index, row in df_timestamp.iterrows():
            user_topics[row['user_id']].add(row['latent_topic'])

    n_topic_change_users = sum([1 for v in user_topics.values() if len(v) > 1])

    return n_topic_change_users/len(user_topics)
