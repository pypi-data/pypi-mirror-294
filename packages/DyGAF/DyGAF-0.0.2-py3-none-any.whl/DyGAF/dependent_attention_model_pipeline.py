# -*- coding: utf-8 -*-""
# Importing required libraries and modules
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import LabelEncoder
# Saving the dictionary to a file (CSV format for easy readability and further processing)
import csv
import random
import os
#import tqdm
import tensorflow as tf
from tensorflow.keras import layers, models, initializers
from sklearn.metrics import accuracy_score

# Import additional libraries
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

import tensorflow_addons as tfa
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score


class CustomAttentionLayer_dpnt(layers.Layer):
    def __init__(self, seed=None, **kwargs):
        super(CustomAttentionLayer_dpnt, self).__init__(**kwargs)
        self.seed = seed  # Store the seed value

    def build(self, input_shape):
        # Define attention weights and bias as trainable variables with the dynamic seed
        self.w = self.add_weight(name='attention_weight',
                                 shape=(input_shape[1], 1),
                                 initializer=tf.keras.initializers.RandomNormal(seed=self.seed),  # Use the dynamic seed
                                 trainable=True)
        self.b = self.add_weight(name='attention_bias',
                                 shape=(input_shape[1],),
                                 initializer='zeros',
                                 trainable=True)
        super(CustomAttentionLayer_dpnt, self).build(input_shape)
    def call(self, inputs, **kwargs):
        # Compute attention scores
        attention_score = tf.nn.sigmoid(tf.nn.tanh(tf.matmul(inputs, self.w) + self.b))
        weighted_output = tf.math.reduce_mean(attention_score, axis=0) * inputs

        # Compute attention scores again
        attention_score = tfa.activations.sparsemax(tf.matmul(weighted_output, self.w) + self.b, axis=1)
        weighted_output = tf.math.reduce_mean(attention_score, axis=0) * inputs

        placeholder = tf.zeros(inputs.shape[-1])
        weighted_output = tf.add(placeholder, weighted_output)
        weighted_output /= 8
        output = weighted_output

        return output, attention_score
    
    
def build_multihead_attention_model_dpnt(input_shape, num_heads, seed= None):
    # Set TensorFlow seed for reproducibility if passed
    if seed is not None:
        tf.random.set_seed(seed)
        
    inputs = layers.Input(shape=input_shape)

    # Multi-head attention output and weights
    multihead_outputs = []
    attention_weights_list = []

    for _ in range(num_heads):
        attention_output, attention_weights = CustomAttentionLayer_dpnt(seed= seed, name=f'attention_layer_head_{_}')(inputs)
        multihead_outputs.append(attention_output)
        attention_weights_list.append(attention_weights)

    # Combine outputs from all heads
    combined_output = layers.Concatenate()(multihead_outputs) if num_heads > 1 else multihead_outputs[0]

    flattened_output = layers.Flatten()(combined_output)
    outputs = layers.Dense(1, activation='sigmoid')(flattened_output)

    model = models.Model(inputs=inputs, outputs=[outputs] + attention_weights_list)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


def dependent_attention_model_pipeline(df, target_column, seed, n_splits, output_dir):
    # Set the seed for reproducibility
    np.random.seed(seed)  # For NumPy operations
    random.seed(seed)  # For Python's random module
    tf.random.set_seed(seed)  # For TensorFlow operations
    
    # Prepare data
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # Encode labels if necessary
    y = LabelEncoder().fit_transform(y)

    # Stratified K-Fold setup
    skf = StratifiedKFold(n_splits=n_splits, random_state=seed, shuffle=True)
    
    # Initialize variables
    attn_weights_list = []

    for i, (train_index, test_index) in enumerate(skf.split(X, y)):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
        # Build and train the model
        model_with_weights = build_multihead_attention_model_dpnt(X_train.shape[1:], num_heads=4, seed=seed)
        model_with_weights.fit(X_train, y_train, validation_split=0.1, epochs=100, batch_size=16)
        
        # Predict and process attention weights
        preds = model_with_weights.predict(X_test)
        preds[0] = (preds[0] > 0.5).astype(int)
        
        attn_weights_list.append(preds[1])  # Save the attention weights
    
    # Concatenate attention weights across all folds, handling unequal fold sizes
    combined_array = np.concatenate(attn_weights_list, axis=0)

    # Calculate the mean across each column (averaging across all samples and all features)
    average_attention_weights = np.mean(combined_array, axis=0)
    
    # Combining feature names and their corresponding attention weights into a dictionary
    features_dict = {X.columns[i]: average_attention_weights[i] for i in range(len(X.columns))}
    

    # Define save path inside output directory
    save_path = output_dir
    
    # Writing to the file in the output directory
    with open(save_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Feature Name', 'Attention Weight'])
        for key, value in features_dict.items():
            writer.writerow([key, value])

    return save_path

# Example usage:
# save_path = dependent_attention_model_pipeline(df_final, 'Target', seed=42, n_splits=5, save_path='output_attention_weights.csv')
