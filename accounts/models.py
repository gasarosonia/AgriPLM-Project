from django.db import models
from django.contrib.auth.models import User
# Create your models here.
MUSHA_CELL_CHOICES =(
    ('Kagarama','Kagarama'),
    ('Nyakabanda','Nyakabanda'),
    ('Musha','Musha'),
    ('Akabare','Akabare'),
    ('Nyabisindu','Nyabisindu'),
    ('Budahanda','Budahanda')
)
TITLE_CHOICES = (
    ('farmer', 'Farmer'),
    ('admin','Admin'),
)
class UserProfiles(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    photo = models.ImageField(upload_to='profile_pictures',null=True, blank=True)
    title = models.CharField(max_length=50, default='farmer',choices=TITLE_CHOICES,null=True, blank=True)
    province = models.CharField(max_length=20, default="Eastern", blank=True, null=True)
    district = models.CharField(max_length=20,default="Rwamagana",blank=True, null=True)
    sector = models.CharField(max_length=20,default="Musha Sector")
    cell = models.CharField(max_length=20,choices=MUSHA_CELL_CHOICES,blank=True,null=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'UserProfiles'