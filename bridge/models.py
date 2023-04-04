from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserData(models.Model):
    file = models.CharField(max_length=200)
    tool = models.CharField(max_length=200)
    fileName = models.CharField(max_length=200)
    dateTime = models.DateTimeField(default=timezone.now)
    noOfPages = models.CharField(max_length=5)
    user = models.ManyToManyField(User, related_name="fileInfosOfUser")
    fileOwner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookOwnerInfo")

    def __str__(self):
        return self.fileName
