from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Common(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    class Meta:
        abstract = True

class Prop(Common):
    """ property for models """
    is_must          = models.BooleanField(default=False)
    optional_value   = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'property'

    def __str__(self):
        return self.code

    def get_optional_value(self):
        value_list = []
        if self.optional_value:
            value_list = [value.strip() for value in self.optional_value.split(';')]
        return value_list

class Category(Common):
    """ model type """
    props    = models.ManyToManyField(Prop)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.code

class HostGroup(Common):
    """docstring for HostGroup"""
    class Meta:
        db_table = 'hostgroup'

    def __str__(self):
        return self.code
        
class Host(models.Model):
    """ model for Host """
    SALT_STATUS_CHOICE = (("ok", "正常"), ("error", "错误"))
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    groups      = models.ManyToManyField(HostGroup, blank=True)
    admins      = models.ManyToManyField(User, blank=True)
    minion_id   = models.CharField(max_length=30)
    hostname    = models.CharField(max_length=100)
    ip          = models.CharField(max_length=20)
    os          = models.CharField(max_length=50)
    cpu         = models.CharField(max_length=100)
    mem         = models.CharField(max_length=50)
    eth         = models.CharField(max_length=200)
    is_virtual  = models.CharField(max_length=50)
    salt_key    = models.CharField(max_length=50, blank=True, null=True)
    minion_status = models.CharField(max_length=10, choices=SALT_STATUS_CHOICE, default="ok")

    class Meta:
        db_table = 'host'

    def __str__(self):
        return self.hostname
        
    