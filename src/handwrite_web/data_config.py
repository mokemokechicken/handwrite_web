# coding: utf8
'''
Created on 2012/11/30

@author: k_morishita
'''

from __future__ import absolute_import
from configservice_client.config import load_config

def get_chars(charset_type):
    return load_config(charset_type)["chars"]

def get_host_port(charset_type):
    cfg = load_config(charset_type)
    return cfg["infer_server_host"], cfg["infer_server_port"]

def get_encoder_type(charset_type):
    cfg = load_config(charset_type)
    return cfg["encoder"], cfg["encoder_params"]

