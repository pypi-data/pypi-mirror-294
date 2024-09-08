
# search_plot_utils

**`search_plot_utils`** is a Python library designed to simplify the visualization and analysis of search results from various hyperparameter optimization methods, including `GridSearchCV`, `RandomizedSearchCV`, and more. This library provides flexible and easy-to-use functions to create insightful plots and tables, enabling better interpretation and comparison of model performance across different hyperparameter combinations.

## Key Features
- **Flexible Plotting**: Visualize search results for a wide range of optimization methods.
- **Customizable Outputs**: Save plots as images or display them directly in Jupyter notebooks.
- **Tabular Insights**: Generate tables from search results with customizable columns and filters.
- **Broad Search Support**: Compatible with `GridSearchCV`, `RandomizedSearchCV`, and other search techniques.

## Installation

You can install `search_plot_utils` via pip (after setting up your project on PyPI) or by cloning the repository and installing manually:

\`\`\`bash
pip install search_plot_utils
\`\`\`

Or to install manually:

\`\`\`bash
git clone https://github.com/yourusername/search_plot_utils.git
cd search_plot_utils
pip install .
\`\`\`

## Usage

### 1. Plotting Search Results

You can use `plot_search_results` to create plots from your search results. This function is flexible and works with `GridSearchCV`, `RandomizedSearchCV`, and similar search objects.

\`\`\`python
from search_plot_utils import plot_search_results
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# Example usage with GridSearchCV
iris = load_iris()
clf = RandomForestClassifier()
param_grid = {'n_estimators': [10, 50], 'max_depth': [2, 4]}
grid_search = GridSearchCV(clf, param_grid)
grid_search.fit(iris.data, iris.target)

# Plot the search results
plot_search_results(grid_search.cv_results_)
\`\`\`

### 2. Creating Tables from Search Results

`table_search_results` helps you create and display tables from search results, making it easy to inspect and compare different hyperparameter settings.

\`\`\`python
from search_plot_utils import table_search_results

# Display the search results in a table
table_search_results(grid_search.cv_results_)
\`\`\`

## Contributing

Contributions are welcome! If you have suggestions or find a bug, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
