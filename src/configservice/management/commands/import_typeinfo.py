# coding: utf8
'''
Created on 2012/12/12

@author: k_morishita
'''

from __future__ import with_statement

from django.core.management.base import BaseCommand
import json
from configservice.models import TypeInfo

class Command(BaseCommand):
    args = "<json filename>"
    help = u"指定されたJSON形式のファイルからTypeInfoをImportします。同一Typenameが存在すれば更新します。"

    def handle(self, *args, **options):
        if len(args) == 0:
            self.print_help("manage.py", "import_typeinfo")
            return
        filename = args[0]
        self.import_typeinfo(filename)
    
    def import_typeinfo(self, filename):
        with open(filename) as fin:
            data = json.load(fin)
        for typename, conf in data.items():
            self.import_conf(typename, conf)
    
    def import_conf(self, typename, conf):
        query = TypeInfo.objects.filter(typename=typename)[:1]
        if len(query) == 0:
            model = TypeInfo()
        else:
            model = query[0]
        model.typename = typename
        model.chars = conf["chars"]
        model.infer_server_host = conf["infer_server_host"]
        model.infer_server_port = conf["infer_server_port"]
        model.data_server_url = conf["data_server_url"]
        model.encoder = conf["encoder"]
        model.encoder_params = json.dumps(conf["encoder_params"])
        model.save()


