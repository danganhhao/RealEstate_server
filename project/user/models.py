from django.db import models

# Create your models here.

# Generate media path to upload image
def uploadLocation(instance, filename, **kwargs):
    filePath = 'user/{user_name}/{filename}'.format(
        user_name=str(instance.username), filename=filename
    )
    return filePath


# User table
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=300)
    gender = models.CharField(max_length=6, null=True, blank=True)
    birthday = models.DateField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    avatar = models.ImageField(upload_to=uploadLocation, null=False, blank=True)
    phoneNumber = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    identifyNumber = models.CharField(max_length=15, null=True, blank=True)
    pin = models.IntegerField(default=000000)

    def __str__(self):
        return self.name


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        # delete if device is login again (just allow maximum 2 device web-mobile)
        super(UserToken, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.name


class ResetPassword(models.Model):
    email = models.CharField(max_length=255, unique=True)
    token = models.CharField(max_length=255, unique=True)
