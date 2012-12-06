# coding: utf8
from django.db import models


class HWData(models.Model):
    char = models.CharField(max_length=8)
    width = models.IntegerField()
    height = models.IntegerField()
    strokes = models.TextField()
    validated = models.BooleanField(default=False)
    is_use = models.BooleanField(default=True)
    fb_ok = models.IntegerField(default=0)
    fb_ng = models.IntegerField(default=0)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    @classmethod
    def copy(cls, hwdata):
        ret = cls(char=hwdata.char, width=hwdata.width, height=hwdata.height,
                  strokes=hwdata.strokes
                  )
        return ret