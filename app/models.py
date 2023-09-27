from django.db import models
from django.contrib.auth.models import  User
# Create your models here.

class SUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile= models.CharField(max_length=15,null=True)
    gender= models.CharField(max_length=10, null=True)
    age=models.CharField(max_length=15,null=True)
    address=models.CharField(max_length=150,null=True)
    img= models.FileField(null=True, blank=True, upload_to='avatar', default='avatar.jpeg')
    def __str__(self):
        return self.user.username
    
class UploadPhpto(models.Model):
    suser = models.ForeignKey(SUser,on_delete=models.CASCADE)
    file= models.FileField()
    postdate = models.DateField()

class Comments(models.Model):
    photo = models.ForeignKey(UploadPhpto,on_delete=models.CASCADE)
    suser = models.ForeignKey(SUser,on_delete=models.CASCADE)
    comment= models.CharField(max_length=200,null=True)
    postdate = models.DateField()
    def __str__(self) -> str:
        return self.comment[0:20] +"............................. User Name : "+self.suser.user.first_name
