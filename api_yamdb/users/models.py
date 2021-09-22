from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):

    USER_ROLES_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]
    FORBIDDEN_USERNAME = [
        'me', 'Me',
        'admin', 'Admin'
    ]
    ERROR_FORBIDDEN_USERNAME = ('Использовать имя "{username}" в качестве '
                                'username запрещено.')

    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )
    role = models.CharField(

        max_length=30,
        choices=USER_ROLES_CHOICES,
        default=USER
    )

    class Meta:
        ordering = ['-date_joined']

    def save(self, *args, **kwargs):
        if self.username in self.FORBIDDEN_USERNAME and not self.is_superuser:
            raise ValidationError(
                self.ERROR_FORBIDDEN_USERNAME.format(username=self.username)
            )
        if self.is_superuser:

            self.role = ADMIN
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR or self.is_superuser

    class Meta:
        ordering = (
            '-username',
        )
