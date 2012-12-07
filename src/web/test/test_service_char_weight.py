# coding: utf8
'''
Created on 2012/12/07

@author: k_morishita
'''

from __future__ import absolute_import

from unittest.case import TestCase

from ..services import service_char_weight
from mock import patch
from ymlib.unittest.misc import relative_package
from django.test.client import RequestFactory
from web.models import HWData

class ServiceCharWeightTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    @patch(relative_package("..services.get_chars", __package__), return_value="abcdefg")
    def test_service_char_weight(self, m1):
        chartype = "hoge"
        req = self.factory.get("/")
        HWData(char="b", width=10, height=10, strokes="[]").save()
        HWData(char="b", width=10, height=10, strokes="[]").save()
        HWData(char="c", width=10, height=10, strokes="[]").save()
        HWData(char="d", width=10, height=10, strokes="[]").save()
        HWData(char="e", width=10, height=10, strokes="[]").save()
        HWData(char="e", width=10, height=10, strokes="[]").save()
        HWData(char="e", width=10, height=10, strokes="[]").save()
        success, response = service_char_weight(req, chartype)
        self.assertEquals(True, success)
        cnt = response["charCount"]
        self.assertEquals(2, cnt["b"])
        self.assertEquals(1, cnt["c"])
        self.assertEquals(1, cnt["d"])
        self.assertEquals(3, cnt["e"])
    