import unittest
from search_plot_utils.plotting import plot_grid_search_non_interactive
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

class TestPlotGridSearchNonInteractive(unittest.TestCase):

    def setUp(self):
        """Set up a small GridSearchCV to use in tests."""
        iris = load_iris()
        clf = RandomForestClassifier()
        param_grid = {'n_estimators': [10, 20], 'max_depth': [2, 3]}
        grid_search = GridSearchCV(clf, param_grid)
        self.clf = grid_search.fit(iris.data, iris.target)

    def test_plot_grid_search_non_interactive(self):
        """Test that the function runs without errors."""
        try:
            plot_grid_search_non_interactive(self.clf, save=False)
        except Exception as e:
            self.fail(f"plot_grid_search_non_interactive raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
