# coding: utf8
'''
Created on 2012/11/30

@author: k_morishita
'''


DATA_CONFIG = {
    "numbers": {
        "chars": u"０１２３４５６７８９",
        "host": "localhost",
        "port": 9999,
    },
    "num_hira": {
        "chars": u"０１２３４５６７８９あいうえおかきくけこがぎぐげごさしすせそざじずぜぞたちつてとだぢづでどなにぬねの" +
                 u"はひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわをん"
        ,
        "host": "localhost",
        "port": 9998,
    }
}

def get_chars(charset_type):
    return DATA_CONFIG[charset_type]["chars"]

def get_host_port(charset_type):
    cfg = DATA_CONFIG[charset_type]
    return cfg["host"], cfg["port"]
