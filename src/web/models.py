# coding: utf8
from django.db import models


class HWData(models.Model):
    char = models.CharField(max_length=8)
    width = models.IntegerField()
    height = models.IntegerField()
    strokes = models.TextField()

    @classmethod
    def copy(cls, hwdata):
        ret = cls(char=hwdata.char, width=hwdata.width, height=hwdata.height,
                  strokes=hwdata.strokes
                  )
        return ret