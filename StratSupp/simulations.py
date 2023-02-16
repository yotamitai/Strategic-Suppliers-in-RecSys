import numpy as np
import pandas as pd
import scipy

from StratSupp.environments import TopicsStatic
from StratSupp.utils import trainset_from_df
from tqdm.auto import tqdm


def simulate_recommendations_with_bidding(
        env,
        cf_model,
        suppliers,
        num_steps,
        payment_per_step,
        promotion_factor,
):
    """
    Simulate recommendations with bidding.

    Parameters
    ----------
    env : TopicsStatic

    cf_model : surprise.AlgoBase

    num_steps : int
        Length of simulation.

    payment_per_step : float
        Total payment to suppliers per step

    promotion_factor : float
        Promotion factor B

    Returns
    -------
    recommendations_df : pandas.DataFrame
        pandas DataFrame with all recommendations. Each row represents a
        recommendation. Each recommendation is associated with a timestamp,
        user id, item id, predicted rating, actual rating, and latent topic.

    payments_df : pandas.DataFrame
        pandas DataFrame with all payment information. Each row represents
        the behavior of a supplier (and its consequences) for a given time
        step. Each row is associated with a timestamp, supplier id,
        supplier bid, attained position, boost factor, revenue, and
        remaining_budget.
    """
    assert isinstance(env, TopicsStatic), (
        'env must be an instance of TopicsStatic or one of its subclasses'
    )
    K = env.n_topics
    assert K == len(suppliers), (
        'Length of supplier list must match number of topics'
    )
    recommendation_results = []
    payment_results = []

    # Fit initial CF model
    recommendation_results = [env.get_initial_ratings()]
    cf_model.fit(trainset_from_df(recommendation_results[0]))

    # Simulate dynamics
    for t in tqdm(range(num_steps)):
        online_users = env.get_online_users()
        recommendations = {}
        # Calculate promotion factors
        bids = suppliers.calculate_bids(context={
            'online_users': online_users,
            'previous_ratings': (
                pd.concat(recommendation_results)
                .pipe(lambda df: df.drop('latent_topic', axis=1) if t > 0 else df)
            ),
            'previous_bids': pd.DataFrame(payment_results),
        })
        for agent, bid in zip(suppliers, bids):
            assert bid >= 0, 'Bids must be positive'
            agent.transfer_funds(-bid)
        pos = K - (scipy.stats.rankdata(bids, method='ordinal') - 1)
        beta = promotion_factor * 2 * ((K - pos) / (K - 1) - 0.5)
        payment = np.zeros(K)
        # Recommend
        for user_id in online_users:
            # Predict ratings
            predicted_ratings = {
                item_id: cf_model.predict(user_id, item_id).est
                for item_id in env.get_unseen_items(user_id)
            }
            # Add promotion bias
            predicted_ratings_with_bias = {
                item_id: predicted_rating + beta[env._item_topics[item_id]]
                for item_id, predicted_rating
                in predicted_ratings.items()
            }
            selected_item = max(
                predicted_ratings_with_bias.items(),
                key=lambda t: t[1],
            )[0]
            recommendations[(user_id, selected_item)] = predicted_ratings[selected_item]
            payment[env._item_topics[selected_item]] += payment_per_step / len(online_users)

        # Recommend
        ratings = env.recommend(list(recommendations))
        recommendation_results.append(
            ratings
            .assign(
                predicted_rating=lambda df: df.apply(
                    lambda row: recommendations[(row['user_id'], row['item_id'])],
                    axis=1,
                ),
                latent_topic=lambda df: df['item_id'].map(
                    lambda item_id: env._item_topics[item_id]
                ),
            )
        )
        # Retrain
        cf_model.fit(trainset_from_df(pd.concat(recommendation_results)))
        # Pay and record remaining budgets
        for topic_k, agent in enumerate(suppliers):
            agent.transfer_funds(payment[topic_k])
            payment_results.append({
                'timestamp': t + 1,
                'supplier': topic_k,  # supplier id
                'bid': bids[topic_k],  # supplier bid
                'position': pos[topic_k],  # pos_t(k)
                'boost': beta[topic_k],  # beta_t^k
                'revenue': payment[topic_k],  # payment made to supplier k
                'remaining_budget': agent.remaining_budget(),  # remaining budget
            })

    return (
        pd.concat(recommendation_results),  # recommendations_df
        pd.DataFrame(payment_results),  # payments_df
    )
