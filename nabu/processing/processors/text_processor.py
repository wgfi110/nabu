'''@file text_processor.py
Contains the TextProcessor'''

import os
import numpy as np
import processor
from nabu.processing.target_normalizers import normalizer_factory

class TextProcessor(processor.Processor):
    '''a processor for text data, does normalization'''

    def __init__(self, conf):
        '''TextProcessor constructor

        Args:
            conf: the textprocessor configuration as a dict of strings'''

        #create the normalizer
        self.normalizer = normalizer_factory.factory(conf['normalizer'])

        self.alphabet = conf['alphabet'].split(' ')

        #initialize the metadata
        self.max_length = 0
        self.sequence_length_histogram = np.zeros(0, dtype=np.int32)

        super(TextProcessor, self).__init__(conf)

    def __call__(self, dataline):
        '''process the data in dataline
        Args:
            dataline: a line of text

        Returns:
            The normalized text as a string'''

        #normalize the line
        normalized = self.normalizer(dataline, self.alphabet)

        #update the metadata
        self.max_length = max(self.max_length, len(normalized.split(' ')))
        seq_length = len(normalized.split(' '))
        if seq_length >= self.sequence_length_histogram.shape[0]:
            self.sequence_length_histogram = np.concatenate(
                [self.sequence_length_histogram, np.zeros(
                    seq_length-self.sequence_length_histogram.shape[0]+1,
                    dtype=np.int32)]
            )
        self.sequence_length_histogram[seq_length] += 1

        return normalized

    def write_metadata(self, datadir):
        '''write the processor metadata to disk

        Args:
            dir: the directory where the metadata should be written'''

        with open(os.path.join(datadir, 'max_length'), 'w') as fid:
            fid.write(str(self.max_length))
        with open(os.path.join(datadir, 'sequence_length_histogram.npy'),
                  'w') as fid:
            np.save(fid, self.sequence_length_histogram)
        with open(os.path.join(datadir, 'alphabet'), 'w') as fid:
            fid.write(' '.join(self.alphabet))
        with open(os.path.join(datadir, 'dim'), 'w') as fid:
            fid.write(str(len(self.alphabet)))