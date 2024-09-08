import pandas as pd
from IPython.display import display

def table_grid_search(clf, all_columns=False, all_ranks=False, save=True, filename='grid_search_results.csv'):
    """Show tables with the grid search results."""
    cv_results = pd.DataFrame(clf.cv_results_).sort_values(by=['rank_test_score', 'mean_fit_time'])

    columns = cv_results.columns.tolist()
    columns = columns[-1:] + columns[-3:-1] + columns[:-3]
    cv_results = cv_results[columns]

    if save:
        cv_results.to_csv(filename, index=True, index_label='Id')

    if not all_columns:
        cv_results.drop('params', axis='columns', inplace=True)
        cv_results.drop(list(cv_results.filter(regex='^std_.*')), axis='columns', inplace=True)
        cv_results.drop(list(cv_results.filter(regex='^split.*')), axis='columns', inplace=True)

    if not all_ranks:
        cv_results = cv_results[cv_results['rank_test_score'] == 1]
        cv_results.drop('rank_test_score', axis='columns', inplace=True)
        cv_results = cv_results.style.hide(axis='index')

    display(cv_results)
