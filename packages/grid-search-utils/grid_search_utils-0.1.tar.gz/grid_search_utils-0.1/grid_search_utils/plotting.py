import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from scipy import stats
import plotly.io as pio

def plot_grid_search(clf, save=False, filename=None):
    """Plot grid search results using Plotly."""
    cv_results = pd.DataFrame(clf.cv_results_).sort_values(by=['rank_test_score', 'mean_fit_time'])
    parameters = cv_results['params'][0].keys()

    rows = -(-len(parameters) // 2)
    columns = min(len(parameters), 2)
    fig = make_subplots(rows=rows, cols=columns)

    row, column = 1, 1
    for parameter in parameters:
        show_legend = row == 1 and column == 1

        mean_test_score = cv_results[cv_results['rank_test_score'] != 1]
        fig.add_trace(go.Scatter(
            name='Mean test score',
            x=mean_test_score['param_' + parameter],
            y=mean_test_score['mean_test_score'],
            mode='markers',
            marker=dict(size=mean_test_score['mean_fit_time'],
                        color='SteelBlue',
                        sizeref=2. * cv_results['mean_fit_time'].max() / (40. ** 2),
                        sizemin=4,
                        sizemode='area'),
            text=mean_test_score['params'].apply(lambda x: pprint.pformat(x, width=-1).replace('{', '').replace('}', '').replace('\n', '<br />')),
            showlegend=show_legend),
            row=row, col=column)

        rank_1 = cv_results[cv_results['rank_test_score'] == 1]
        fig.add_trace(go.Scatter(
            name='Best estimators',
            x=rank_1['param_' + parameter],
            y=rank_1['mean_test_score'],
            mode='markers',
            marker=dict(size=rank_1['mean_fit_time'],
                        color='Crimson',
                        sizeref=2. * cv_results['mean_fit_time'].max() / (40. ** 2),
                        sizemin=4,
                        sizemode='area'),
            text=rank_1['params'].apply(str),
            showlegend=show_legend),
            row=row, col=column)

        fig.update_xaxes(title_text=parameter, row=row, col=column)
        fig.update_yaxes(title_text='Score', row=row, col=column)

        if pd.to_numeric(cv_results['param_' + parameter], errors='coerce').notnull().all():
            x_values = cv_results['param_' + parameter].sort_values().unique().tolist()
            r = stats.linregress(x_values, range(0, len(x_values))).rvalue
            if r < 0.86:
                fig.update_xaxes(type='log', row=row, col=column)

        column += 1
        if column > columns:
            column = 1
            row += 1

    fig.update_layout(legend=dict(traceorder='reversed'),
                      width=columns * 360 + 100,
                      height=rows * 360,
                      title='Best score: {:.6f} with {}'.format(cv_results['mean_test_score'].iloc[0],
                                                                str(cv_results['params'].iloc[0]).replace('{',
                                                                                                          '').replace(
                                                                    '}', '')),
                      hovermode='closest',
                      template='none')

    if save and filename:
        pio.write_image(fig, filename)

    pio.show(fig, renderer='notebook')

def plot_grid_search_non_interactive(clf, save=True, file_name='grid_search_plot.png'):
    """Plot grid search results using Matplotlib."""
    cv_results = pd.DataFrame(clf.cv_results_).sort_values(by=['rank_test_score', 'mean_fit_time'])
    parameters = cv_results['params'][0].keys()

    rows = -(-len(parameters) // 2)
    columns = min(len(parameters), 2)
    fig, axes = plt.subplots(rows, columns, figsize=(columns * 6, rows * 6))
    axes = np.array([[axes]]) if rows == 1 and columns == 1 else np.reshape(axes, (rows, columns))

    row, column = 0, 0
    for parameter in parameters:
        ax = axes[row, column]

        mean_test_score = cv_results[cv_results['rank_test_score'] != 1]
        sizes = mean_test_score['mean_fit_time'] * 8000
        ax.scatter(mean_test_score['param_' + parameter], mean_test_score['mean_test_score'],
                   s=sizes, color='steelblue', label='Mean test score', alpha=0.6)

        rank_1 = cv_results[cv_results['rank_test_score'] == 1]
        sizes = rank_1['mean_fit_time'] * 8000
        ax.scatter(rank_1['param_' + parameter], rank_1['mean_test_score'],
                   s=sizes, color='crimson', label='Best estimators', alpha=0.6)

        ax.set_xlabel(parameter)
        ax.set_ylabel('Score')
        ax.set_title(f'Parameter: {parameter}')
        ax.legend()

        if pd.to_numeric(cv_results['param_' + parameter], errors='coerce').notnull().all():
            x_values = cv_results['param_' + parameter].sort_values().unique().tolist()
            r = stats.linregress(x_values, range(0, len(x_values))).rvalue
            if r < 0.86:
                ax.set_xscale('log')

        column += 1
        if column >= columns:
            column = 0
            row += 1

    fig.suptitle('Grid Search Results')
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    if save:
        plt.savefig(file_name)

    plt.show()
