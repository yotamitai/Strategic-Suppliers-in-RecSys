import numpy as np
import surprise


def trainset_from_df(df):
    """
    Convert DataFrame to Surprise training set.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with columns [user_id, item_id, rating]

    Returns
    -------
    trainset : surprise.Trainset
    """
    dataset = surprise.Dataset.load_from_df(
        df=df[['user_id', 'item_id', 'rating']],
        reader=surprise.Reader(rating_scale=(1, 5)),
    )
    return dataset.build_full_trainset()


def topic_histogram(lst, n_values):
    int_lst = [int(x) for x in lst]
    h = [0] * n_values
    for item in int_lst:
        h[item] += 1
    return np.array(h)
