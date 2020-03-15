from django.db import models


# Create your models here.

# Generate media path to upload image
def uploadLocation(instance, filename, **kwargs):
    filePath = 'user/{user_id}/{filename}'.format(
        user_id=str(instance.name.id), filename=filename
    )
    return filePath


# User table
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    avatar = models.ImageField(upload_to=uploadLocation, null=False, blank=True)
    phoneNumber = models.CharField(max_length=15)
    emailAddress = models.EmailField(null=True, blank=True)
    identifyNumber = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name
