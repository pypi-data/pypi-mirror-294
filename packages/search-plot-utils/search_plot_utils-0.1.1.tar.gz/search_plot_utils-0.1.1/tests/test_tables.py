import unittest
from search_plot_utils.tables import table_grid_search
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

class TestTableGridSearch(unittest.TestCase):

    def setUp(self):
        """Set up a small GridSearchCV to use in tests."""
        iris = load_iris()
        clf = RandomForestClassifier()
        param_grid = {'n_estimators': [10, 20], 'max_depth': [2, 3]}
        grid_search = GridSearchCV(clf, param_grid)
        self.clf = grid_search.fit(iris.data, iris.target)

    def test_table_grid_search(self):
        """Test that the function runs without errors."""
        try:
            table_grid_search(self.clf, save=False)
        except Exception as e:
            self.fail(f"table_grid_search raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
