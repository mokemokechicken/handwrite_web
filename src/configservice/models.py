# coding: utf8
from django.db import models
import json

class TypeInfo(models.Model):
    typename = models.CharField(max_length=256)
    chars = models.TextField()
    infer_server_host = models.CharField(max_length=256)
    infer_server_port = models.IntegerField()
    data_server_url = models.CharField(max_length=512)
    encoder = models.CharField(max_length=256)
    encoder_params = models.TextField()
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def to_dict(self):
        ret = {
               "id": self.id, "typename": self.typename,
               "chars": self.chars,
               "infer_server_host": self.infer_server_host, "infer_server_port": self.infer_server_port,
               "data_server_url": self.data_server_url, 
               "encoder": self.encoder, "encoder_params": json.loads(self.encoder_params),
               }
        return ret
