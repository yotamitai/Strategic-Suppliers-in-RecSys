def stability(df_rec, df_pay, lookback_timestamp):
    """
    :param lookback_timestamp: (List) timestamps for which to measure stability
    :return             value: (Float) between 0-1
    """
    value = 0

    for timestep in lookback_timestamp:
        df_timestamp = df_rec[df_rec["timestamp"] == timestep]

    assert 0.0 <= value <= 1.0, 'Stability measurement not in range'
    return value


def heterogeneity(df_rec, df_pay, lookback_timestamp):
    """
    :param lookback_timestamp: (List) timestamps for which to measure heterogeneity
    :return             value: (Float) between 0-1
    """
    value = 0
    unique = []
    counts = []

    for timestep in lookback_timestamp:
        df_timestamp = df_rec[df_rec["timestamp"] == timestep]
        unique.append(df_timestamp['latent_topic'].nunique())
        counts.append(df_timestamp['latent_topic'].value_counts())

    # aggregation


    diff_n_unique = sum([abs(unique[i]-unique[i-1]) for i in range(1, len(unique))])/len(unique)


    assert 0.0 <= value <= 1.0, 'Heterogeneity measurement not in range'
    return value
