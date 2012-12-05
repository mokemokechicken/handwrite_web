# coding: utf8
'''
Created on 2012/12/05

@author: k_morishita
'''

from __future__ import absolute_import

from unittest.case import TestCase

from django.test.client import RequestFactory

from ymlib.unittest.misc import relative_package
import json
from mock import patch

from ..services import service_post_hwdata
from ..models import HWData
from hwencoder.simple_n_direction import ConvertSimpleNDirection


class ServiceHWDataTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    
    @patch(relative_package("..services.create_converter", __package__), return_value=ConvertSimpleNDirection(8))
    @patch(relative_package("..services.service_infer", __package__), return_value=[1,1,1])
    def test_service_post_hwdata(self, sinfer_mock, m2):
        req = self.factory.get("/hogehoge/api/hwdata")
        hwdata = {"meta": {"size": (50,60)}, "char": u"あ", "strokes": [((0,0),(1,1)),((2,2),(3,3))]}
        data = json.dumps(hwdata)
        success, ret = service_post_hwdata(req, "hogehoge", data, True)
        self.assertEquals(True, success)
        self.assertEquals(True, ret["success"])
        self.assertEquals([1,1,1], ret["ys"])
        self.assertEquals(True, sinfer_mock.called)
        
        q = HWData.objects.all().order_by("-id")
        model = q[0]
        self.assertEquals((50,60), (model.width, model.height))
        self.assertEquals(u"あ", model.char)

    @patch(relative_package("..services.create_converter", __package__), return_value=ConvertSimpleNDirection(8))
    @patch(relative_package("..services.HWData", __package__))
    @patch(relative_package("..services.service_infer", __package__), return_value=[1,1,1])
    def test_service_get_hwdata(self, sinfer_mock, modelCls, m3):
        req = self.factory.get("/hogehoge/api/hwdata")
        hwdata = {"meta": {"size": (50,60)}, "char": u"あ", "strokes": [((0,0),(1,1)),((2,2),(3,3))]}
        data = json.dumps(hwdata)
        #
        success, ret = service_post_hwdata(req, "hogehoge", data, False)
        self.assertEquals(True, success)
        self.assertEquals(True, ret["success"])
        self.assertEquals([1,1,1], ret["ys"])
        self.assertEquals(True, sinfer_mock.called)
        #
        model_instance = modelCls.return_value
        self.assertEquals(False, model_instance.save.called)
        

