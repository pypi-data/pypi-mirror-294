# cython: language_level=3
# cython: profile=True
# Time-stamp: <2024-04-26 10:40:41 Tao Liu>

"""Module description:

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file LICENSE included with
the distribution).
"""
# ------------------------------------
# python modules
# ------------------------------------
from math import sqrt
import logging

logger = logging.getLogger(__name__)
debug   = logger.debug
info    = logger.info
# ------------------------------------
# Other modules
# ------------------------------------

import numpy as np
cimport numpy as np
from cpython cimport bool

# ------------------------------------
# MACS3 modules
# ------------------------------------
from MACS3.Signal.Prob import pnorm2
from MACS3.Signal.BedGraph import bedGraphTrackI
from MACS3.Signal.Region import Regions

# ------------------------------------
# Misc functions
# ------------------------------------

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

cpdef list generate_weight_mapping( list fraglen_list, list means, list stddevs, float min_frag_p = 0.001 ):
    """Generate weights for each fragment length in short, mono, di, and tri-signals track

    return: list of four dictionaries, with key as fraglen and value as the weight.
            ret[0] -- dictionary for short
            ret[1] -- dictionary for mono
            ret[2] -- dictionary for di
            ret[3] -- dictionary for tri
    """
    cdef:
        list ret_mapping
        list variances
        int l
        float m_s, m_m, m_d, m_t
        float v_s, v_m, v_d, v_t
        float p_s, p_m, p_d, p_t
        float s
        int i, j
    assert len(means) == 4
    assert len(stddevs) == 4
    [m_s, m_m, m_d, m_t] = means
    [v_s, v_m, v_d, v_t] = [ x**2 for x in stddevs ]
    ret_mapping = [ {}, {}, {}, {} ]
    for i in range( len(fraglen_list) ):
        l = fraglen_list[ i ]
        p_s = pnorm2( float(l), m_s, v_s )
        p_m = pnorm2( float(l), m_m, v_m )
        p_d = pnorm2( float(l), m_d, v_d )
        p_t = pnorm2( float(l), m_t, v_t )
        s = p_s + p_m + p_d + p_t
        if p_s < min_frag_p and p_m < min_frag_p and p_d < min_frag_p and p_t < min_frag_p:
            # we exclude the fragment which can't be assigned to
            # short, mono, di-nuc, and tri-nuc (likelihood <
            # min_frag_p, default:0.001) Normally this fragment is too
            # large. We exclude these fragment by setting all weights
            # to zero.
            debug(f"The fragment length {l} can't be assigned to either distribution so will be excluded!")
            ret_mapping[ 0 ][ l ] = 0
            ret_mapping[ 1 ][ l ] = 0
            ret_mapping[ 2 ][ l ] = 0
            ret_mapping[ 3 ][ l ] = 0
            continue
        ret_mapping[ 0 ][ l ] = p_s / s
        ret_mapping[ 1 ][ l ] = p_m / s
        ret_mapping[ 2 ][ l ] = p_d / s
        ret_mapping[ 3 ][ l ] = p_t / s
    return ret_mapping

cpdef list generate_digested_signals( object petrack, list weight_mapping ):
    """Generate digested pileup signals (four tracks) using weight mapping 

    return: list of four signals in dictionary, with key as chromosome name and value as a p-v array.
            ret[0] -- dictionary for short
            ret[1] -- dictionary for mono
            ret[2] -- dictionary for di
            ret[3] -- dictionary for tri
    """
    cdef:
        list ret_digested_signals
        list ret_bedgraphs
        object bdg
        int i
        dict certain_signals
        np.ndarray pv
        bytes chrom
    ret_digested_signals = petrack.pileup_bdg_hmmr( weight_mapping )
    ret_bedgraphs = []
    for i in range( 4 ):                  #yes I hardcoded 4!
        certain_signals = ret_digested_signals[ i ]
        bdg = bedGraphTrackI()
        for chrom in sorted(certain_signals.keys()):
            bdg.add_chrom_data_hmmr_PV( chrom, certain_signals[ chrom ] )
        ret_bedgraphs.append( bdg )
    return ret_bedgraphs

