from django.db import models

class Token(models.Model):
    uuid = models.CharField(max_length=200, unique=True)
    expiration_unixtime = models.IntegerField()

    def __str__(self):
        return self.uuid