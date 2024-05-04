from sklearn.ensemble import RandomForestRegressor
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib


def add_grid(axes: matplotlib.axes._axes.Axes) -> None:
    """Function adding grid with necessary format to given axes
    :param axes: object of matplotlib axes
    :returns: None
    """
    axes.grid(color='grey', linestyle='-', linewidth=0.5, which='major', axis='both')
    axes.grid(color='lightblue', linestyle='-', linewidth=0.5, which='minor', axis='both')
    axes.minorticks_on()
    return 1


def random_forest_model_generation(best_rf_params, X_train, y_train, X_test, y_test):
    """Function to create model, train it, print its score and return model"""
    model = RandomForestRegressor(**best_rf_params)
    model.fit(X_train, y_train)
    train_score = model.score(X_train, y_train)
    print(f'The train score is: {train_score}')
    test_score = model.score(X_test, y_test)
    print(f'The test score is: {test_score}')
    return model


def graphical_comparison_of_model(**kwargs):
    """Graphical representation of results of model accuracy
    as a **kwargs to function need to be given dictionary of following structure:
    test_input = {
    'model': model,
    'model_name': 'Porosity-ResistivityDeep',
    'param_name': 'Porosity',
    'param_units': 'v/v',
    'limits': (-0.05, 0.4),
    'X_train': X_train,
    'X_test': X_test,
    'y_train': y_train,
    'y_test': y_test,}
    """
    def adjust_axes(ax_to_modify, grids=True):
        """Adjusting axes for comparison porosity plot"""
        ax_to_modify.set_xlim(kwargs['limits'][0], kwargs['limits'][1])
        ax_to_modify.set_ylim(kwargs['limits'][0], kwargs['limits'][1])
        ax_to_modify.plot([kwargs['limits'][0], kwargs['limits'][1]], [kwargs['limits'][0], kwargs['limits'][1]],
                          label='mean line', color='red')
        ax_to_modify.legend()
        if grids:
            add_grid(ax_to_modify)
        else:
            pass

    predictions_train = kwargs['model'].predict(kwargs['X_train'])
    predictions_test = kwargs['model'].predict(kwargs['X_test'])
    fig, ax = plt.subplots(2, 2, figsize=(15, 10))
    ax[0, 0].scatter(kwargs['y_train'], predictions_train,
                     label=f'train selection n={len(kwargs["y_train"])}', s=10, c='green', alpha=0.5)
    ax[0, 1].scatter(kwargs['y_test'], predictions_test,
                     label=f'test selection n={len(kwargs["y_test"])}', s=10, c='blue', alpha=0.5)
    ax[0, 0].set_title(f'Comparison of real and predicted {kwargs["param_name"]} (train)')
    ax[0, 0].set_xlabel(f'Real  {kwargs["param_name"]}, {kwargs["param_units"]}')
    ax[0, 0].set_ylabel(f'Predicted {kwargs["param_name"]}, {kwargs["param_units"]}')
    ax[0, 1].set_title(f'Comparison of real and predicted {kwargs["param_name"]} (test)')
    ax[0, 1].set_xlabel(f'Real {kwargs["param_name"]}, {kwargs["param_units"]}')
    ax[0, 1].set_ylabel(f'Predicted {kwargs["param_name"]}, {kwargs["param_units"]}')
    [adjust_axes(ax[0, i]) for i in range(2)]
    [adjust_axes(ax[1, i], grids=False) for i in range(2)]
    ax[1, 0].hist2d(kwargs['y_train'], predictions_train, label='train selection', bins=60)
    ax[1, 1].hist2d(kwargs['y_test'], predictions_test, label='test selection', bins=60)


def show_grid_search_score(grid):
    """Show graphically score of grid search and time for calculations"""
    def convert_params(row):
        return str(row['params'])

    cv_results = pd.DataFrame.from_dict(grid.cv_results_)
    cv_results['params'] = cv_results.apply(convert_params, axis=1)

    fig, ax = plt.subplots(2, 1, figsize=(10, 10))

    sns.barplot(data=cv_results, x='mean_test_score', y='params', ax=ax[0]).set_title('mean_test_score')
    ax[0].set_xlim(0, 1)
    ax[0].bar_label(ax[0].containers[0], cv_results['mean_test_score'].values.round(3), fontsize=12)
    sns.barplot(data=cv_results, x='mean_score_time', y='params', ax=ax[1]).set_title('mean_score_time')
    ax[1].bar_label(ax[1].containers[0], cv_results['mean_score_time'].values.round(2), fontsize=12)


def prepare_df_feature_importance(model):
    return pd.DataFrame([model.feature_names_in_, model.feature_importances_], index=['feature name', 'importance']).T


if __name__ == '__main__':
    fig_, ax_ = plt.subplots(1, 1, figsize=(6, 6))
    ax_.scatter([1, 2], [1, 2])
    add_grid(ax_)
    print(type(ax_))
    plt.show()