cpdef list extract_signals_from_regions( list signals, object regions, int binsize = 10, hmm_type = 'gaussian'  ):
    # we will take regions in peaks, create a bedGraphTrackI with
    # binned regions in peaks, then let them overlap with signals to
    # create a list (4) of value arrays.
    # 
    cdef:
        list extracted_data, extracted_len, extracted_positions
        object signaltrack
        object regionsbdg
        bytes chrom
        int i, s, e, tmp_s, tmp_e, tmp_n, n, c, counter, prev_c
        list ps
        object p
        list ret_training_data, ret_training_lengths, ret_training_bins

    regionsbdg = _make_bdg_of_bins_from_regions( regions, binsize )
    debug('#      extract_signals_from_regions: regionsbdg completed')
    # now, let's overlap
    extracted_positions = []
    extracted_data = []
    extracted_len = []
    for signaltrack in signals: # four signal tracks
        # signaltrack is bedGraphTrackI object
        [ positions, values, lengths ] = signaltrack.extract_value_hmmr( regionsbdg )
        extracted_positions.append( positions )
        extracted_data.append( values )
        extracted_len.append( lengths )
    positions = []
    values = []
    lengths = []
    debug('#      extract_signals_from_regions: extracted positions, data, len')
    ret_training_bins = []
    ret_training_data = []
    ret_training_lengths = []
    
    nn = len( extracted_data[0] )
    assert nn > 0
    assert nn == len( extracted_data[1] )
    assert nn == len( extracted_data[2] )
    assert nn == len( extracted_data[3] )
    counter = 0
    prev_c = extracted_len[0][0]
    c = 0
    if hmm_type == "gaussian":
        for i in range( nn ):
            ret_training_bins.append( extracted_positions[0][i] )
            ret_training_data.append(
                [max( 0.0001, extracted_data[0][i] ),
                 max( 0.0001, extracted_data[1][i] ),
                 max( 0.0001, extracted_data[2][i] ),
                 max( 0.0001, extracted_data[3][i] ) ] )
            c = extracted_len[0][i]
            if counter != 0 and c != prev_c:
                ret_training_lengths.append( counter )
                counter = 0
            prev_c = c
            counter +=  1
        debug('#      extract_signals_from_regions: ret_training bins, data, lengths - gaussian')
    #poisson can only take int values as input
    if hmm_type == "poisson":
        for i in range( nn ):
            ret_training_bins.append( extracted_positions[0][i] )
            ret_training_data.append(
                [ int(max( 0.0001, extracted_data[0][i] )),
                int(max( 0.0001, extracted_data[1][i] )),
                int(max( 0.0001, extracted_data[2][i] )),
                int(max( 0.0001, extracted_data[3][i] )) ] )
            c = extracted_len[0][i]
            if counter != 0 and c != prev_c:
                ret_training_lengths.append( counter )
                counter = 0
            prev_c = c
            counter +=  1
        debug('#      extract_signals_from_regions: ret_training bins, data, lengths - poisson')
    # last region
    ret_training_lengths.append( counter )
    assert sum(ret_training_lengths) == len(ret_training_data)
    assert len(ret_training_bins) == len(ret_training_data)
    return [ ret_training_bins, ret_training_data, ret_training_lengths ]

cdef _make_bdg_of_bins_from_regions ( object regions, int binsize ):
    # this function will return a BedGraphTrackI object
    cdef:
        object regionsbdg
        long n
        bytes chrom
        list ps
        int s, e, tmp_p, mark_bin, i, r

    assert isinstance( regions, Regions )

    regionsbdg = bedGraphTrackI(baseline_value=-100)

    n = 0
    # here we convert peaks from a PeakIO to BedGraph object with a
    # given binsize.
    mark_bin = 1                      #this is to mark the continuous bins in the same region, it will increase by one while moving to the next region
    for chrom in sorted(regions.get_chr_names()):
        tmp_p = 0                         #this is to make gap in bedgraph for not covered regions.
        ps = regions[ chrom ]
        for i in range( len( ps ) ):
            # for each region
            s = ps[ i ][ 0 ]
            e = ps[ i ][ 1 ]
            # make bins, no need to be too accurate...
            s = s//binsize*binsize
            e = e//binsize*binsize
            #tmp_n = int(( e - s )/binsize)
            for r in range( s, e, binsize ):
                tmp_s = r
                tmp_e = r + binsize
                if tmp_s > tmp_p:
                    regionsbdg.add_loc_wo_merge( chrom, tmp_p, tmp_s, 0 ) #the gap
                regionsbdg.add_loc_wo_merge( chrom, tmp_s, tmp_e, mark_bin ) #the value we put in the bin bedgraph is the number of bins in this region
                n += 1
                tmp_p = tmp_e
            # end of region, we change the mark_bin
            mark_bin += 1
    # we do not merge regions in regionsbdg object so each bin will be separated.
    debug( f"added {n} bins" )
    return regionsbdg
