from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


def validate_message_content(content):
    if content is None or content == "" or content.isspace():
        raise ValidationError(
            'Content is empty or Invalid',
            code='invalid',
            params={
                'content': content
            }
        )


class User(AbstractUser):
    last_read_date = models.DateTimeField(auto_now_add=True,blank=False, nu
                                           =False)
    online = models.BooleanField(null = False,blank= False,default=False)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def read(self):
        self.last_read_date = timezone.now()
        self.save()

    def unread_message(self):
        return Message.objects.filter(created_at__gt = self.last_read_date).count()


class Message(models.Model):
    id = models.UUIDField(primary_key= True,null=False,default=uuid.uuid4,edita
                          = False)
    author = models.ForeignKey(User,blank=False,null=False, related_name='author_messages',on_delete=models.CASCADE)
    content = models.TextField(validators=[validate_message_content])
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    