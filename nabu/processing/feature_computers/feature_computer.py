'''@file feature_computer.py
contains the FeatureComputer class'''

from abc import ABCMeta, abstractmethod

class FeatureComputer(object):
    '''A featurecomputer is used to compute features'''

    __metaclass__ = ABCMeta

    def __init__(self, conf):
        '''
        FeatureComputer constructor

        Args:
            conf: the feature configuration
        '''

        self.conf = conf

    def __call__(self, sig, rate):
        '''
        compute the features

        Args:


        Returns:
            the features as a [seq_length x feature_dim] numpy array
        '''

        #snip the edges
        sig = snip(sig, rate, float(self.conf['winlen']),
                   float(self.conf['winstep']))

        #compute the features and energy
        feat = self.comp_feat(sig, rate)

        return feat

    @abstractmethod
    def comp_feat(self, sig, rate):
        '''
        compute the features

        Args:
            sig: the audio signal as a 1-D numpy array
            rate: the sampling rate

        Returns:
            the features as a [seq_length x feature_dim] numpy array
        '''

    @abstractmethod
    def get_dim(self):
        '''the feature dimemsion'''


def snip(sig, rate, winlen, winstep):
    '''
    snip the edges of the utterance to fit the sliding window

    Args:
        sig: audio signal
        rate: sampling rate
        winlen: length of the sliding window [s]
        winstep: stepsize of the sliding window [s]

    Returns:
        the snipped signal
    '''
    # calculate the number of frames in the utterance as number of samples in
    #the utterance / number of samples in the frame
    num_frames = int((len(sig)-winlen*rate)/(winstep*rate))
    # cut of the edges to fit the number of frames
    sig = sig[0:int(num_frames*winstep*rate + winlen*rate)]

    return sig