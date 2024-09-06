# src/visualization/visualize.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
from sklearn.metrics import roc_curve, auc

def auc_roc_curve(y_true, y_pred_proba):
    """
    Plot the ROC curve and calculate AUC for a set of true labels and predicted probabilities.

    Args:
        y_true (np.ndarray or pd.Series): True binary labels.
        y_pred_proba (np.ndarray or pd.Series): Predicted probabilities for the positive class.

    Returns:
        None: Displays the ROC curve plot.
    """
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()

def plot_histograms(df, columns, ncols=2):
    """
    Plot histograms for specified columns of a DataFrame.
    """
    n = len(columns)
    nrows = n // ncols + (n % ncols > 0)

    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12, 4 * nrows))
    ax = ax.flat

    for i, col in enumerate(columns):
        sns.histplot(df[col], ax=ax[i], kde=True)
        ax[i].set_title(f'Histogram of {col}', fontsize=14)

    for i in range(n, len(ax)):
        ax[i].set_visible(False)

    plt.tight_layout()
    plt.show()

def plot_boxplots(df):
    """
    Plot boxplots for all numeric columns in the DataFrame.
    """
    numeric_data = df.select_dtypes(include=['float64', 'int64'])
    plt.figure(figsize=(15, 10))
    sns.boxplot(data=numeric_data, orient='h')
    plt.title('Boxplots for All Numeric Columns')
    plt.show()

def distribution_analysis(df):
    """
    Plot distribution analysis for 'ast' and 'per' columns.
    """
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    sns.histplot(df['ast'], kde=True, color='orange')
    plt.title('Distribution Analysis of ast')
    plt.xlabel('Assists')
    plt.ylabel('Frequency')

    plt.subplot(1, 2, 2)
    sns.histplot(df['AST_per'], kde=True, color='blue')
    plt.title('Distribution Analysis of AST_per')
    plt.xlabel('Assist Percentage')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()

def free_throw_analysis(df):
    """
    Plot distribution analysis for 'FTM', 'FTA', and 'FT_per' columns.
    """
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 3, 1)
    sns.histplot(df['FTM'], kde=True, color='green')
    plt.title('Distribution Analysis of FTM')
    plt.xlabel('Free Throws Made')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 2)
    sns.histplot(df['FTA'], kde=True, color='purple')
    plt.title('Distribution Analysis of FTA')
    plt.xlabel('Free Throw Attempts')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 3)
    sns.histplot(df['FT_per'], kde=True, color='red')
    plt.title('Distribution Analysis of FT_per')
    plt.xlabel('Free Throw Percentage')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()

def top_teams_no_drafted(df):
    """
    Plot pie chart for top 10 teams with no drafted players.
    """
    top_10 = df['team'].value_counts().nlargest(10).index
    top_10 = df[df['team'].isin(top_10)]
    no_drafted = top_10[top_10['drafted'] == 0]
    counts = no_drafted['team'].value_counts().reset_index()
    counts.columns = ['team', 'count']

    fig = px.pie(counts, names='team', values='count', color='team',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 title='Top 10 Teams with No Drafted Players')
    fig.update_layout(xaxis_title='Team', yaxis_title='Counts')
    fig.show()

def yearly_free_throw_analysis(df):
    """
    Plot yearly analysis for free throw percentages.
    """
    yearly_ftp = df.groupby('year')['FT_per'].sum().reset_index()
    yearly_ftp['year'] = pd.to_datetime(yearly_ftp['year'], format='%Y').dt.year

    plt.figure(figsize=(12, 6))
    fig = sns.relplot(data=yearly_ftp, x='year', y='FT_per', kind='line', height=5, aspect=2)
    fig.set(title='Free Throws Percentage Yearly Analysis', ylabel='Free Throws Percentage', xlabel="Year")

    sns.regplot(data=yearly_ftp, x='year', y='FT_per', scatter=False, ax=fig.ax, line_kws={'color': 'black', 'linestyle': '--'})

    fig.ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.grid(False)
    plt.show()

def yearly_block_percentage_analysis(df):
    """
    Plot yearly analysis for block percentages.
    """
    yearly_blk = df.groupby('year')['blk_per'].sum().reset_index()
    yearly_blk['year'] = pd.to_datetime(yearly_blk['year'], format='%Y').dt.year

    fig = px.bar(yearly_blk, x='year', y='blk_per', title='Block Percentage Yearly Analysis',
                 labels={'blk_per': 'Block Percentage', 'year': 'Year'}, color_discrete_sequence=['khaki'])
    fig.add_scatter(x=yearly_blk['year'], y=yearly_blk['blk_per'].rolling(window=2).mean(),
                    mode='lines', line=dict(color='red', dash='dash'), name='Trendline')
    fig.update_layout(xaxis_title='Year', yaxis_title='Block Percentage', xaxis=dict(tickmode='linear'), template='plotly_white')
    fig.show()

def yearly_games_played_analysis(df):
    """
    Plot yearly analysis for number of games played.
    """
    yearly_gp = df.groupby('year')['GP'].sum().reset_index()
    yearly_gp['year'] = pd.to_datetime(yearly_gp['year'], format='%Y').dt.year

    plt.figure(figsize=(12, 6))
    fig = sns.relplot(data=yearly_gp, x='year', y='GP', kind='line', height=5, aspect=2)
    fig.set(title='Number of Games Played Yearly Analysis', ylabel='Number of Games Played', xlabel="Year")

    sns.regplot(data=yearly_gp, x='year', y='GP', scatter=True, ax=fig.ax, line_kws={'color': 'purple', 'linestyle': '--'})

    fig.ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.show()

def conference_count_plot(df):
    """
    Plot count of different conferences.
    """
    fig = px.histogram(df, x='conf', color_discrete_sequence=['lightcoral'])
    fig.update_layout(title='Count Plot of Conference', xaxis_title='Conf', yaxis_title='Count', bargap=0.2)
    fig.show()

def top_teams_steals(df):
    """
    Plot top 20 teams by total steals.
    """
    steals_team = df.groupby('team')['stl'].sum().reset_index()
    top_20 = steals_team.nlargest(20, 'stl')
    fig = px.bar(top_20, x='team', y='stl', color='team', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(title='Top 20 Teams by Total Steals', xaxis_title='Team', yaxis_title='Total Steals')
    fig.show()
