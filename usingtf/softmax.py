# Obvious ripoff of softmax.py, which is:
#
# ==============================================================================
# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""A very simple MNIST classifier.

See extensive documentation at
https://www.tensorflow.org/get_started/mnist/beginners
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse, sys
import tensorflow as tf


def main(_):
    # Import data

    # Create the model
    # 1 input layer 0 hidden layers 1 output layer
    
    x = tf.placeholder(tf.float32, [None,1])
    # input layer        batch size ^    ^ input size
    W = tf.Variable(    tf.zeros((1,10)))
    # weight layer 0   batch size ^ ^ output size
    b = tf.Variable(    tf.zeros([10]))
    # bias layer 0    output size ^
    y = tf.matmul(x, W) + b
    # output layer  shape = (batch size, output size)


    # Define loss and optimizer
    y_ = tf.placeholder(tf.int64, [None])

    # The raw formulation of cross-entropy,
    #
    #   tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.nn.softmax(y)),
    #                                 reduction_indices=[1]))
    #
    # can be numerically unstable.
    #
    # So here we use tf.losses.sparse_softmax_cross_entropy on the raw
    # outputs of 'y', and then average across the batch.
    cross_entropy = tf.losses.sparse_softmax_cross_entropy(labels=y_, logits=y)
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()
    # Train
    for _ in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})









 
