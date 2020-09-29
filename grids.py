"""Classifier Parameters"""

decision_tree_param = dict(pca__n_components=[20],
                           decisiontree__criterion=['gini', 'entropy'],
                           decisiontree__max_depth=[4, 6, 8, 12])

gradient_boosting_param = dict(pca__n_components=[20],
                               gradientbooster__criterion=['friedman_mse', 'mse', 'mae'],
                               gradientbooster__max_depth=[4, 6, 8, 12])

random_forest_param = dict(pca__n_components=[20],
                           randomforest__criterion=['gini', 'entropy'],
                           randomforest__max_depth=[4, 6, 8, 12])

