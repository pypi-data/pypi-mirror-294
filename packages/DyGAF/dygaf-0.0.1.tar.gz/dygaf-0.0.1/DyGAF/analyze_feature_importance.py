import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def analyze_feature_importance(dependent_weights_path, independent_weights_path, df_final, seed, feature_output_path):
    # Load dependent and independent attention weights
    dependent_df = pd.read_csv(dependent_weights_path)
    independent_df = pd.read_csv(independent_weights_path)
    
    weights_dependent, weights_independent = dependent_df['Attention Weight'], independent_df['Attention Weight']

    # Normalize the attention weights
    w_independent_normalized = (weights_independent - np.min(weights_independent)) / (np.max(weights_independent) - np.min(weights_independent))
    w_dependent_normalized = (weights_dependent - np.min(weights_dependent)) / (np.max(weights_dependent) - np.min(weights_dependent))

    # Custom scoring function
    def custom_score2(w1, w2):
        min_component = np.minimum(w1, w2)  # Captures importance of low values
        product_component = w1 * w2         # Captures importance of high values
        return 2 * (((min_component + product_component) / 2) ** 2)  # Squared average to balance both conditions

    # Calculate custom scores for each feature
    custom_scores2 = custom_score2(w_independent_normalized, w_dependent_normalized)

    # Create a DataFrame for analysis
    df_features = pd.DataFrame({
        'Feature Name': dependent_df['Feature Name'],
        'CustomScore': custom_scores2
    })

    # Prepare the features and target from the provided DataFrame
    X = df_final.drop(columns=["Target"])
    y = df_final["Target"]
    y = LabelEncoder().fit_transform(y)

    # Apply the custom scores to the features
    for i, j in enumerate(df_features['Feature Name']):
        X[j] = X[j] * df_features['CustomScore'][i]

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=4)

    # Initialize and train the Random Forest classifier
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_split=5, random_state=4)
    clf.fit(X_train, y_train)

    # Make predictions on the test set and evaluate the model
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")

    # Get feature importances
    feature_importances = clf.feature_importances_
    feature_names = X.columns

    # Create a DataFrame with feature importances
    features_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': feature_importances,
    }).sort_values(by='Importance', ascending=False)

    # Sort the features by importance
    features_df = features_df.sort_values(by='Importance', ascending=False).reset_index(drop=True)

    # Save the feature importance DataFrame to a CSV file
    features_df.to_csv(feature_output_path, index=False)
    print(f"Feature importance saved to {feature_output_path}")

    # Return feature importance DataFrame and accuracy
    return features_df, accuracy

'''
dependent_weights_path = '/Users/mdkito51/Desktop/DM_lab_23-24/04. Covid_19/DyGAF_FOLDER/DyGAF_model_code/new_CUSTOM_ATTENTION_DEPENDENT_MODEL_all_FEATURES_multihead4_updated_070924.csv'
independent_weights_path = '/Users/mdkito51/Desktop/DM_lab_23-24/04. Covid_19/DyGAF_FOLDER/DyGAF_model_code/new_CUSTOM_ATTENTION_INDEPENDENT_MODEL_all_FEATURES_multihead4_updated_070924.csv'

df_final = pd.read_csv('/Users/mdkito51/Desktop/DM_lab_23-24/04. Covid_19/DyGAF_FOLDER/package/input/covid_input_file.csv', index_col=None, sep = '\t')  # Replace with the actual path to your data
seed = 42
feature_output_path = f"features_importance_{seed}.csv"  # Output file for feature importances

# Get the feature importance DataFrame and accuracy
features_df, accuracy = analyze_feature_importance(dependent_weights_path, independent_weights_path, df_final, seed, feature_output_path)

# Display the top features
print(features_df.head(100))  # Top 100 features
print(f"Model Accuracy: {accuracy:.4f}")
'''