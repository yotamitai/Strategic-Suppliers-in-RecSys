import numpy as np


class BiddingAgent:
    """
    Generic class for simulating a bidding agent (supplier)
    """

    def __init__(self, initial_budget, topic_k, random_state=None):
        """
        Initialize the bidding agent.

        Parameters
        ----------
        initial_budget : float
            Initial budget (non-negative)

        topic_k : int
            Topic id corresponding to the agent (0,...,K-1)

        random_state : Seed. Valid input to `np.random.default_rng`.
        """
        assert initial_budget >= 0, 'Initial budget must be nonnegative.'
        self.initial_budget = initial_budget
        self._remaining_budget = initial_budget
        self.topic_k = topic_k
        self.rng = np.random.default_rng(random_state)
        self.payment_history = []

    def calculate_bid(self, context=None):
        """
        Return the raw bid, to be implemented by subclasses.
        The `place_bid` function validates the value returned.

        Parameters
        ----------
        context : any
            a context parameter for informed decision-making.

        Returns
        -------
        bid : float
            bid for next promotion.
        """
        raise NotImplementedError

    def remaining_budget(self):
        """
        Get the remaining budget of the bidding agent.

        Returns
        -------
        remaining_budget : float
        """
        return self._remaining_budget

    def transfer_funds(self, m):
        """
        Transfer/receive funds resulting from recommendations.
        Negative value of `m` represents tranfer of funds from the agent
        to the system, and a positive value of `m` represents a payment
        from the system to the agent.

        Parameters
        ----------
        m : float
            Amount of pay.
        """
        assert self._remaining_budget + m >= 0, (
            'Each payment must preserve a non-negative budget'
        )
        self._remaining_budget += m
        self.payment_history.append(m)


class RandomFractionBiddingAgent(BiddingAgent):
    """
    Agent simulating a random bidding policy.
    At each step, suppliers of this type bid a random amount of money
    between 0 and half the money they currently have.
    """

    def calculate_bid(self, context=None):
        return self.rng.uniform(low=0.0, high=0.5) * self.remaining_budget()

    def update_bidding_range(self, private_incomes, total_incomes):
        return None

class StrategicBiddingAgent(BiddingAgent):
    def __init__(self, initial_budget, topic_k, random_state=None):
        super().__init__(initial_budget, topic_k, random_state)
        self.upper_limit = 0.5
        self.lower_limit = 0.25

    def update_bidding_range(self, private_incomes, total_incomes):
        # update upper_limit
        hostility = (total_incomes - private_incomes) / private_incomes
        self.upper_limit = 0.25 + 0.75 * hostility

        # update lower_limit
        if self._remaining_budget < self.initial_budget:
            # low success
            self.lower_limit = 0.25 * (1 - hostility)
        else:
            # high success
            self.lower_limit = 0.25

    def calculate_bid(self, context=None):
        return self.rng.uniform(low=self.lower_limit,
                                high=self.upper_limit) * self.remaining_budget()
