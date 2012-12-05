# coding: utf8
'''
Created on 2012/12/05

@author: k_morishita
'''


from __future__ import absolute_import

import json
from unittest.case import TestCase

from mock import patch
from django.test.client import RequestFactory

from ..services import dataset_service
from web.models import HWData
from ymlib.unittest.misc import relative_package
from hwencoder.simple_n_direction import ConvertSimpleNDirection


class DataServiceTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    @patch(relative_package("..services.create_converter", __package__))
    @patch(relative_package("..services.get_hwdataset", __package__))
    @patch(relative_package("..services.get_chars", __package__), return_value=u"０１２３")
    def test_dataset_service(self, mock_get_chars, mock_get_hwdataset, m3):
        req = self.factory.get("/?noise_range=0.9,1.1&multiply=3")
        hwmodel = HWData(width=50, height=60, char=u"１", strokes=json.dumps([((0,0),(1,1)),((2,2),(1,1))]))
        mock_get_hwdataset.return_value = [hwmodel]
        m3.return_value = ConvertSimpleNDirection(8, 20)
        data, info = dataset_service(req, "hoge")
        self.assertEquals(4, info["out"])
        self.assertEquals(3, info["row"])
        self.assertEquals(8*2*20, info["in"])
        lines = data.strip().split("\n")
        self.assertEquals(3, len(lines))
        l1 = lines[0].split(",")
        self.assertEquals(1+8*2*20+1, len(l1)) # [id] + [num_in] + [y] 


