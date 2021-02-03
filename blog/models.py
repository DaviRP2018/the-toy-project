from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Writer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_editor = models.BooleanField(default=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_writer(sender, instance, created, **kwargs):
    """Creates a writer based on the User model every time an User is created"""
    if created:
        Writer.objects.create(user=instance, name=instance.username)


@receiver(post_save, sender=User)
def save_user_writer(sender, instance, **kwargs):
    """Saves the writer based on the User model every time the User is saved"""
    instance.writer.name = instance.username
    instance.writer.save()


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.BooleanField(default=False)
    written_by = models.ForeignKey(
        Writer, null=True, blank=True, on_delete=models.SET_NULL, related_name="fk_written_by"
    )
    edited_by = models.ForeignKey(Writer, null=True, blank=True, on_delete=models.SET_NULL, related_name="fk_edited_by")

    def __str__(self):
        return self.title
