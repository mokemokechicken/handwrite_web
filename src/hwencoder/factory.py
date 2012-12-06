# coding: utf8
'''
Created on 2012/12/05

@author: k_morishita
'''
from __future__ import absolute_import

from handwrite_web.data_config import get_encoder_type
from .simple_n_direction import ConvertSimpleNDirection
from hwencoder.split_n_direction import ConvertSplitNDirection

def create_converter(chartype):
    enc_type, params = get_encoder_type(chartype)
    if enc_type == "SimpleNDirection":
        return ConvertSimpleNDirection(**params)
    elif enc_type == "SplitNDirection":
        return ConvertSplitNDirection(**params)
    return ConvertSimpleNDirection(8)

