from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=100)
    pic = models.ImageField(upload_to="img",blank=True,null=True)
    friends = models.ManyToManyField('Friend',related_name="my_followers")
    # followers = models.ManyToManyField('Following',related_name="my_friends")
    link = models.URLField(null=True,blank=True)
    bio = models.TextField(default="",blank=True,null=True)
    friend_request_sent = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name)

class Friend(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE,related_name="all_friends")

    def __str__(self):
        return self.profile.name + "--" + str(self.id)

class Following(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE,related_name="all_followers")

    def __str__(self):
        return self.profile.name


class ChatMessages(models.Model):
    body = models.TextField()
    msg_sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="message_sender")
    msg_receiver = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="messsage_receiver")
    seen = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

# Create a signal handler to set a default value for the created field
@receiver(pre_save, sender=ChatMessages)
def set_created(sender, instance, **kwargs):
    if not instance.created:
        instance.created = timezone.now()
        
    def __str__(self):
        return self.body[:30]
    