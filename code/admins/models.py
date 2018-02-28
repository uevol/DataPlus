from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    ''' user profile '''
    user     = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    roles    = models.ManyToManyField('Role')
    phone    = models.CharField(max_length=30, blank=True)
    wechat   = models.CharField(max_length=30, blank=True)
    comment  = models.TextField(max_length=100, blank=True)

    class Meta:
        ''' class meta info '''
        db_table = 'user_profile'

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    '''create or update user profile '''
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()

class GroupProfile(models.Model):
    ''' user profile '''
    group   = models.OneToOneField(Group, related_name='profile', on_delete=models.CASCADE)
    roles   = models.ManyToManyField('Role')

    class Meta:
        ''' class meta info '''
        db_table = 'group_profile'

    def __str__(self):
        return self.group.name

@receiver(post_save, sender=Group)
def create_or_update_group_profile(sender, instance, created, **kwargs):
    '''create or update user profile '''
    if created:
        GroupProfile.objects.create(group=instance)
    instance.profile.save()

class Role(models.Model):
    ''' user role '''
    name   = models.CharField(max_length=30, unique=True)
    perms  = models.ManyToManyField('Perm', blank=True)

    class Meta:
        ''' class meta info '''
        db_table = 'role'

    def __str__(self):
        return self.name

class Perm(models.Model):
    ''' custom permission '''
    name   = models.CharField(max_length=100)
    code   = models.CharField(max_length=100)

    class Meta:
        ''' class meta info '''
        db_table = 'permission'

    def __str__(self):
        return self.name


class Menu(models.Model):
    name   = models.CharField(max_length=100)
    code   = models.CharField(max_length=100)
    url    = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, on_delete=models.CASCADE)

    class Meta:
        ''' class meta info '''
        db_table = 'menu'

    def __str__(self):
        return self.name