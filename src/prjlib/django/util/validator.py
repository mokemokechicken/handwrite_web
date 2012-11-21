# coding: utf-8
import re
import sys

FLOAT_PATTERN = re.compile("^[0-9]+\.[0-9]*[1-9]$")

def is_yyyy_mm_dd_hh_mm_ss(value, nullable=False):
    """日付時刻形式(YYYY/MM/DD HH:mm:ss)であることをチェックする。
    @param value
    @return boolean True:OK False:NG
    """
    if nullable and value is None:
        return True
    
    valid = re.match("^20[0-9]{2}-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]$", value) is not None
    return valid

def is_yyyymmddhhmmss(value, nullable=False):
    """日付時刻形式(YYYYMMDDHHmmss)であることをチェックする。
    @param value
    @return boolean True:OK False:NG
    """
    if nullable and value is None:
        return True
    
    valid = re.match("^20[0-9]{2}[0-1][0-9][0-3][0-9][0-2][0-9][0-5][0-9][0-5][0-9]$", value) is not None
    return valid

def check_length(value, min=0, max=sys.maxint, charset='utf8'):
    """文字列の長さをチェックする。
    @param value チェック対象文字列
    @param min 最小文字数
    @param max 最大文字数
    @param charset 文字コードセット
    @return boolean True:OK False:NG
    """
    length = 0
    if value is not None:
        length = len(value)
    
    return length >= min and length <= max

def is_digit(value, nullable=False):
    """文字列が数値のみで構成されていることをチェックする。
    @param value チェック対象文字列
    @param nullable Noneを許可するかどうか
    @return boolean True:OK False:NG
    """
    if nullable and value is None:
        return True
    
    return value is not None and value.isdigit()

def is_float(value, nullable=False):
    """文字列が小数値であることをチェックする。
    @param value チェック対象文字列
    @param nullable Noneを許可するかどうか
    @return boolean True:OK False:NG
    """
    if nullable and value is None:
        return True
    
    return value is not None and FLOAT_PATTERN.match(value) is not None
