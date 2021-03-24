import tensorflow as tf
import numpy as np 
import logging
logger = tf.get_logger()
logger.setLevel(logging.ERROR)

base = np.array([1.9, 2.3, 4.0, 4.7, 5.3], dtype = float)
result = np.array([6.1, 7.3, 12.4, 14.5, 16.3], dtype = float)

l0 = tf.keras.layers.Dense(units = 1, input_shape=[1])
model = tf.keras.Sequential(l0)

model.compile(loss='mean_squared_error', optimizer='sgd')

treino = model.fit(base, result, epochs= 500)

print(model.predict([1])* 10)