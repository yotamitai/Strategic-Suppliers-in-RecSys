import numpy as np

from StratSupp.utils import topic_histogram


def heterogeneity(df_rec, df_pay, last_timestamp, n_topics=10):
    """
    :param last_timestamp: (int) the last timestamp
    :return         value: (Float) between 0-1
    """
    df_last_timestamp = df_rec[df_rec["timestamp"] == last_timestamp]
    hist = topic_histogram(df_last_timestamp['latent_topic'].values, n_topics)
    market_shares = [round((x / df_last_timestamp.shape[0]), 3) for x in hist]
    non_zero_topics = df_last_timestamp['latent_topic'].nunique()

    # calculate heterogeneity
    market_shares_heterogeneity = 0 #TODO

    value = market_shares_heterogeneity
    assert 0.0 <= value <= 1.0, 'Heterogeneity measurement not in range'
    return value


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


def heterogeneity(df_rec, df_pay):
    pass