import numpy as np

RANDOM_STATE = 1234
topics_params = {
    'n_users': 100,
    'n_items': 300,
    'n_topics': 10,
    'n_initial_ratings': 2000,
    'random_state': RANDOM_STATE,
}

# surprise.SVD
svd_model_params = {
    'n_factors': 16,
    'random_state': RANDOM_STATE,
}

bid_recommendation_rng = np.random.default_rng(RANDOM_STATE)

initial_budget = 50
bidding_simulation_params = {
    'payment_per_step': 100,
    'num_steps': 1000,
}
num_steps = bidding_simulation_params['num_steps']
lookback_steps = int(0.02 * num_steps)

n_strategic_agents = 10 #topics_params['n_topics']

promotion_range = list(np.linspace(0, 5, 11))
affinity_range = [round(x, 1) for x in np.linspace(-2, 2, 11)]

significance_stability_bound = 0.99  # TODO define significance stability bound
significance_heterogeneity_bound = 0.15  # TODO define significance heterogeneity bound