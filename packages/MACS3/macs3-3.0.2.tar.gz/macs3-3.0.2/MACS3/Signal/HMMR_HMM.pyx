# cython: language_level=3
# cython: profile=True
# Time-stamp: <2024-03-01 23:34:51 Tao Liu>

"""Module description:

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file LICENSE included with
the distribution).
"""
# ------------------------------------
# python modules
# ------------------------------------
from math import sqrt

# ------------------------------------
# Other modules
# ------------------------------------

import numpy as np
cimport numpy as np
from cpython cimport bool
import hmmlearn
from hmmlearn.hmm import GaussianHMM, PoissonHMM
from sklearn import cluster
import json
# from hmmlearn cimport hmm

# ------------------------------------
# MACS3 modules
# ------------------------------------
from MACS3.Signal.Prob import pnorm2

# ------------------------------------
# Misc functions
# ------------------------------------

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html
cdef inline float get_weighted_density( int x, float m, float v, w ):
    """Description:
    
    parameters:
      1. x: the observed value
      2. m: the mean of gaussian
      3. v: the variance of the gaussian
      4. w: the weight
    return value:
    """
    return w * pnorm2( float(x), m, v )

# ------------------------------------
# Classes
# ------------------------------------

# ------------------------------------
# public functions
# ------------------------------------


cpdef hmm_training( list training_data, list training_data_lengths, int n_states = 3, int random_seed = 12345, covar = 'full', hmm_type = 'gaussian' ):
    # training data should be in array like format: X = np.array([[.5, .3, .1, .1], [.6, .4, 0, 0]])
    # if we do not want init_prob to be updated through learning, set params = 'tmc' and init_prob = initial_state otherwise it will be overwritten
    # according to base documentation, if init_prob not stated, it is set to be equally likely for any state (1/ # of components)
    # if we have other known parameters, we should set these (ie: means_weights, covariance_type etc.)
    rs = np.random.RandomState(np.random.MT19937(np.random.SeedSequence(random_seed)))
    if hmm_type == "gaussian":
        hmm_model = GaussianHMM( n_components= n_states, covariance_type = covar, random_state = rs, verbose = False )
    if hmm_type == "poisson":
        hmm_model = PoissonHMM( n_components= n_states, random_state = rs, verbose = False )
    hmm_model = hmm_model.fit( training_data, training_data_lengths )
    assert hmm_model.n_features == 4
    return hmm_model

cpdef hmm_predict( list signals, list lens, hmm_model ):
    predictions = hmm_model.predict_proba( signals, lens )
    return predictions

cpdef void hmm_model_save( str model_file, object hmm_model, int hmm_binsize, int i_open_region, int i_nucleosomal_region, int i_background_region, hmm_type ):
    if hmm_type == "gaussian":
        if hmm_model.covariance_type == "diag":
            covars = hmm_model.covars_.diagonal(axis1=1, axis2=2)
        elif hmm_model.covariance_type == "full":
            covars = hmm_model.covars_
        else:
            raise Exception(f"Unknown covariance type {hmm_model.covariance_type}")
        with open( model_file, "w" ) as f:
            json.dump( {"startprob":hmm_model.startprob_.tolist(),
                        "transmat":hmm_model.transmat_.tolist(),
                        "means":hmm_model.means_.tolist(),
                        "covars":covars.tolist(),
                        "covariance_type":hmm_model.covariance_type,
                        "n_features":int(hmm_model.n_features),
                        "i_open_region":int(i_open_region),
                        "i_background_region":int(i_background_region),
                        "i_nucleosomal_region":int(i_nucleosomal_region),
                        "hmm_binsize":int(hmm_binsize), 
                        "hmm_type":hmm_type}, f )
    if hmm_type == "poisson":
        with open( model_file, "w" ) as f:
            json.dump( {"startprob":hmm_model.startprob_.tolist(),
                        "transmat":hmm_model.transmat_.tolist(),
                        "lambdas":hmm_model.lambdas_.tolist(),
                        "n_features":int(hmm_model.n_features),
                        "i_open_region":int(i_open_region),
                        "i_background_region":int(i_background_region),
                        "i_nucleosomal_region":int(i_nucleosomal_region),
                        "hmm_binsize":int(hmm_binsize),
                        "hmm_type":hmm_type}, f )

cpdef list hmm_model_init( str model_file ):
    with open( model_file ) as f:
        m = json.load( f )
        hmm_type = m.get("hmm_type", "gaussian") #if no model_type written, assume older file and use gaussian
        if hmm_type == "gaussian":
            hmm_model = GaussianHMM( n_components=3, covariance_type=m["covariance_type"] )
            hmm_model.means_ = np.array(m["means"])
            hmm_model.covars_ = np.array(m["covars"])
            hmm_model.covariance_type = m["covariance_type"]
        if hmm_type == "poisson":
            hmm_model = PoissonHMM( n_components=3 )
            hmm_model.lambdas_ = np.array(m["lambdas"])
        hmm_model.startprob_ = np.array(m["startprob"])
        hmm_model.transmat_ = np.array(m["transmat"])
        hmm_model.n_features = m["n_features"]
        return [ hmm_model, m["i_open_region"], m["i_background_region"], m["i_nucleosomal_region"], m["hmm_binsize"], hmm_type ]
