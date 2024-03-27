from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def _str_(self):
        return self.name
    
class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    image = models.ImageField(upload_to="room_images/", null=True,blank=True)
    name = name = models.CharField(max_length=200)
    participants = models.ManyToManyField(User,related_name="participants", blank=True)
    description = models.TextField(null=True,blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-update","-created"]

    def _str_(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-update","-created"]


    def _str_(self):
        return self.body[0:20]