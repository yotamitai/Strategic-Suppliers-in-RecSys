import numpy as np
import surprise

from StratSupp.agents import StrategicBiddingAgent, RandomFractionBiddingAgent
from StratSupp.environments import TopicsDynamic
from StratSupp.measurements import stability, heterogeneity
from StratSupp.plotting import plot_df
from StratSupp.simulations import simulate_recommendations_with_bidding
from StratSupp.suppliers import SuppliersGroup

RANDOM_STATE = 1234

# TopicsDyamic
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

initial_budget = 100
bidding_simulation_params = {
    'payment_per_step': 100,
    'promotion_factor': 1.0,
    'num_steps': 100,
}
num_steps = bidding_simulation_params['num_steps']
lookback_steps = int(0.02 * num_steps)

n_strategic_agents = 10 #topics_params['n_topics']

if __name__ == '__main__':
    # environment
    env = TopicsDynamic(topic_change=0.0, **topics_params)
    # prediction model
    cf_model = surprise.SVD(**svd_model_params)
    # suppliers
    strategic_agents = [StrategicBiddingAgent(initial_budget=initial_budget,
                                              random_state=bid_recommendation_rng, topic_k=k)
                        for k in range(n_strategic_agents)]
    random_agents = [RandomFractionBiddingAgent(initial_budget=initial_budget,
                                                random_state=bid_recommendation_rng, topic_k=k)
                     for k in range(n_strategic_agents, topics_params['n_topics'])]
    suppliers = SuppliersGroup(agents=(strategic_agents + random_agents))
    # simulate
    recommendation_results_df, payments_df = simulate_recommendations_with_bidding(  # environment
        env=env, cf_model=cf_model, suppliers=suppliers,
        payment_per_step=bidding_simulation_params["payment_per_step"],
        promotion_factor=bidding_simulation_params["promotion_factor"],
        num_steps=bidding_simulation_params["num_steps"]
        # global simulation parameters (lengths, payment per step, promotion)
        # **bidding_simulation_params
    )

    # plot
    plot_df(payments_df)

    # measurements
    timestamp = range(num_steps-lookback_steps, num_steps)
    stability_value = stability(recommendation_results_df, payments_df, timestamp)
    heterogeneity_value = heterogeneity(recommendation_results_df, payments_df, timestamp)
    print(stability_value, heterogeneity_value)
