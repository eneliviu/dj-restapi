from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    # image = models.ImageField(
    #     upload_to='images/', default='../tsipho0ghipyymo9gs9s'
    # )
    # '..https://res.cloudinary.com/dchoskzxj/image/upload/v1728892217/tsipho0ghipyymo9gs9s.webp'
    image = CloudinaryField('image', default=None, blank=False)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
