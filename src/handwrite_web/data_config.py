# coding: utf8
'''
Created on 2012/11/30

@author: k_morishita
'''
import copy

DATA_CONFIG = {
    "numbers": {
        "chars": u"０１２３４５６７８９",
        # infer server endpoint
        "host": "localhost",
        "port": 9999,
        # stroke data encoding
        "encoder": "SimpleNDirection",
        "encoder_params": {"n_direction": 8},
    },
    "num_hira": {
        "chars": u"０１２３４５６７８９あいうえおかきくけこがぎぐげごさしすせそざじずぜぞたちつてとだぢづでどなにぬねの" +
                 u"はひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわをん",
        # infer server endpoint
        "host": "localhost",
        "port": 9998,
        # stroke data encoding
        "encoder": "SimpleNDirection",
        "encoder_params": {"n_direction": 8},
    }
}

d8 = copy.copy(DATA_CONFIG["num_hira"])
d8["encoder"] = "SplitNDirection"
d8["encoder_params"] = {"n_direction": 8}
d8["port"] = 9997
DATA_CONFIG["num_hira-d8"] = d8

d2 = copy.copy(d8)
d2["encoder_params"] = {"n_direction": 2}
d2["port"] = 9996
DATA_CONFIG["num_hira-d2"] = d2

def get_chars(charset_type):
    return DATA_CONFIG[charset_type]["chars"]

def get_host_port(charset_type):
    cfg = DATA_CONFIG[charset_type]
    return cfg["host"], cfg["port"]

def get_encoder_type(charset_type):
    cfg = DATA_CONFIG[charset_type]
    return cfg["encoder"], cfg["encoder_params"]

