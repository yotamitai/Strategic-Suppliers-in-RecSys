import numpy as np
import surprise

from StratSupp.agents import StrategicBiddingAgent, RandomFractionBiddingAgent
from StratSupp.environments import TopicsDynamic
from StratSupp.measurements import stability, heterogeneity
from StratSupp.plotting import plot_supplier_over_time
from StratSupp.simulations import simulate_recommendations_with_bidding
from StratSupp.suppliers import SuppliersGroup
from CONFIG import *


def run(promotion, affinity):
    # environment
    env = TopicsDynamic(topic_change=affinity, **topics_params)
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
        promotion_factor=promotion,
        num_steps=bidding_simulation_params["num_steps"]
        # global simulation parameters (lengths, payment per step, promotion)
        # **bidding_simulation_params
    )

    return recommendation_results_df, payments_df


if __name__ == '__main__':
    promotion_factor = 0.5
    affinity_change = 0.0

    recommendation_results_df, payments_df = run(promotion_factor, affinity_change)

    # measurements
    stability_value = stability(recommendation_results_df, verbose=True)
    heterogeneity_value = heterogeneity(recommendation_results_df)

    # printing
    print(f'Stability score: {stability_value}\nHeterogeneity score: {heterogeneity_value}')
    print(f'Measurements from the {lookback_steps} last timestamps')

    # plot
    plot_supplier_over_time(payments_df, 'remaining_budget')
    plot_supplier_over_time(payments_df, 'bid')
    plot_supplier_over_time(payments_df, 'hostility')
