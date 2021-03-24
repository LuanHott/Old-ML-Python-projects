import tensorflow as tf
from tensorflow import keras

import csv
import pandas as pd

import numpy as np

import matplotlib as plt

import logging
logger = tf.get_logger()
logger.setLevel(logging.ERROR)

tabela = pd.read_csv('owid-covid-data.csv')

print (tabela)

y_tabela = tabela.pop('new_deaths')

labels = tabela.columns.values

categorical_columns = ['iso_code','location']
numeric_columns = ['date', 'total_cases', 'new_cases', 'total_deaths',
 'total_cases_per_million', 'new_cases_per_million',
 'total_deaths_per_million', 'new_deaths_per_million']

feature_columns = []
for feature_name in categorical_columns:
    vocabulary = tabela[feature_name].unique()
    feature_columns.append(tf.feature_column.categorical_column_with_vocabulary_list(feature_name,vocabulary))

for feature_name in numeric_columns:
    feature_columns.append(tf.feature_column.numeric_column(feature_name, dtype=tf.float32))

def make_input_fn(data_df, label_df, num_epochs = 10, shuffle = True, batch_size=32):
    def input_function():
        ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))
        if shuffle:
            ds = ds.shuffle(1000)
        ds = ds.batch(batch_size).repeat(num_epochs)
        return ds
    return input_function

treino_input_fn = make_input_fn(tabela, y_tabela)

linear_est = tf.estimator.LinearClassifier(feature_columns=feature_columns)

result = linear_est.train(treino_input_fn)

print(result)