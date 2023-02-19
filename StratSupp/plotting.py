def plot_df(df):
    df.pivot('timestamp', 'supplier', 'remaining_budget').plot.line(
        title='Remaining budget over time for different suppliers',
        xlabel='Time ($t$)',
        ylabel='Remaining budget',
        figsize=(12, 6),
        )
