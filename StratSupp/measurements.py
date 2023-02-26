import numpy as np

from StratSupp.utils import topic_histogram
from CONFIG import *


def _shares_in_numbers(df_rec, time_step, return_indices=False):
    n_topics = topics_params["n_topics"]

    df_timestamp = df_rec[df_rec["timestamp"] == time_step]
    hist = topic_histogram(df_timestamp['latent_topic'].values, n_topics)
    market_shares = [round((x / df_timestamp.shape[0]), 3) for x in hist]

    major = -1
    for x in market_shares:
        if x > 0.5:
            major = x

    non_zero_topics = df_timestamp['latent_topic'].nunique().tolist()

    if return_indices:
        return major, non_zero_topics

    major_binary = min(1, major+1)

    if len(non_zero_topics) == 1:
        monopoly_binary = 0
    else:
        monopoly_binary = 1

    monopoly_continuous = len(non_zero_topics) / n_topics

    return major_binary, monopoly_binary, monopoly_continuous


def heterogeneity(df_rec, df_pay, last_timestamp, n_topics=10):
    """
    :param last_timestamp: (int) the last timestamp
    :return         value: (Float) between 0-1
    """

    last_timestamp = bidding_simulation_params["num_steps"]
    return _shares_in_numbers(df_rec, last_timestamp, return_indices=False)


def stability(df_rec, df_pay, lookback_timestamps, n_topics=10, verbose=False):
    """
    :param lookback_timestamps: (List) timestamps for which to measure stability
    :return              value: (Float) between 0-1
    """
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
        diff_shares.append(abs(market_shares[i] - market_shares[i - 1]))
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
    market_shares_stability = round(np.average([sum(x) for x in diff_shares]),3)
    # unique_heterogeneity = sum(diff_unique)/len(lookback_timestamps)
    # counts_heterogeneity = [sum(x)/len for i in diff_counts]

    value = market_shares_stability
    assert 0.0 <= value <= 1.0, 'Stability measurement not in range'
    return value


def stability_from_suppliers_view(df_rec):
    n_topics = topics_params["n_topics"]
    last_timestamp = bidding_simulation_params["num_steps"]

    majors_change = 0
    non_zeros_change = 0

    prev_major, prev_non_zero = _shares_in_numbers(df_rec, last_timestamp-lookback_steps, return_indices=True)
    for time_step in range(last_timestamp-lookback_steps+1, lookback_steps):
        new_major, new_non_zero = _shares_in_numbers(df_rec, time_step, return_indices=True)
        new_major_change = int(not new_major == prev_major)
        new_non_zero_change = len(set(prev_non_zero).symmetric_difference(set(new_non_zero))) / n_topics

        majors_change += new_major_change
        non_zeros_change += new_non_zero_change

        prev_major, prev_non_zero = new_major, new_non_zero

    majors_change /= (lookback_steps-1)
    non_zeros_change /= (lookback_steps-1)

    return 1-majors_change, 1-non_zeros_change


