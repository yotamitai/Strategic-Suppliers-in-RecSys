class SuppliersGroup:
    def __init__(self, agents):
        """
        Initialize the suppliers group.

        Parameters
        ----------
        agents : list of BiddingAgent
        """
        self.agents = agents

    def calculate_bids(self, context):
        return [agent.calculate_bid(context) for agent in self.agents]

    def transfer_funds(self, payment_vector):
        for agent, payment in zip(self.agents, payment_vector):
            agent.transfer_funds(payment)

    def __len__(self):
        return len(self.agents)

    def __iter__(self):
        return iter(self.agents)

    def __getitem__(self, i):
        return self.agents[i]
