from django.db import models
from telegram import Update
from language import MultiLanguage, multilanguage





class User(models.Model):


    chat_id = models.BigIntegerField()
    fullname = models.TextField(null=True,blank=True)
    username = models.CharField(max_length=255,null=True,blank=True)


    is_registered = models.BooleanField(default=False)

    lang = models.CharField(max_length=2)

    name = models.CharField(max_length=50)
    shop_number = models.IntegerField(default=0)
    phone = models.CharField(max_length=13, null=True, blank=True)
    akp = models.CharField(max_length=8, null=True, blank=True)
    ball = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name




    @classmethod
    def get(cls, update:Update):
        return (
            tgUser:=update.effective_user,
            user:=cls.objects.get_or_create(
                chat_id=tgUser.id,
                defaults=dict(
                    fullname=tgUser.full_name,
                    username=tgUser.username
                )
            )[0],
            user.temp
        )


    @property
    def temp(self):
        return UserTemp.objects.get_or_create(user=self)[0]

    def text(self, textName, **kwargs):
        print(self.lang)
        return multilanguage.get(textName, self.lang, **kwargs)




class UserTemp(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)




    int1 = models.IntegerField(null=True,blank=True)
    int2 = models.IntegerField(null=True,blank=True)
    int3 = models.IntegerField(null=True,blank=True)
    int4 = models.IntegerField(null=True,blank=True)
    int5 = models.IntegerField(null=True,blank=True)


    str1 = models.TextField(null=True,blank=True)
    str2 = models.TextField(null=True,blank=True)
    str3 = models.TextField(null=True,blank=True)
    str4 = models.TextField(null=True,blank=True)
    str5 = models.TextField(null=True,blank=True)

