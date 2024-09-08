
from setuptools import setup, find_packages

setup(
    name='search_plot_utils',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'pandas',
        'scikit-learn',
    ],
    author='Diogo Hajjar',
    author_email='diogohajjar@gmail.com',
    description='Simplifies the visualization and analysis of search results from hyperparameter optimization.',
    long_description=""" 
    # search_plot_utils
    
    `search_plot_utils` is a Python library designed to simplify the visualization and analysis of search results from various hyperparameter optimization methods, including `GridSearchCV`, `RandomizedSearchCV`, and more. This library provides flexible and easy-to-use functions to create insightful plots and tables, enabling better interpretation and comparison of model performance across different hyperparameter combinations.
    
    ## Key Features:
    
    - **Flexible Plotting**: Visualize search results for a wide range of optimization methods.
    - **Customizable Outputs**: Save plots as images or display them directly in Jupyter notebooks.
    - **Tabular Insights**: Generate tables from search results with customizable columns and filters.
    - **Broad Search Support**: Compatible with `GridSearchCV`, `RandomizedSearchCV`, and other search techniques.
    
    ## Installation:
    
    You can install `search_plot_utils` via pip:
    
    ```bash
    pip install search_plot_utils
    ```
    
    Or install manually:
    
    ```bash
    git clone https://github.com/yourusername/search_plot_utils.git
    cd search_plot_utils
    pip install .
    ```
    
    ## Example Usage:
    
    ```python
    from grid_search_utils.plotting import plot_grid_search, plot_grid_search_non_interactive
    from grid_search_utils.tables import table_grid_search
    
    from sklearn.model_selection import GridSearchCV
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier
    
    # Load dataset and set up model
    iris = load_iris()
    clf = RandomForestClassifier()
    param_grid = {'n_estimators': [10, 50], 'max_depth': [2, 4]}
    
    # Execute GridSearchCV
    grid_search = GridSearchCV(clf, param_grid)
    grid_search.fit(iris.data, iris.target)
    
    # Generate search results plot
    plot_search_results(grid_search.cv_results_)
    
    # Generate search results plot (Non Interactive version)
    plot_grid_search_non_interactive(grid_search.cv_results_)
    
    # Generate search results table
    table_search_results(grid_search.cv_results_)
    ```
    
    
    ## License:
    
    This project is licensed under the MIT License.
    """,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/search_plot_utils',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
