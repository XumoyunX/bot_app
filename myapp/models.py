from django.db import models






class Users(models.Model):
    name = models.CharField(max_length=50)
    shop_number = models.IntegerField(default=0)
    phone = models.CharField(max_length=13, null=True, blank=True)
    akp = models.CharField(max_length=8, null=True, blank=True)
    chat_id = models.BigIntegerField()
    ball = models.BigIntegerField(default=0)
    lang = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name