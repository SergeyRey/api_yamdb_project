from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='category'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='genre'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        ordering = ['name']

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='title'
    )
    year = models.PositiveSmallIntegerField(
        validators=[validate_year],
        verbose_name='Year'
    )
    description = models.TextField(
        verbose_name='description'
    )
    genre = models.ManyToManyField(
        to=Genre
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='category'
    )

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='author'
    )
    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='title'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10, 'Максимальная оценка - 10'),
            MinValueValidator(1, 'Минимальная оценка - 1'),
        ],
        verbose_name='score'
    )

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        ordering = (
            '-pub_date',
        )
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_following'),
        )


class Comment(models.Model):
    review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='review'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='author'
    )
    text = models.TextField(
        verbose_name='author'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = (
            '-pub_date',
        )
