from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import models as auth_models

# Create your models here.
class Room(models.Model):
    roomid = models.IntegerField(unique=True)
    roomnumber = models.IntegerField()
    building = models.CharField(max_length=255)

class Course(models.Model):
    courseid = models.IntegerField(unique=True)
    coursename = models.CharField(max_length=255)
    coursesubject = models.CharField(max_length=255)
    coursenum = models.IntegerField()
    sectionnum = models.IntegerField()
 
class Session(models.Model):
    sessionid = models.IntegerField(unique=True)
    topic = models.CharField(max_length=255)
#    roomid = models.ForeignKey(Room, on_delete=models.CASCADE)
 #   courseid = models.ForeignKey(Course, on_delete=models.CASCADE)

 
class User(models.Model):
    name = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    online = models.BooleanField()
    sessionid = models.ForeignKey(Session, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=255)
    #authsession = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
  
