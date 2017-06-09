'''@file cross_entropy_evauator.py
contains the CrossEntropyEvaluator class'''

import tensorflow as tf
import evaluator
from nabu.neuralnetworks.components import ops

class CrossEntropyEvaluator(evaluator.Evaluator):
    '''a evaluator for evaluating the cross-entropy loss'''

    def compute_loss(self, inputs, input_seq_length, targets,
                     target_seq_length):
        '''compute the validation loss for a batch of data

        Args:
            inputs: the inputs to the neural network, this is a dictionary of
                [batch_size x ...] tensors
            input_seq_length: The sequence lengths of the input utterances, this
                is a dictionary of [batch_size] vectors
            targets: the targets to the neural network, this is a list of
                [batch_size x max_output_length] tensors.
            target_seq_length: The sequence lengths of the target utterances,
                this is a dictionary of [batch_size] vectors

        Returns:
            the loss as a scalar'''

        #compute logits
        logits, logit_seq_length = self.model(
            inputs=inputs,
            input_seq_length=input_seq_length,
            targets=targets,
            target_seq_length=target_seq_length,
            is_training=False)

        #compute loss
        with tf.name_scope('cross_entropy_loss'):
            losses = []

            for t in targets:
                #stack all the logits except the final logits
                stacked_logits = ops.seq2nonseq(logits[t], logit_seq_length[t])

                #create the stacked targets
                stacked_targets = ops.seq2nonseq(targets[t],
                                                 target_seq_length[t])

                losses.append(tf.nn.sparse_softmax_cross_entropy_with_logits(
                    logits=stacked_logits,
                    labels=stacked_targets))

            loss = tf.reduce_sum(losses)

        return loss