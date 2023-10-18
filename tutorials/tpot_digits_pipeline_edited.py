import pandas as pd
from sklearn.feature_selection import SelectFwe, f_classif
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
import joblib

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_parquet('digits.parquet')
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: 0.9703263114415531
exported_pipeline = make_pipeline(
    SelectFwe(score_func=f_classif, alpha=0.045),
    MLPClassifier(alpha=0.1, learning_rate_init=0.001)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
print(exported_pipeline.score(testing_features, testing_target))
print(results)

# Save the model
joblib.dump(exported_pipeline, 'digits_model.joblib')
