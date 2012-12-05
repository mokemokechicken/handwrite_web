# coding: utf8
'''
Created on 2012/11/30

@author: k_morishita
'''


DATA_CONFIG = {
    "numbers": {
        "chars": u"０１２３４５６７８９",
        # infer server endpoint
        "host": "localhost",
        "port": 9999,
        # stroke data encoding
        "encoder": "SimpleNDirection",
    },
    "num_hira": {
        "chars": u"０１２３４５６７８９あいうえおかきくけこがぎぐげごさしすせそざじずぜぞたちつてとだぢづでどなにぬねの" +
                 u"はひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわをん",
        # infer server endpoint
        "host": "localhost",
        "port": 9998,
        # stroke data encoding
        "encoder": "SimpleNDirection",
    }
}

def get_chars(charset_type):
    return DATA_CONFIG[charset_type]["chars"]

def get_host_port(charset_type):
    cfg = DATA_CONFIG[charset_type]
    return cfg["host"], cfg["port"]

def get_encoder_type(charset_type):
    cfg = DATA_CONFIG[charset_type]
    return cfg["encoder"]
    