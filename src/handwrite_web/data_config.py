# coding: utf8
'''
Created on 2012/11/30

@author: k_morishita
'''

from __future__ import absolute_import

import copy
import time
from configservice.client.client import ConfigClient

CONFIG_SERVER_URL = "http://localhost:8000/config"

_CONFIG_CACHE = {}
_CONFIG_CACHE_TIME = {}
CACHE_EXPIRE = 10

def load_config(charset_type):
    if charset_type not in _CONFIG_CACHE or _CONFIG_CACHE_TIME[charset_type]+CACHE_EXPIRE < time.time():
        cc = ConfigClient(CONFIG_SERVER_URL)
        _CONFIG_CACHE[charset_type] = cc.get_config(charset_type)
        _CONFIG_CACHE_TIME[charset_type] = time.time()
    return copy.copy(_CONFIG_CACHE[charset_type])

def get_chars(charset_type):
    return load_config(charset_type)["chars"]

def get_host_port(charset_type):
    cfg = load_config(charset_type)
    return cfg["infer_server_host"], cfg["infer_server_port"]

def get_encoder_type(charset_type):
    cfg = load_config(charset_type)
    return cfg["encoder"], cfg["encoder_params"]

