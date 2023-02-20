import matplotlib.pyplot as plt
def plot_budget(df):
    df.pivot('timestamp', 'supplier', 'remaining_budget').plot.line(
        title='Supplier remaining budget over time ',
        xlabel='Time ($t$)',
        ylabel='Remaining budget',
        figsize=(12, 6),
        )
    plt.show()

def plot_bid(df):
    df.pivot('timestamp', 'supplier', 'bid').plot.line(
        title='Supplier bidding over time',
        xlabel='Time ($t$)',
        ylabel='Remaining budget',
        figsize=(12, 6),
        )
    plt.show()
