# coding: utf8
'''
Created on 2012/11/30

@author: k_morishita
'''


DATA_CONFIG = {
    "numbers": {
        "chars": u"０１２３４５６７８９",
    }
}

def get_chars(charset_type):
    return DATA_CONFIG[charset_type]["chars"]
