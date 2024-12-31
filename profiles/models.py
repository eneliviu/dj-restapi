from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


#  **Restrict File Types:** Ensure that only image files can be uploaded to prevent potential security vulnerabilities.
# from django.core.exceptions import ValidationError

# def validate_image(image):
#     file_extension = os.path.splitext(image.name)[1].lower()
#     if file_extension not in ['.jpg', '.jpeg', '.png', '.gif']:
#         raise ValidationError("Unsupported file extension.")

#     class Profile(models.Model):
#       # ... other fields ...
#         image = CloudinaryField(
#             'image',
#             default='sample',
#             validators=[validate_image],
#             blank=True,
#             null=True
#       )


class Profile(models.Model):
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)  # optional
    content = models.TextField(blank=True)  # optional
    # image = models.ImageField(
    #     blank=True,
    #     null=True,
    #     default="../hvc6gc5ikhagzoytuq3k"
    # )
    image = CloudinaryField(
        'image',
        # default='https://res.cloudinary.com/dchoskzxj/image/upload/v1721990160/yg9qwd4v15r23bxwv5u4',
        default="v1734719974/hvc6gc5ikhagzoytuq3k",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)

# post_save.connect(create_profile, sender=User)
