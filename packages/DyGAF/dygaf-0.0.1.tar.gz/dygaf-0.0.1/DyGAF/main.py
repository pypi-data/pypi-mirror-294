import os
import argparse
import pandas as pd
from .dependent_attention_model_pipeline import dependent_attention_model_pipeline
from .independent_attention_model_pipeline import independent_attention_model_pipeline
from .analyze_feature_importance import analyze_feature_importance

def DyGAF(df_path, target_column, seed, n_splits):
    # Load the dataset
    df_final = pd.read_csv(df_path, index_col=None, sep='\t')
    print(df_final.head())
    # Define output directory
    output_dir = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define paths for dependent, independent weights, and feature output files
    dependent_weights_path = os.path.join(output_dir, f'output_seed{seed}_dependent_attention_weights.csv')
    independent_weights_path = os.path.join(output_dir, f'output_seed{seed}_independent_attention_weights.csv')
    feature_output_path = os.path.join(output_dir, f'features_importance_seed{seed}.csv')
    print(os.getcwd())
    print(dependent_weights_path)
    print(feature_output_path)
    # Run the dependent attention model pipeline
    dependent_output_path = dependent_attention_model_pipeline(df_final, target_column, seed, n_splits, dependent_weights_path)
    print(f"Dependent attention weights saved to {dependent_output_path}")

    # Run the independent attention model pipeline
    independent_output_path = independent_attention_model_pipeline(df_final, target_column, seed, n_splits, independent_weights_path)
    print(f"Independent attention weights saved to {independent_output_path}")

    # Analyze the feature importance using both attention models
    features_df, accuracy = analyze_feature_importance(dependent_output_path, independent_output_path, df_final, seed, feature_output_path)
    #print(f"Feature importance saved to {feature_output_path}")
    print(f"Model accuracy: {accuracy:.4f}")

    return features_df, accuracy


def main():
    parser = argparse.ArgumentParser(description='Run the attention model pipeline and analyze feature importance.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Add arguments for each part of the pipeline
    parser.add_argument('--df_path', type=str, required=True, help='Path to the dataset CSV file')
    parser.add_argument('--target_column', type=str, required=True, help='Target column in the dataset')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    parser.add_argument('--n_splits', type=int, default=5, help='Number of splits for StratifiedKFold')

    args = parser.parse_args()


    # Run the pipeline with the provided arguments
    DyGAF(
        df_path=args.df_path,
        target_column=args.target_column,
        seed=args.seed,
        n_splits=args.n_splits
    )


